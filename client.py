import os
from spotkit.api import SpotKitAPI

# Initialize the API client
#highspot tenant ->settings ->developer ->basics
CLIENT_KEY = os.environ['CLIENT_KEY'] # your highspot developer key
CLIENT_SECRET= os.environ['CLIENT_SECRET'] #your highspot developer secret

hspt_api = spotkitAPI(client_id=CLIENT_KEY, client_secret=CLIENT_SECRET, use_basic_auth=True)

# Get current user
current_user = hspt_api.get_current_user()
print(current_user)

# List users
users = hspt_api.list_users(limit=10)

# # Add or update a user
# new_user = {
#     "email": "newuser@example.com",
#     "properties": {
#         "first_name": "New",
#         "last_name": "User"
#     }
# }
# response = hspt_api.add_user(new_user)