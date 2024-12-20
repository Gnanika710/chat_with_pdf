
user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.scdn.co/image/ab67616d00001e02964a582949cbf461ce54375f" alt="User Avatar">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''


bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdJGnVoEMYC_2cdHJLZPezjqse6nLYURLcCQ&s" alt="Bot Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''


typing_indicator_template = '''
<div class="typing-indicator">
    <span></span><span></span><span></span>
</div>
'''


css = """
<style>
    .stTextInput input {
        background-color: #2E2E2E;
        color: white;
        border: 1px solid #555555;
        padding: 10px;
        font-size: 16px;
        border-radius: 5px;
    }

    .stTextInput label {
        color: white;
        font-size: 14px;
        font-weight: bold;
    }

    .stTextInput div {
        margin-bottom: 20px;
    }

    .chat-message {
        display: flex;
        margin-bottom: 20px;
        padding: 10px;
        border-radius: 5px;
    }

    .chat-message.user {
        background-color: #5c6bc0;
        color: white;
        flex-direction: row-reverse;
    }

    .chat-message.bot {
        background-color: #607d8b;
        color: white;
        flex-direction: row;
    }

    .chat-message .avatar img {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin: 0 10px;
    }

    .chat-message .message {
        max-width: 70%;
        word-wrap: break-word;
    }

    .typing-indicator {
        display: inline-block;
        margin-top: 10px;
    }

    .typing-indicator span {
        display: inline-block;
        width: 8px;
        height: 8px;
        margin-right: 5px;
        border-radius: 50%;
        background-color: #ffffff;
        animation: typing 1.2s infinite ease-in-out;
    }

    .typing-indicator span:nth-child(1) {
        animation-delay: 0s;
    }

    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }

    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes typing {
        0% {
            opacity: 0;
        }
        50% {
            opacity: 1;
        }
        100% {
            opacity: 0;
        }
    }

    .background-music {
        display: none;
    }
</style>
"""
