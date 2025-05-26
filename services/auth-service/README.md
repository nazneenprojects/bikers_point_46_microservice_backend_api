# To install new python package
- poetry add <package name>


### How the Login Endpoint Works:

Authentication Flow:

Accepts OAuth2PasswordRequestForm (username/password)
Uses the authenticate_user function to verify credentials
If authentication fails, returns 401 Unauthorized


Token Generation:

Creates a JWT token with user email and ID
Sets expiration based on your config settings
Updates the user's last login timestamp in the database


Response:

Returns access token, token type ("bearer"), and expiration time in seconds
