# runllm.py

from database_manager import DatabaseManager
from rag_optimizer import RAGOptimizer
from tts import TTS
from config import LOGGING_CONFIG
import logging

# ===========================
# Logger Setup
# ===========================

# Configure logging based on settings in config.py
logging.basicConfig(
    filename=LOGGING_CONFIG['LOG_FILE'],
    level=logging.getLevelName(LOGGING_CONFIG['LOG_LEVEL']),
    format='%(asctime)s:%(levelname)s:%(message)s'
)
logger = logging.getLogger(__name__)

# ===========================
# TheraxusAI Class
# ===========================

class TheraxusAI:
    def __init__(self, user_id="default_user"):
        """
        Initialize the Theraxus AI system for a specific user.
        
        :param user_id: A unique identifier for the user, used for handling user-specific sessions.
        """
        self.user_id = user_id  # Placeholder for user identification (multi-user support)
        self.db_manager = DatabaseManager()
        self.rag = RAGOptimizer()
        self.tts = TTS()

    def generate_response(self, user_input: str) -> str:
        """
        Generate AI response based on user input.
        
        :param user_input: User's input message as a string.
        :return: Response generated by the AI as a string.
        """
        try:
            # Log the received user input
            logger.info(f"Received input from user {self.user_id}: {user_input}")

            # Add user input to chat history
            self.db_manager.add_chat(user_id=self.user_id, role="user", content=user_input)

            # Retrieve relevant documents for the user-specific context
            relevant_docs = self.rag.search_documents(user_input, user_id=self.user_id)
            context = " ".join(relevant_docs)

            # Placeholder for AI response generation
            # In a real scenario, integrate with a language model like LLama
            response = f"Based on your input, here's a summary: {context[:100]}..."

            # Add AI response to chat history
            self.db_manager.add_chat(user_id=self.user_id, role="assistant", content=response)

            logger.info(f"Generated response for user {self.user_id}: {response}")
            return response
        except Exception as e:
            logger.error(f"Error generating response for user {self.user_id}: {e}")
            return "I'm sorry, I encountered an error while processing your request."

# ===========================
# Main Function for Text-Based Chat
# ===========================

def main():
    """Main function to run the text-based chat interface."""
    try:
        # Ask user to provide a unique user ID for multi-user support
        user_id = input("Enter your user ID (or leave blank for default): ").strip()
        user_id = user_id if user_id else "default_user"

        # Initialize Theraxus AI instance with the provided user ID
        ai = TheraxusAI(user_id=user_id)
        print("Welcome to Theraxus AI! Type 'exit' to quit.")

        while True:
            try:
                # Get input from the user
                user_input = input("\nYou: ").strip()

                # Handle exit commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("AI: Goodbye!")
                    ai.tts.speak("Goodbye!")
                    logger.info(f"User {user_id} ended the session.")
                    break

                # Generate AI response and speak the output
                response = ai.generate_response(user_input)
                print(f"AI: {response}")
                ai.tts.speak(response)

            except KeyboardInterrupt:
                # Handle graceful exit on keyboard interrupt (Ctrl+C)
                print("\nExiting...")
                ai.tts.speak("Goodbye!")
                logger.info(f"User {user_id} interrupted the session with Ctrl+C.")
                break
            except Exception as e:
                logger.error(f"Chat loop error for user {user_id}: {e}")
                print("AI: I encountered an error. Please try again.")

    except Exception as e:
        logger.error(f"Error initializing Theraxus AI: {e}")
        print("An error occurred while starting the application. Please check the logs for more details.")

# ===========================
# Entry Point
# ===========================

if __name__ == "__main__":
    main()

# ===========================
# Instructions for Modifications
# ===========================

# This script serves as the main entry point for the text-based chat interface of Theraxus AI.
# Enhancements made:
# - Added `user_id` for multi-user support, enabling the system to manage separate sessions for each user.
# - Improved error handling and logging for better maintainability and user experience.
# - Added more detailed comments and instructions for developers.

# To modify:
# - Integrate a real language model (e.g., LLama) in the generate_response method.
# - Enhance the response generation logic to utilize context from retrieved documents.
# - Implement additional commands or functionalities as needed (e.g., 'save', 'load', 'docs').
# - Further customize user identification and authentication if needed for advanced multi-user support.
