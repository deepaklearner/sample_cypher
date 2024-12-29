# user_api.sh
#!/bin/bash
BASE_URL="http://localhost:8000"

# Example: Create a user
curl -X POST "$BASE_URL/iam/user/create" -d '{"username": "john_doe", "email": "john@example.com"}' -H "Content-Type: application/json"

# Example: Update user info
curl -X PUT "$BASE_URL/iam/user/update" -d '{"username": "john_doe", "email": "new_email@example.com"}' -H "Content-Type: application/json"