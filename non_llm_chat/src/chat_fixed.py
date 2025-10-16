import gradio as gr
from non_llm_chat.SimpleChatbot import SimpleChatbot

# Initialize the simple chatbot
chatbot = SimpleChatbot()

def chatbot_interface(message, history):
    """Interface function for Gradio ChatInterface"""
    response = chatbot.get_response(message)
    return response

# Create Gradio interface with ChatInterface for better conversation flow
iface = gr.ChatInterface(
    fn=chatbot_interface,
    title="🤖 Simple Non-LLM Chatbot",
    description="""
    This chatbot uses pattern matching and rule-based responses (no LLM required!) and can:
    • Have natural conversations using pattern matching
    • Solve basic math problems (try: 'what is 5 + 3 * 2?')
    • Tell you the current time and date
    • Remember recent conversation history
    • Handle greetings, jokes, and general questions
    • Learn from conversations and store them in a local database
    
    Try commands like: 'conversation history', 'clear history', 'stats', 'tell me a joke', or ask math questions!
    """,
    examples=[
        "Hello! How are you?",
        "What is 15 + 27?",
        "What time is it?",
        "Tell me a joke",
        "What can you do?",
        "Show conversation history",
        "Show stats"
    ]
)

if __name__ == "__main__":
    print("Starting Simple Non-LLM Chatbot...")
    print("This chatbot uses pattern matching and stores conversations locally.")
    iface.launch(share=True, server_name="0.0.0.0", server_port=7860)