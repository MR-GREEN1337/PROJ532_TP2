import streamlit as st
import httpx

# Simple Streamlit app for login and signup
class LoginSignupApp:
    def __init__(self):
        self.session = httpx.AsyncClient()

    async def signup(self, new_username, new_password):
        response = await self.session.post(
            "http://127.0.0.1:8000/signup",
            data={"new_username": new_username, "new_password": new_password},
        )
        return response.text

    async def login(self, username, password):
        response = await self.session.post(
            "http://127.0.0.1:8000/login", data={"username": username, "password": password}
        )
        return response.text

def main():
    st.title("Login and Signup App")

    # Login Form
    st.header("Login")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
        result = await app_instance.login(username, password)
        st.write(result)

    # Signup Form
    st.header("Signup")
    new_username = st.text_input("New Username:")
    new_password = st.text_input("New Password:", type="password")
    if st.button("Signup"):
        result = await app_instance.signup(new_username, new_password)
        st.write(result)

if __name__ == "__main__":
    app_instance = LoginSignupApp()
    main()
