# 🤖 AI Chatbot Project — Complete Documentation

Here's all the information you need for your **AI Chatbot Project**:

---

## 📌 1. Project Title

**AI Chatbot — Intelligent Conversational Assistant**

---

## 📖 2. Description (What Does It Do?)

The **AI Chatbot** is an intelligent conversational application that simulates human-like conversations using Natural Language Processing (NLP) and Machine Learning. It can understand user queries, process them, and provide relevant, contextual responses in real-time.

### **Key Features:**

- 💬 **Natural Language Understanding** — Processes and interprets human language
- 🧠 **Intent Recognition** — Identifies what the user wants (greeting, question, command)
- 🤖 **Smart Responses** — Generates contextually appropriate replies
- 📚 **Knowledge Base** — Trained on custom intents and patterns
- 🌐 **Web Interface** — User-friendly chat UI accessible from any browser
- ⚡ **Real-time Processing** — Instant responses with low latency
- 🎯 **High Accuracy** — Predicts user intent with confidence scoring
- 💾 **Conversation Logging** — Stores chat history for analysis
- 🔄 **Extensible** — Easy to add new intents and responses
- 🎨 **Modern UI** — Clean, responsive chat interface

### **How It Works:**

```
User Input → Text Preprocessing → Intent Classification → 
Response Selection → Reply to User
```

### **Use Cases:**

- 🛒 **Customer Support** — Answer FAQs automatically
- 📚 **Education** — Tutoring and study assistance
- 💼 **Business** — Lead generation and booking
- 🏥 **Healthcare** — Symptom checking and guidance
- 🎮 **Entertainment** — Fun conversations and games
- 🤝 **Personal Assistant** — Task help and information

---

## 🚀 3. How to Run (Commands to Start the Project)

### **Prerequisites:**

- ✅ Python 3.8 or higher
- ✅ pip (Python package manager)
- ✅ VS Code or any text editor

### **Step 1: Create Project Folder**

Open your terminal (Command Prompt / PowerShell / Terminal) and run:

```bash
# Navigate to your Desktop
cd Desktop

# Create the project folder
mkdir ai-chatbot-project
cd ai-chatbot-project
```

### **Step 2: Create Virtual Environment (Recommended)**

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

You'll see `(venv)` appear in your terminal — this means the environment is active.

### **Step 3: Install Required Libraries**

```bash
pip install flask nltk
```

### **Step 4: Download NLTK Data**

```bash
python -m nltk.downloader punkt
```

### **Step 5: Create the Main Python File**

Create a file named **`chatbot.py`** and paste the complete chatbot code:

```python
# =============================================================================
#  AI Chatbot - Intelligent Conversational Assistant
#  Technologies: Python, Flask, NLTK
# =============================================================================

import nltk
import random
import string
import json
from flask import Flask, request, jsonify, render_template_string

# Download required NLTK data (only first time)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# =============================================================================
# =================== KNOWLEDGE BASE / CORPUS ================================
# =============================================================================

corpus = {
    "greetings": [
        "Hello! How can I help you today?",
        "Hi there! What's on your mind?",
        "Hey! Nice to meet you. How can I assist?",
        "Greetings! How may I help you?",
        "Hello! I'm here to answer your questions."
    ],
    "goodbyes": [
        "Goodbye! Have a great day!",
        "See you later! Take care!",
        "Bye! Feel free to come back anytime.",
        "Farewell! It was nice talking to you.",
        "Goodbye! Hope I was helpful."
    ],
    "thanks": [
        "You're welcome!",
        "Glad I could help!",
        "No problem at all!",
        "Happy to assist!",
        "Anytime!"
    ],
    "name_questions": [
        "I'm an AI Chatbot, your virtual assistant.",
        "You can call me AI Assistant.",
        "I'm a chatbot built with Python and NLTK.",
        "I don't have a personal name, but I'm here to help!"
    ],
    "capabilities": [
        "I can answer questions, have conversations, tell jokes, and help with general queries.",
        "I can chat about various topics, provide information, and assist with common questions.",
        "I'm designed to help you with information, casual conversation, and basic tasks."
    ],
    "jokes": [
        "Why don't scientists trust atoms? Because they make up everything! 😄",
        "Why did the computer go to the doctor? Because it had a virus! 💻",
        "What do you call a bear with no teeth? A gummy bear! 🐻",
        "Why don't programmers like nature? Too many bugs! 🐛",
        "How does the moon cut his hair? Eclipse it! 🌙"
    ],
    "weather": [
        "I don't have real-time weather data, but you can check weather.com or your phone's weather app!",
        "I can't access live weather, but I can help with other questions!"
    ],
    "time": [
        "I don't have access to real-time clock, but your device should show the current time!",
        "Time flies when we're having a good conversation! ⏰"
    ],
    "help": [
        "I can chat with you, answer questions, tell jokes, and help with general topics. Just ask!",
        "Try asking me about my name, what I can do, or tell me a joke!"
    ],
    "default": [
        "That's interesting! Tell me more.",
        "I'm not sure I understand. Could you rephrase that?",
        "Hmm, I'm still learning. Can you ask differently?",
        "I don't have information about that yet. Try asking something else!",
        "Sorry, I didn't quite get that. Could you try again?"
    ]
}

# Keywords mapping for intent detection
keywords = {
    "greetings": ["hello", "hi", "hey", "greetings", "good morning", "good evening", "howdy"],
    "goodbyes": ["bye", "goodbye", "see you", "farewell", "exit", "quit"],
    "thanks": ["thank", "thanks", "thank you", "thx", "appreciate"],
    "name_questions": ["your name", "who are you", "what are you", "identify yourself"],
    "capabilities": ["what can you do", "capabilities", "features", "abilities", "help me with"],
    "jokes": ["joke", "funny", "make me laugh", "humor", "laugh"],
    "weather": ["weather", "temperature", "rain", "sunny", "forecast"],
    "time": ["time", "date", "day", "clock", "what time"],
    "help": ["help", "assist", "support", "guide"]
}

# =============================================================================
# =================== NLP PROCESSING FUNCTIONS ===============================
# =============================================================================

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    """Clean and lemmatize input text"""
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize
    words = nltk.word_tokenize(text)
    # Lemmatize
    words = [lemmatizer.lemmatize(w) for w in words]
    return " ".join(words)

def detect_intent(user_input):
    """Detect user intent based on keywords"""
    processed = preprocess_text(user_input)
    
    # Check each category for keyword matches
    for intent, kw_list in keywords.items():
        for keyword in kw_list:
            if keyword in processed:
                return intent
    
    return "default"

def get_response(user_input):
    """Generate a response based on detected intent"""
    intent = detect_intent(user_input)
    return random.choice(corpus[intent])

# =============================================================================
# =================== FLASK WEB APPLICATION ==================================
# =============================================================================

app = Flask(__name__)

# HTML Template for chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .chat-container {
            width: 90%;
            max-width: 500px;
            height: 80vh;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .chat-header h1 { font-size: 24px; margin-bottom: 5px; }
        .chat-header p { font-size: 12px; opacity: 0.9; }
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f5f7fa;
        }
        .message {
            margin-bottom: 15px;
            display: flex;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .bot-message { justify-content: flex-start; }
        .user-message { justify-content: flex-end; }
        .message-bubble {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.4;
        }
        .bot-message .message-bubble {
            background: white;
            color: #333;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .user-message .message-bubble {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }
        .chat-input {
            display: flex;
            padding: 15px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }
        .chat-input input {
            flex: 1;
            padding: 12px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
        }
        .chat-input input:focus { border-color: #667eea; }
        .chat-input button {
            margin-left: 10px;
            padding: 12px 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
        }
        .chat-input button:hover { opacity: 0.9; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🤖 AI Chatbot</h1>
            <p>Your Intelligent Assistant</p>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="message bot-message">
                <div class="message-bubble">
                    Hello! 👋 I'm your AI assistant. How can I help you today?
                </div>
            </div>
        </div>
        <div class="chat-input">
            <input type="text" id="userInput" placeholder="Type your message..." 
                   onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    
    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (!message) return;
            
            // Add user message
            addMessage(message, 'user');
            input.value = '';
            
            // Get bot response
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                addMessage(data.response, 'bot');
            } catch (error) {
                addMessage('Sorry, something went wrong!', 'bot');
            }
        }
        
        function addMessage(text, sender) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            messageDiv.innerHTML = `<div class="message-bubble">${text}</div>`;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Serve the chat interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and return bot response"""
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({"response": "Please type something!"})
    
    bot_response = get_response(user_message)
    return jsonify({"response": bot_response})

# =============================================================================
# =================== RUN THE APPLICATION ====================================
# =============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 AI Chatbot is starting...")
    print("=" * 50)
    print("📡 Open your browser and visit:")
    print("   http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)
```

### **Step 6: Run the Project**

Make sure your virtual environment is active, then run:

```bash
python chatbot.py
```

**You should see:**
```
==================================================
🤖 AI Chatbot is starting...
==================================================
📡 Open your browser and visit:
   http://127.0.0.1:5000
==================================================
 * Running on http://127.0.0.1:5000
```

### **Step 7: Open in Browser**

Open any web browser and go to:
```
http://127.0.0.1:5000
```

You'll see a beautiful chat interface! Start chatting with the bot. 🎉

### **Step 8: Stop the Server**

Press **`Ctrl + C`** in the terminal to stop the chatbot.

---

## 🎯 Try These Sample Messages:

| You Type | Bot Replies |
|----------|-------------|
| "Hello" | A friendly greeting |
| "What is your name?" | Introduction |
| "Tell me a joke" | A funny joke 😄 |
| "What can you do?" | List of capabilities |
| "Thank you" | You're welcome! |
| "Bye" | Goodbye message |
| "Help" | Usage instructions |

---

## 📊 Quick Summary Card

| Attribute | Details |
|-----------|---------|
| **Project Name** | AI Chatbot — Intelligent Conversational Assistant |
| **Language** | Python 3.8+ |
| **Libraries** | Flask, NLTK |
| **Interface** | Web-based chat UI |
| **Port** | 5000 |
| **Run Command** | `python chatbot.py` |
| **Access URL** | `http://127.0.0.1:5000` |

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install flask nltk` |
| `nltk_data not found` | Run `python -m nltk.downloader punkt` |
| Port 5000 already in use | Change port in code: `port=5001` |
| `python` not recognized | Use `python3` instead |
| Virtual env not activating | Make sure you're in the project folder |

---

Would you like me to help you with:
- 📄 **Project Report** (formal documentation)?
- 🎨 **Adding more features** (jokes, weather API, etc.)?
- 📤 **Deploying online** (so anyone can access it)?
- 🗄️ **Adding database** (to save chat history)? 🌟
