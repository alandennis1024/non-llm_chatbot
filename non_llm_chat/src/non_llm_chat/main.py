"""
Main entry point for the non-LLM chatbot application.
This module provides the main function that can be executed from the command line
or used as an entry point for Databricks Asset Bundle jobs.
"""

import argparse
import logging
import sys
import os
from typing import Optional
# Add the current directory to Python path for imports
#sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask_app import ChatBotFlaskApp
from chatbot import BasicChatBot, ChatBotManager



def setup_logging(log_level: str = "INFO"):
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def run_flask_app(host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
    """
    Run the Flask web application.
    
    Args:
        host: Host address to bind to
        port: Port number to bind to
        debug: Enable debug mode
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting Non-LLM Chatbot Flask Application")
    
    try:
        app = ChatBotFlaskApp(host=host, port=port, debug=debug)
        app.run()
    except Exception as e:
        logger.error(f"Error running Flask app: {str(e)}")
        raise


def run_cli_chat():
    """Run a command-line interface for the chatbot."""
    logger = logging.getLogger(__name__)
    logger.info("Starting Non-LLM Chatbot CLI")
    
    # Create and train a chatbot
    bot = BasicChatBot("CLIChatBot")
    bot.train_basic_conversations()
    
    print("Non-LLM Chatbot CLI")
    print("Type 'quit', 'exit', or 'bye' to exit")
    print("-" * 40)
    
    try:
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Bot: Goodbye! Have a great day!")
                break
            
            if user_input:
                response = bot.get_response(user_input)
                print(f"Bot: {response}")
    
    except KeyboardInterrupt:
        print("\nBot: Goodbye! Have a great day!")
    except Exception as e:
        logger.error(f"Error in CLI chat: {str(e)}")
        print(f"Error: {str(e)}")
    finally:
        bot.cleanup()


def train_and_save_bot(bot_name: str, training_data_file: Optional[str] = None):
    """
    Create and train a chatbot, then save it.
    
    Args:
        bot_name: Name of the bot to create
        training_data_file: Optional path to training data file
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Creating and training bot: {bot_name}")
    
    try:
        bot = BasicChatBot(bot_name)
        
        # Train with basic conversations
        bot.train_basic_conversations()
        
        # Train with English corpus if ChatterBot corpus is available
        try:
            bot.train_with_corpus('chatterbot.corpus.english')
            logger.info("Trained with English corpus")
        except Exception as e:
            logger.warning(f"Could not train with English corpus: {str(e)}")
        
        # Train with custom data if provided
        if training_data_file and os.path.exists(training_data_file):
            with open(training_data_file, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                bot.train_with_conversations(lines)
                logger.info(f"Trained with custom data from {training_data_file}")
        
        logger.info(f"Bot '{bot_name}' created and trained successfully")
        
    except Exception as e:
        logger.error(f"Error creating/training bot: {str(e)}")
        raise


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Non-LLM Chatbot Application")
    parser.add_argument(
        "--mode",
        choices=["web", "cli", "train"],
        default="web",
        help="Run mode: web (Flask app), cli (command line), or train (train bot)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host address for web mode (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port number for web mode (default: 5000)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode for web mode"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    parser.add_argument(
        "--bot-name",
        default="TrainedBot",
        help="Bot name for train mode (default: TrainedBot)"
    )
    parser.add_argument(
        "--training-data",
        help="Path to training data file for train mode"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.log_level)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting application in {args.mode} mode")
    
    try:
        if args.mode == "web":
            run_flask_app(host=args.host, port=args.port, debug=args.debug)
        elif args.mode == "cli":
            run_cli_chat()
        elif args.mode == "train":
            train_and_save_bot(args.bot_name, args.training_data)
        else:
            logger.error(f"Unknown mode: {args.mode}")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)


# For Databricks job execution
def databricks_main():
    """
    Entry point specifically for Databricks job execution.
    Runs the Flask app with default settings suitable for Databricks.
    """
    setup_logging("INFO")
    logger = logging.getLogger(__name__)
    logger.info("Starting Non-LLM Chatbot for Databricks")
    
    try:
        # Run Flask app with settings suitable for Databricks
        run_flask_app(host="0.0.0.0", port=8080, debug=False)
    except Exception as e:
        logger.error(f"Databricks execution error: {str(e)}")
        raise


if __name__ == "__main__":
    main()