import gradio as gr
from non_llm_chat.src.non_llm_chat.enhanced_chatbot import EnhancedChatbot
# Initialize the enhanced chatbot
enhanced_bot = EnhancedChatbot()

def chatbot_interface(message, history):
    """Interface function for Gradio ChatInterface"""
    response = enhanced_bot.get_response(message)
    return response

# Create Gradio interface with ChatInterface for better conversation flow
iface = gr.ChatInterface(
    fn=chatbot_interface,
    title="🤖 Enhanced Non-LLM Chatbot",
    description="""
    This chatbot is powered by ChatterBot (no LLM required!) and can:
    • Have natural conversations and learn from them
    • Solve basic math problems (try: 'what is 5 + 3 * 2?')
    • Tell you the current time and date
    • Remember recent conversation history
    • Handle greetings, jokes, and general questions
    
    Try commands like: 'conversation history', 'clear history', 'tell me a joke', or ask math questions!
    """,
    examples=[
        "Hello! How are you?",
        "What is 15 + 27?",
        "What time is it?",
        "Tell me a joke",
        "What can you do?",
        "Show conversation history"    ]
    # ,
    # undo_btn="Delete Previous",
    # clear_btn="Clear Chat"
)

if __name__ == "__main__":
    print("Starting Enhanced Non-LLM Chatbot...")
    print("The chatbot will train on first run - this may take a moment.")
    iface.launch(share=True, server_name="0.0.0.0", server_port=7860)