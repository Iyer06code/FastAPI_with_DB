import requests
import json

BASE_URL = "http://localhost:8000"

def test_chat_flow():
    # 1. Signup a test user
    email = "test_chat_user_1@example.com"
    password = "password123"
    
    print(f"1. Signing up user: {email}")
    try:
        signup_res = requests.post(f"{BASE_URL}/signup", json={"email": email, "password": password})
        print("Signup:", signup_res.status_code, signup_res.json())
    except:
        print("User might already exist, proceeding to login.")

    # 2. Login to get token (if needed, but our current AI route relies on user_id in body, not token auth yet!)
    # Wait, the AI route takes `user_id` in the body. It doesn't use the token dependency yet.
    # `def ask_ai(request: AIRequest, db: Session = Depends(get_db)):` 
    # The `AIRequest` has `user_id`. The route does NOT have `Current User` dependency.
    # So we just need the user ID. 
    # To get the ID, let's login.
    
    print("2. Logging in...")
    login_res = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    if login_res.status_code != 200:
        print("Login failed:", login_res.text)
        return

    # Decode token to get user_id? Or assume ID=1 if first user?
    # Actually, the login response is just tokens. 
    # Let's inspect the `utils/jwt_handler.py` or just assume we know the ID or query the DB directly if we could.
    # But this is a black-box test.
    # Wait, `login` returns `access_token` and `refresh_token`.
    # Does it return user_id? `create_tokens` in `jwt_handler.py`.
    
    # Let's try to get the user ID from the database using a separate script or just guessing.
    # Actually, let's look at `routes/user_routes.py`, `login` returns `Token`.
    # `schemas/Token_schemas.py` probably has access_token.
    
    # FOR NOW, I will just try with user_id=1 or something, assuming the DB has users.
    # Better yet, I'll update the script to use a known user ID if I can.
    # Or just use the `signup` logic to ensure a user exists, and getting the ID might be tricky without a `me` endpoint.
    # Does `user_routes.py` have a `me` endpoint? No.
    
    # I'll rely on the existing user `4mh23cs129a@gmail.com` which might be in the DB.
    # Let's just try user_id=1.
    user_id = 1 

    # 3. Start New Chat
    print("\n3. Starting new chat...")
    req_body = {
        "user_id": user_id,
        "message": "What is the capital of France?"
    }
    chat_res = requests.post(f"{BASE_URL}/ai/ask", json=req_body)
    print("New Chat Response:", chat_res.status_code)
    try:
        chat_data = chat_res.json()
        print(chat_data)
        chat_id = chat_data.get("chat_id")
    except:
        print("Failed to parse response")
        return

    if not chat_id:
        print("Error: No chat_id returned")
        return

    # 4. Continue Chat
    print(f"\n4. Continuing chat {chat_id}...")
    req_body_2 = {
        "user_id": user_id,
        "chat_id": chat_id,
        "message": "And what is its population?"
    }
    chat_res_2 = requests.post(f"{BASE_URL}/ai/ask", json=req_body_2)
    print("Continue Chat Response:", chat_res_2.status_code, chat_res_2.json())

    # 5. Fetch History
    print(f"\n5. Fetching history for user {user_id}...")
    hist_res = requests.get(f"{BASE_URL}/chat/history/{user_id}")
    print("History:", hist_res.status_code, hist_res.json())

    # 6. Fetch Messages
    print(f"\n6. Fetching messages for chat {chat_id}...")
    msg_res = requests.get(f"{BASE_URL}/chat/messages/{chat_id}")
    print("Messages:", msg_res.status_code, msg_res.json())

if __name__ == "__main__":
    test_chat_flow()
