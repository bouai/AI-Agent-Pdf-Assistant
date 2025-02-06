import typer
from typing import Optional, List
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.llm.google import Gemini

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
db_url = "postgresql+psycopg2://ai:ai@localhost:5532/ai"

# Function to initialize the knowledge base from the user's input URL
def initialize_knowledge_base(pdf_url: str):
    knowledge_base = PDFUrlKnowledgeBase(
        urls=[pdf_url],
        vector_db=PgVector2(collection="recipes", db_url=db_url)
    )
    knowledge_base.load()
    return knowledge_base

# Introduce the assistant
def introduce_assistant():
    print("\nHello! I am your PDF Assistant. I can help you extract and understand information from a PDF document.")
    print("Please provide a URL to a PDF file you'd like assistance with.\n")

def pdf_assistant(new: bool = False, user: str = "user", pdf_url: Optional[str] = None):
    run_id: Optional[str] = None

    if pdf_url is None:
        # Ask for the PDF URL if not provided
        pdf_url = input("Enter the PDF URL: ").strip()
        if not pdf_url:
            print("PDF URL is required. Exiting...")
            return

    # Initialize the knowledge base with the provided URL
    knowledge_base = initialize_knowledge_base(pdf_url)

    # Storage setup for the assistant
    storage = PgAssistantStorage(table_name="pdf_assistant", db_url=db_url)

    # If continuing an existing session, retrieve the run ID
    if not new:
        existing_run_ids: List[str] = storage.get_all_run_ids(user)
        if len(existing_run_ids) > 0:
            run_id = existing_run_ids[0]

    # Setup the assistant
    assistant = Assistant(
        run_id=run_id,
        user_id=user,
        knowledge_base=knowledge_base,
        storage=storage,
        llm=Gemini(model="gemini-1.5-pro"),
        show_tool_calls=True,  # Show tool calls in the response
        search_knowledge=True,  # Enable the assistant to search the knowledge base
        read_chat_history=True,  # Enable the assistant to read the chat history
    )
    
    if run_id is None:
        run_id = assistant.run_id
        print(f"Started Run: {run_id}\n")
    else:
        print(f"Continuing Run: {run_id}\n")

    # Continuous chat loop until the user types "exit"
    print("\nType 'exit' to end the conversation.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye! Exiting the chat.")
            break
        
        # Simulate the assistant's response to user input (replace with actual LLM call)
        assistant_response = assistant.query(user_input)
        print(f"Assistant: {assistant_response}")

    # Start the assistant's CLI interface
    assistant.cli_app(markdown=True)

if __name__ == "__main__":
    introduce_assistant()  # Introduce the assistant to the user
    typer.run(pdf_assistant)
