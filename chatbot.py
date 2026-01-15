import streamlit as st
import requests

# --- CONFIGURATION ---
API_URL = "https://YOUR-NGROK-URL-HERE.ngrok-free.app/chat"

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="CrownClown",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- AESTHETIC STYLING (CSS) ---
st.markdown("""
<style>
    /* 1. Global Font imports */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* 2. Base Theme Application */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #ffffff; 
    }
    
    .stMarkdown, .stMarkdown p {
        color: #ffffff !important;
    }
    
    /* 3. Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 4. Background Enhancement */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 15, 15) 0%, rgb(45, 45, 60) 90.2%);
        background-attachment: fixed; /* Fix bg so it doesn't look weird when scrolling */
    }
    
    /* 5. Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1a1b26; /* Deep blue-gray */
        border-right: 1px solid #30363d;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #7aa2f7; /* Soft blue accent */
    }
    
    /* 6. Chat Message Styling */
    .stChatMessage[data-testid="stChatMessage"] {
        background-color: transparent;
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(30, 30, 40, 0.5); /* Slight contrast */
        border-radius: 12px;
        padding: 10px;
        border: 1px solid #30363d;
    }
    
    /* 7. Button Styling */
    .stButton button {
        background: #24283b;
        color: #c0caf5;
        border: 1px solid #414868;
        border-radius: 6px;
        transition: all 0.2s ease;
        text-align: left;
    }
    .stButton button:hover {
        background: #414868;
        color: white;
        border-color: #7aa2f7;
    }
    
    /* 8. Input Field Styling - FIXED "WHITE STRIP" BUG */
    
    /* Target the sticky bottom container */
    [data-testid="stBottom"] {
        background-color: transparent !important;
        background: none !important;
        box-shadow: none !important;
        padding-bottom: 20px; /* Add breathing room at bottom */
    }

    /* Target the inner wrapper of the input */
    [data-testid="stBottom"] > div {
        background-color: transparent !important;
        background: none !important;
    }

    /* Target the actual input box container */
    [data-testid="stChatInput"] {
        background-color: transparent !important;
        border-color: #414868 !important;
    }

    /* Style the typing area (Textarea) */
    .stChatInput textarea {
        background-color: #1a1b26 !important; /* Matches sidebar */
        color: #e0e0e0 !important;
        border: 1px solid #414868 !important;
        border-radius: 10px !important;
    }

    /* Focus state for the input */
    .stChatInput textarea:focus {
        border-color: #7aa2f7 !important;
        box-shadow: 0 0 10px rgba(122, 162, 247, 0.3) !important;
    }

    /* 9. Sticky Sidebar Header (Rename + New Chat) */
    div[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:nth-child(1) {
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: #1a1b26; /* Match Sidebar BG */
        padding-bottom: 10px;
        padding-top: 20px; /* Space for the top */
        border-bottom: 1px solid #30363d;
    }
    
    /* 10. Typography */
    h1 {
        background: linear-gradient(to right, #7aa2f7, #bb9af7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem;
    }
</style>
""", unsafe_allow_html=True)


# --- HEADER AREA ---
st.title("CrownClown")
st.markdown("*Powered by Llama 3.2 via Google Colab*")

st.markdown("---")

# --- STATE MANAGEMENT ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {"Chat 1": []}

if "current_chat_id" not in st.session_state:
    if st.session_state.all_chats:
        st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[0]
    else:
        st.session_state.all_chats = {"Chat 1": []}
        st.session_state.current_chat_id = "Chat 1"

# --- SIDEBAR: CHAT SELECTION ---
with st.sidebar:
    # --- STICKY TOP SECTION ---
    header_container = st.container()
    
    with header_container:
        st.markdown("### Settings")
        
        # 1. Rename
        current_chat_name = st.session_state.current_chat_id
        new_name_input = st.text_input("Rename Current Chat", value=current_chat_name)
        
        if new_name_input and new_name_input != current_chat_name:
            if new_name_input in st.session_state.all_chats:
                st.error("Name already exists.")
            else:
                # Perform rename
                st.session_state.all_chats[new_name_input] = st.session_state.all_chats.pop(current_chat_name)
                st.session_state.current_chat_id = new_name_input
                st.rerun()

        # 2. New Chat Button
        if st.button("+ New Conversation", use_container_width=True):
            new_chat_name = f"Chat {len(st.session_state.all_chats) + 1}"
            while new_chat_name in st.session_state.all_chats:
                 new_chat_name += " (New)"
            st.session_state.all_chats[new_chat_name] = []
            st.session_state.current_chat_id = new_chat_name
            st.rerun()

    # --- SCROLLABLE LIST SECTION ---
    st.markdown("### Conversations")
    
    chat_names = list(st.session_state.all_chats.keys())

    for chat_name in chat_names:
        if st.button(chat_name, key=f"btn_{chat_name}", use_container_width=True):
            st.session_state.current_chat_id = chat_name
            st.rerun()

# --- MAIN CHAT INTERFACE ---
if st.session_state.current_chat_id not in st.session_state.all_chats:
    st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[0]

current_history = st.session_state.all_chats[st.session_state.current_chat_id]

# Container for chat messages
chat_container = st.container()

with chat_container:
    # If empty, show a welcome message
    if not current_history:
        st.markdown(
            """
            <div style='text-align: center; padding: 50px; color: #666;'>
                <h3>Hello!</h3>
                <p>I'm ready to help. Start typing below.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    for message in current_history:
        if message.startswith("User: "):
            with st.chat_message("user"):
                st.markdown(message.replace("User: ", "", 1))
        elif message.startswith("Bot: "):
            with st.chat_message("assistant", avatar="https://img.icons8.com/color/48/android-os.png"):
                st.markdown(message.replace("Bot: ", "", 1))

# --- INPUT AREA ---
if prompt := st.chat_input("Type your message here..."):
    # 1. Update UI immediately
    user_msg_fmt = f"User: {prompt}"
    st.session_state.all_chats[st.session_state.current_chat_id].append(user_msg_fmt)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Call API
    try:
        with st.spinner("Thinking..."):
            payload = {
                "message": prompt,
                "history": st.session_state.all_chats[st.session_state.current_chat_id]
            }
            
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                ai_reply_text = response.json().get("response", "Error: Empty reply")
            else:
                ai_reply_text = f"Error {response.status_code}: {response.text}"
                
        # 3. Update History
        bot_msg_fmt = f"Bot: {ai_reply_text}"
        st.session_state.all_chats[st.session_state.current_chat_id].append(bot_msg_fmt)
        
        with st.chat_message("assistant", avatar="https://img.icons8.com/color/48/android-os.png"):
            st.markdown(ai_reply_text)

        st.rerun()

    except Exception as e:
        st.error(f"Connection Failed: {e}")