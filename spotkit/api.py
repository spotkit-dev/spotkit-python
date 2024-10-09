import requests
import json
import logging
from requests.auth import HTTPBasicAuth

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpotKitAPI:
    BASE_URL = "https://api.latest.highspot.com"
    
    def __init__(self, version="v1.0", api_key: str = None, client_id=None, client_secret=None, use_basic_auth=False):
        """
        Initializes the spotkitAPI client.

        Args:
            version (str): The API version to use.
            api_key (str, optional): The API key for authentication.
            client_id (str, optional): The client ID for OAuth authentication.
            client_secret (str, optional): The client secret for OAuth authentication.
            use_basic_auth (bool, optional): Flag to use basic authentication.
        """
        self.version = version
        self.api_key = api_key
        self.client_id = client_id
        self.client_secret = client_secret
        self.use_basic_auth = use_basic_auth

        # If API_key is not provided, fetch the bearer token using client credentials
        # if not api_key and client_id and client_secret:
        #     self.api_key = self.get_bearer_token()
        # Fetch the bearer token if Basic Auth is not enabled and no API key is provided
        if not use_basic_auth and not api_key and client_id and client_secret:
            self.api_key = self._get_bearer_token()
        
        self.headers = {
            #"Authorization": f"Bearer {self.api_key}",
            "Authorization": f"Bearer {self.api_key}" if not use_basic_auth else "",
            "Content-Type": "application/json",
        }

    def _get_full_url(self, endpoint):
        """
        Constructs the full URL for the API request.

        Args:
            endpoint (str): The API endpoint.

        Returns:
            str: The full URL for the API request.
        """
        return f"{self.BASE_URL}/{self.version}/{endpoint}"

    def _get_bearer_token(self):
        """
        Obtains a bearer token using client credentials.

        Returns:
            str: The bearer token if successful, otherwise False.
        """
        try:
            token_response = self._post(
                "auth/oauth2/token",
                data={"grant_type": "client_credentials"},
                auth=HTTPBasicAuth(self.client_id, self.client_secret),
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            return token_response.get('access_token') if token_response else False
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to obtain bearer token: {e}")
            return False
    
    def _get_auth(self):
        """
        Returns the appropriate authentication method based on use_basic_auth flag.

        Returns:
            HTTPBasicAuth or None: The authentication method, if applicable.
        """
        if self.use_basic_auth and self.client_id and self.client_secret:
            return HTTPBasicAuth(self.client_id, self.client_secret)
        return None
    
    def _get(self, endpoint, params=None):
        """
        Internal method to send a GET request to the API.

        Args:
            endpoint (str): The API endpoint.
            params (dict, optional): Query parameters for the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = self._get_full_url(endpoint)
        try:
            response = requests.get(url, headers=self.headers, params=params, auth=self._get_auth())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"GET request failed for {url}: {e}")
            return {"error": str(e)}

    def _post(self, endpoint, data=None, auth=None, headers=None):
        """
        Internal method to send a POST request to the API.

        Args:
            endpoint (str): The API endpoint.
            data (dict, optional): The data to send in the request.
            auth (requests.auth.HTTPBasicAuth, optional): The authentication method to use.
            headers (dict, optional): Additional headers to include in the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = self._get_full_url(endpoint)
        headers = headers if headers else self.headers
        try:
            response = requests.post(url, headers=headers, data=data, auth=auth or self._get_auth())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"POST request failed for {url}: {e}")
            return {"error": str(e)}

    def _patch(self, endpoint, data=None):
        """
        Internal method to send a PATCH request to the API.

        Args:
            endpoint (str): The API endpoint.
            data (dict, optional): The request body data.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = self._get_full_url(endpoint)
        try:
            response = requests.patch(url, headers=self.headers, data=data, auth=self._get_auth())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"PATCH request failed for {url}: {e}")
            return {"error": str(e)}

    def _delete(self, endpoint):
        """
        Internal method to send a DELETE request to the API.

        Args:
            endpoint (str): The API endpoint.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = self._get_full_url(endpoint)
        try:
            response = requests.delete(url, headers=self.headers, auth=self._get_auth())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"DELETE request failed for {url}: {e}")
            return {"error": str(e)}

    # Users
    def get_current_user(self):
        """
        Retrieves the current authenticated user's details.

        Returns:
            dict: A dictionary containing the user's details.
        """
        return self._get("me")
    
    def list_users(self, email=None, limit=25, start=0, list_options=None, with_fields=None, exclude_fields=None):
        """
        List users with optional filtering by email and pagination.
        
        Args:
            email (str, optional): Filter users by email.
            limit (int, optional): The maximum number of users to return.
            start (int, optional): The starting point for pagination.
            list_options (str, optional): Additional list options as a comma-separated string.
            with_fields (str, optional): Fields to include as a comma-separated string.
            exclude_fields (str, optional): Fields to exclude as a comma-separated string. (groups, favorites, or askterisk for wildcard)
        
        Returns:
            dict: A dictionary containing the list of users.
        """
        params = {'email': email, 
                'limit': limit, 
                'start': start,
                'list': list_options,
                'with-fields': with_fields,
                'exclude-fields': exclude_fields
                }
        # Remove keys with None values to avoid sending them in the request
        params = {key: value for key, value in params.items() if value is not None}
        return self._get("users", params=params)

    def add_user(self, user_data):
        """
        Adds or updates a user in the system.

        Args:
            user_data (dict): A dictionary containing user details.

        Returns:
            dict: A dictionary containing the API's response.
        """
        try:
            json_data = json.dumps([user_data])
            return self._post("users", data=json_data)
        except Exception as e:
            logger.error(f"Failed to add user: {e}")
            return {"error": str(e)}

    def delete_user(self, user_id):
        """
        Deletes a user by their user ID.

        Args:
            user_id (str): The ID of the user to delete.

        Returns:
            dict: A dictionary containing the API's response.
        """
        return self._delete(f"users/{user_id}")

    def get_user(self, id=None, email=None):
        """
        Retrieves a user's details by their user ID or email.

        Args:
            id (str, optional): The ID of the user to retrieve.
            email (str, optional): The email of the user to retrieve.

        Returns:
            dict: A dictionary containing the user's details.

        Raises:
            ValueError: If neither `id` nor `email` is provided.
        """
        if not id and not email:
            raise ValueError("You must specify at least one of user 'id' or user 'email'.")

        # If user_email is provided, retrieve the user_id using list_users
        if email:
            users = self.list_users(email=email, list_options="all")
            if users.get('collection'):
                id = users['collection'][0]['id']
            else:
                logger.error(f"User not found with the provided email: {email}")
                return {"error": "User not found with the provided email."}

        # Now use the user_id to get the user details
        return self._get(f"users/{id}")

     # Spots
    def list_spots(self, role=None, limit=100, start=0):
        """
        List spots with optional role filtering and pagination.

        Args:
            role (str, optional): The role to filter spots.
            limit (int, optional): The maximum number of spots to return.
            start (int, optional): The starting point for pagination.

        Returns:
            dict: A dictionary containing the list of spots.
        """
        params = {'role': role, 'limit': limit, 'start': start}
        return self._get("spots", params=params)

    def get_spot(self, spot_id):
        """
        Retrieve a spot's details by its ID.

        Args:
            spot_id (str): The ID of the spot to retrieve.

        Returns:
            dict: A dictionary containing the spot's details.
        """
        return self._get(f"spots/{spot_id}")

    def create_spot(self, spot_data):
        """
        Create a new spot.

        Args:
            spot_data (dict): A dictionary containing the spot's details.

        Returns:
            dict: A dictionary containing the API's response.
        """
        try:
            return self._post("spots", data=json.dumps(spot_data))
        except Exception as e:
            logger.error(f"Failed to create spot: {e}")
            return {"error": str(e)}

    def update_spot(self, spot_id, spot_data):
        """
        Update an existing spot's details.

        Args:
            spot_id (str): The ID of the spot to update.
            spot_data (dict): A dictionary containing the updated details.

        Returns:
            dict: A dictionary containing the API's response.
        """
        return self._patch(f"spots/{spot_id}", data=spot_data)

    def delete_spot(self, spot_id):
        """
        Deletes a spot by its ID.

        Args:
            spot_id (str): The ID of the spot to delete.

        Returns:
            dict: A dictionary containing the API's response.
        """
        return self._delete(f"spots/{spot_id}")

    def get_spot_by_name(self, spot_name, role=None):
        """
        Helper method to get a spot ID by its name.

        Args:
            spot_name (str): The name of the spot to retrieve.
            role (str, optional): The role to filter spots.

        Returns:
            str: The spot ID if found, otherwise 'Spot not found'.
        """
        spots = self.list_spots(role=role)
        for spot in spots.get('collection', []):
            if spot.get('title') == spot_name:
                return spot.get('id')
        return "Spot not found"

    # Items
    def list_items_in_spot(self, spot_id, limit=100, start=0):
        """
        List items within a spot.

        Args:
            spot_id (str): The ID of the spot to list items from.
            limit (int, optional): The maximum number of items to return.
            start (int, optional): The starting point for pagination.

        Returns:
            dict: A dictionary containing the list of items.
        """
        params = {'limit': limit, 'start': start}
        return self._get(f"spots/{spot_id}/lists", params=params)

    def get_item(self, item_id):
        """
        Retrieve an item's details by its ID.

        Args:
            item_id (str): The ID of the item to retrieve.

        Returns:
            dict: A dictionary containing the item's details.
        """
        return self._get(f"items/{item_id}")

    def add_item(self, spot_id, item_data):
        """
        Add an item to a spot.

        Args:
            spot_id (str): The ID of the spot to add the item to.
            item_data (dict): A dictionary containing the item's details.

        Returns:
            dict: A dictionary containing the API's response.
        """
        try:
            return self._post(f"spots/{spot_id}/items", data=json.dumps(item_data))
        except Exception as e:
            logger.error(f"Failed to add item: {e}")
            return {"error": str(e)}

    def update_item(self, item_id, item_data):
        """
        Update an item's details.

        Args:
            item_id (str): The ID of the item to update.
            item_data (dict): A dictionary containing the updated details.

        Returns:
            dict: A dictionary containing the API's response.
        """
        return self._patch(f"items/{item_id}", data=item_data)

    def delete_item(self, item_id):
        """
        Delete an item by its ID.

        Args:
            item_id (str): The ID of the item to delete.

        Returns:
            dict: A dictionary containing the API's response.
        """
        return self._delete(f"items/{item_id}")

    # Groups
    def list_groups(self, role=None, limit=100, start=0):
        """
        List groups with optional role filtering and pagination.

        Args:
            role (str, optional): The role to filter groups.
            limit (int, optional): The maximum number of groups to return.
            start (int, optional): The starting point for pagination.

        Returns:
            dict: A dictionary containing the list of groups.
        """
        params = {'role': role, 'limit': limit, 'start': start}
        return self._get("groups", params=params)

    def get_group(self, group_id):
        """
        Retrieve a group's details by its ID.

        Args:
            group_id (str): The ID of the group to retrieve.

        Returns:
            dict: A dictionary containing the group's details.
        """
        return self._get(f"groups/{group_id}")

    def create_group(self, group_data):
        """
        Create a new group.

        Args:
            group_data (dict): A dictionary containing the group's details.

        Returns:
            dict: A dictionary containing the API's response.
        """
        try:
            return self._post("groups", data=json.dumps(group_data))
        except Exception as e:
            logger.error(f"Failed to create group: {e}")
            return {"error": str(e)}

    def update_group(self, group_id, group_data):
        """
        Update a group's details.

        Args:
            group_id (str): The ID of the group to update.
            group_data (dict): A dictionary containing the updated details.

        Returns:
            dict: A dictionary containing the API's response.
        """
        return self._patch(f"groups/{group_id}", data=group_data)

    def delete_group(self, group_id):
        """
        Delete a group by its ID.

        Args:
            group_id (str): The ID of the group to delete.

        Returns:
            dict: A dictionary containing the API's response.
        """
        return self._delete(f"groups/{group_id}")