import firebase_admin
from firebase_admin import credentials, auth



# 1. Initialize Firebase Admin
cred = credentials.Certificate("key.json")
app = firebase_admin.initialize_app(cred)

def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        print(f"User created successfully: {user.uid}")
        return user.uid  # Return the user ID for later use
    except Exception as e:
        print(f"Error creating user: {e}")
        return None


def check_user_exists(email, password):
    try:
        # Try to sign in the user with provided credentials
        user = auth.get_user_by_email(email=email)
        # If sign-in succeeds, user exists
        firebase_admin.delete_app(app)
        return True
    except Exception as e:
        # If sign-in fails (wrong credentials), user doesn't exist
        print(f"Error: {e}")
        return False

