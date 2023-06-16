import requests
from urllib.parse import urlencode

# Set up your Spotify API credentials
client_id = '23eb14aefb1d4e13b79e426c953213ee'
client_secret = 'b6d36e4786034b3eabd8e0be08159439'
redirect_uri = 'http://localhost:8888/callback/'

# Step 1: Obtain authorization code
params = {
    'client_id': client_id,
    'response_type': 'code',
    'redirect_uri': redirect_uri,
    'scope': 'user-read-private user-read-email'  # Add desired scopes here
}

authorization_url = 'https://accounts.spotify.com/authorize?' + urlencode(params)
print('Please visit the following URL to authorize the application:')
print(authorization_url)
authorization_code = input('Enter the authorization code: ')

# Step 2: Exchange authorization code for access and refresh tokens
token_url = 'https://accounts.spotify.com/api/token'
data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri
}

response = requests.post(token_url, data=data)
response_data = response.json()

# Step 3: Handle the response
if 'access_token' in response_data:
    access_token = response_data['access_token']
    refresh_token = response_data['refresh_token']
    expires_in = response_data['expires_in']
    
    # Use the access token to make API requests
    # For example, you can make a GET request to retrieve the current user's profile
    profile_url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(profile_url, headers=headers)
    profile_data = response.json()
    
    # Process the profile data as needed
    print('Logged in as:', profile_data['display_name'])
else:
    print('Error occurred during token exchange:', response_data['error'])
