# CrownClown Chatbot

CrownClown is a powerful, custom-trained AI chatbot system that runs its heavy-duty brain on Google Colab (free GPU) while you interact with it through a sleek, modern Streamlit interface on your local computer.

## Architecture

*   **Brain (Backend):** Llama 3.1 8B (Fine-tuned) running on **Google Colab**.
*   **Body (Frontend):** A "Midnight Modern" aesthetic chat interface built with **Streamlit** running on your **Local PC**.
*   **The Bridge:** **Ngrok** tunnels the connection securely from Colab to your PC.

## Why Unsloth?

This project utilizes **Unsloth**, a library designed to optimize Large Language Model (LLM) training and inference.
*   **Speed:** It makes training significantly faster (up to 2x-5x faster than standard Hugging Face implementations).
*   **Efficiency:** It dramatically reduces memory usage, allowing us to fine-tune a powerful model like Llama 3 (8 Billion parameters) entirely within the limits of a **free Google Colab T4 GPU**. Without Unsloth, this would likely cause "Out of Memory" errors on the free tier.

---

## Prerequisites

Before you start, ensure you have:
1.  **A Google Account** (to use Google Colab and Drive).
2.  **An Ngrok Account** (Free tier is fine).
3.  **Python Installed** on your local computer.

---

## Step-by-Step Setup Guide

### Phase 1: Getting Your Ngrok Key (Critical Step)
Ngrok is the magic tool that lets your local computer talk to the Google Colab server. You need a free "Auth Token" to make it work.

1.  Go to [dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup) and create a free account.
2.  Once logged in, look at the sidebar on the left.
3.  Click on **"Your Authtoken"**.
4.  You will see a long string of characters (e.g., `2Ob.....`). **Copy this token.**
5.  Keep this safe; you will need to paste it into the Colab notebook.

### Phase 2: Setting up the Backend (Google Colab)

1.  **Open the Notebook:** Upload the `LLM_server.ipynb` file to your Google Drive or open it directly in Google Colab.

2.  **Select the Correct Runtime:**
    *   Go to `Runtime` > `Change runtime type`.
    *   Set "Hardware accelerator" to **T4 GPU**.
    *   **IMPORTANT:** Do **NOT** use the Google TPU v5e or other TPU options. This codebase is specifically optimized for NVIDIA GPUs (like the T4), and using a TPU will cause errors or poor performance.

3.  **Locate Step 6:** Scroll down to the cell labeled `# === STEP 6: START SERVER ===`.
    *   *Note regarding Training:* You can **SKIP** the training steps (Steps 2 & 3 in the notebook) if you have already trained the model once (the saved model in Google Drive will be used) or if you do not have a custom dataset to finetune. The training step is strictly for injecting specific knowledge/style into the model.

4.  **Paste Token:** Find the line:
    ```python
    NGROK_AUTH_TOKEN = "PASTE_YOUR_TOKEN_HERE"
    ```
    Replace the placeholder with the token you copied in Phase 1.

5.  **Run the Server:** Run the Step 6 cell (and previously the Setup/Install cell Step 1).
6.  **Get the URL:** Once the server cell is running, look at the output. You will see a URL that looks like:
    `Make sure to copy the public URL: https://YOUR-NGROK-URL-HERE.ngrok-free.app/chat`
    **Copy this URL.** This is your API Link.

### Phase 3: Setting up the Frontend (Local Computer)

1.  **Install Dependencies:**
    Open your terminal/command prompt and run:
    ```bash
    pip install streamlit requests
    ```

2.  **Configure the App:**
    Open `chatbot.py` in your code editor.
    Find line 5:
    ```python
    # PASTE YOUR LATEST NGROK URL HERE (From Colab output)
    API_URL = "https://your-new-url.ngrok-free.app/chat"
    ```
    Paste the URL you copied from Colab (make sure to keep the `/chat` at the end).

3.  **Run the Chatbot:**
    In your terminal, navigate to the project folder and run:
    ```bash
    streamlit run chatbot.py
    ```

4.  **Chat!**
    Your browser will open with the "CrownClown" interface. You can now chat locally with your AI model running in the cloud!

---

## Features

*   **Fine-Tuned Model:** Uses a custom-trained version of Llama 3.1 8B.
*   **Persistent Memory:** Saves the model and datasets to your Google Drive automatically.
*   **RAG (Knowledge Base):** Reads facts from `my_knowledge.txt` in your Drive to answer specific questions.
*   **Web Search:** Can search the web for real-time info (news, weather, etc.).
*   **Aesthetic UI:** Feature-rich, dark-themed UI with chat history and management.

---

## Troubleshooting

*   **"Connection Failed":**
    *   Check if the Google Colab cell is still running (it must stay running!).
    *   Did the Ngrok URL change? (It changes every time you restart Colab). Update `API_URL` in `chatbot.py`.
*   **Model not loading:**
    *   Make sure Google Drive is mounted correctly in the Colab notebook.
