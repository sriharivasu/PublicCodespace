import streamlit as st
import bcrypt
import json
import cohere
import time

# File to save user data
DATA_FILE = "user_data.json"


# === Data Handling ===
def load_user_data():
    try:
        with open("user_data.json", "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Start fresh if file is empty, corrupt, or missing
        return {}

def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# === Auth Utilities ===
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# === Dialogs ===
@st.dialog("Register")
def register_dialog():
    st.write("Create a new account")
    new_user = st.text_input("Username", key="reg_user")
    new_pass = st.text_input("Password", type="password", key="reg_pass")
    confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
    apikey = st.text_input("API Key (Get one **[here](https://dashboard.cohere.com/api-keys)**)", type="password", key="reg_apikey")

    if st.button("Register"):
        if new_user in user_data:
            st.error("Username already exists.")
        elif new_pass != confirm:
            st.error("Passwords do not match.")
        else:
            user_data[new_user] = {
                "password": hash_password(new_pass),
                "apikey": hash_password(apikey),
                "score": 0,
                "inventory": ["fire", "water", "earth", "air", "light"]
            }
            save_user_data(user_data)
            st.success("Registration successful!")
            if "apikeys" not in st.session_state:
                st.session_state.apikeys = apikey
            st.session_state.user = new_user
            st.rerun()

@st.dialog("Login")
def login_dialog():
    st.write("Log in to your account")
    username = st.text_input("Username", key="log_user")
    password = st.text_input("Password", type="password", key="log_pass")
    apikey2 = st.text_input("Cohere API Key (See yours **[here](https://dashboard.cohere.com/api-keys)**)", type="password", key="log_apikey")

    if st.button("Login"):
        if username not in user_data:
            st.error("User not found.")
        elif not check_password(password, user_data[username]["password"]):
            st.error("Incorrect password.")
        elif not check_password(apikey2, user_data[username]["apikey"]):
            st.error("Incorrect API Key.")
        else:
            st.success("Login successful!")
            st.session_state.user = username
            st.session_state.apikeys = apikey2
            st.rerun()

user_data = load_user_data()

if "user" not in st.session_state:
    st.session_state.user = None
if "selected_elements" not in st.session_state:
    st.session_state.selected_elements = []
if "just_crafted" not in st.session_state:
    st.session_state.just_crafted = False




if st.session_state.user:
    if st.session_state.user and st.session_state.user in user_data:
        username = st.session_state.user
        score = user_data[username]["score"]
        inventory = user_data[username]["inventory"]
    

        st.sidebar.markdown(f"**User:** `{username}`")
        st.sidebar.markdown(f"**Score:** `{score}`")

        st.sidebar.markdown("---")
        st.sidebar.markdown("### Add Elements")

        selected = st.session_state.selected_elements
        for element in sorted(set(inventory), key=str.lower):
            if st.sidebar.button(element.title()):
                if len(selected) < 2 and element not in selected:
                    selected.append(element)
                    st.session_state.selected_elements = selected
                    save_user_data(user_data)
                    st.rerun()
                elif len(selected) >= 2:
                    st.warning("You can only select two elements at a time.")
                    st.rerun()

        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Log Out"):
            st.session_state.user = None
            st.rerun()
        if st.sidebar.button("Save Progress"):
            save_user_data(user_data)
            st.sidebar.success("Progress saved")
    else:
        st.session_state.user = None
else:
    st.sidebar.markdown("### Login or Register")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔐 Login"):
            login_dialog()
    with col2:
        if st.button("🆕 Register"):
            register_dialog()

# === Main Area ===
st.title("⚗️ Elemental Craft")
st.caption("The way you play is by clicking 2 buttons (elements) on the sidebar (left) and if it's a valid combination, it'll give a new element. It is turing complete, meaning that you can achieve whatever you want. Eventually.")

if st.session_state.user:
    selected = st.session_state.selected_elements
    inventory = user_data[st.session_state.user]["inventory"]

    if selected:
        combo_display = " + ".join([e.upper() for e in selected])
        st.markdown(f"**Selected:** `{combo_display}`")
    try:
        co_v2 = cohere.ClientV2(api_key = st.session_state.apikeys)
    except Exception as a:
        st.error(f"⚠️ Cohere API error: {a} You must have had a trial api key.")
    
    if len(selected) == 2 and not st.session_state.just_crafted:
        
        try:
            response = co_v2.chat(
            model="command-a-03-2025",
            messages=[{
                "role": "user",
                "content": f"In Infinite Craft, what is the result of combining {selected[0]} and {selected[1]} as an object? Maximum amount of words should be 4, and you should come straight to the answer, without any extra words. If it's not possible in Infinite Craft, say 'Nothing' (unless if it is Nothing in Infinite Craft)."
            }],
            )
            new_element = response.message.content[0].text.strip(".").strip(",").strip("?").strip("!").strip(" ")
        except Exception as e:
            st.error(f"⚠️ Cohere API error: {e}")
            new_element = None
        
        

        if new_element and new_element.lower() != "nothing":
            st.markdown(f"**Crafting Result:** `{new_element}`")
            if new_element not in inventory:
                inventory.append(new_element)
                user_data[st.session_state.user]["score"] += 1
                save_user_data(user_data) 
                st.success(f"🎉 New Element Discovered: **{new_element}**")
                st.rerun()
                st.rerun()
        else:
            st.error("❌ That combination doesn't do anything... yet.")
            time.sleep(2)
            

        st.session_state.selected_elements = []
        st.session_state.just_crafted = True
        st.rerun()

    if st.session_state.just_crafted:
        st.session_state.just_crafted = False

    if st.button("❌ Clear Selection"):
        st.session_state.selected_elements = []
        st.rerun()
else:
    st.info("Please log in or register to begin crafting.")
