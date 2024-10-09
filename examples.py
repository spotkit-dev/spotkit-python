"""
This script demonstrates how to interact with the Highspot API using the spotkitAPI client.

It covers various functionalities, including:
- Initializing the API client with developer credentials
- Retrieving the current authenticated user
- Listing users with various filters and options
- Adding a new user to the system
- Fetching user details by ID or email

Ensure that `CLIENT_KEY` and `CLIENT_SECRET` are set as environment variables before running the script.
"""

import os
from spotkit.api import SpotKitAPI

# Initialize the API client using environment variables for credentials
CLIENT_KEY = os.environ['CLIENT_KEY']  # Your Highspot developer key
CLIENT_SECRET = os.environ['CLIENT_SECRET']  # Your Highspot developer secret

hspt_api = SpotKitAPI(client_id=CLIENT_KEY, client_secret=CLIENT_SECRET)

def get_current_user():
    """
    Retrieves and prints the details of the current authenticated user.
    """
    current_user = hspt_api.get_current_user()
    print("Current User:", current_user)

def list_users_examples():
    """
    Demonstrates listing users with different options.
    """
    # List users with a limit of 10
    users = hspt_api.list_users(limit=10)
    print("Users (limit 10):", users)

    # List users with filtering by email and specific fields
    users = hspt_api.list_users(
        email="heath@hspttrust.com",
        list_options="all",
        with_fields="id,name,email,role"
    )
    print("Filtered Users by Email:", users)

    # List users with pagination and excluding specific fields
    users = hspt_api.list_users(
        limit=5,
        start=0,
        list_options="all",
        with_fields="id,name,email,role",
        exclude_fields="groups"
    )
    print("Users with Pagination and Exclusions:", users)

def add_or_update_user():
    """
    Adds or updates a user in the system and retrieves the user's details if created.

    Returns:
        dict: The created user's details, or an error message if creation fails.
    """
    # Define a new user
    new_user = {
        "email": "newuser14@hspttrust.com",
        "properties": {
            "name": "New",
            "surname": "User14",
            "display_name": "New User14"
        }
    }
    
    # Add or update the user
    response = hspt_api.add_user(new_user)
    user_status = response['collection'][0]['status']
    user_id = response['collection'][0]['id']
    user_created = response['collection'][0]['created']

    print(f"Status: {user_status}")
    print(f"User ID: {user_id}")
    print(f"Created: {user_created}")

    # If the user was created, fetch the user's details
    if user_created:
        user_details = hspt_api.get_user(id=user_id)
        print("User Details:", user_details)
        return user_details
    else:
        print("User was not created.")
        return {"error": "User was not created."}

def get_user_by_email(email):
    """
    Retrieves and prints a user's details by their email.

    Args:
        email (str): The email of the user to retrieve.
    """
    user_details = hspt_api.get_user(email=email)
    print(f"User Details for {email}:", user_details)

if __name__ == "__main__":
    # Get and print the current user
    get_current_user()

    # List users with various options
    list_users_examples()

    # Add a new user and fetch their details
    add_or_update_user()

    # Retrieve user details by email
    get_user_by_email('newuser14@hspttrust.com')