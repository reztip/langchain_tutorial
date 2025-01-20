import streamlit as st
import psycopg2
from langchain.prompts import PromptTemplate    
from langchain_ollama import ChatOllama
import pydantic

# Database connection settings
DB_HOST = 'localhost'
DB_NAME = 'ollama_tutorial'
DB_USER = 'ollama_tutorial'
DB_PASSWORD = 'ollama_tutorial'

class StreamlitAgent(pydantic.BaseModel):
    name: str
    description: str
def invoke_agent(agent: StreamlitAgent):

    llm = ChatOllama(model = "llama3.1")
    prompt = PromptTemplate.from_template(f"""
    You are an one of many agent that responds to simple questions on a UI.  However, your reponse is tailored to your personality, and you start the reply with your name.
    The following description is a background on your personality and dicates how you should respond:
    Description: {agent.description}
    """
    )
    chain = prompt | llm
    response = chain.invoke({"input": state["input"]})
    decision = response.content.strip().lower()
    return {"decision": decision, "input": state["input"]}

# Establish a connection to the PostgreSQL database
def main():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cursor = conn.cursor()

    # Get the list of agent names from the database
    cursor.execute("SELECT name FROM agents")
    agents = [row[0] for row in cursor.fetchall()]

    st.title("Chat with your favorite LLM!")
    # Radio selection for choosing a list of entries named "Agents" or creating a new agent entry
    agent_choice = st.selectbox('Select an Agent', ['New Agent'] + agents)

    if agent_choice == 'New Agent':
        # Show the form for creating a new agent entry if no existing agents are selected
        new_agent_name = st.text_input('Agent Name')
        new_agent_description = st.text_area('Agent Description')

        if st.button('Submit New Agent'):
            cursor.execute("INSERT INTO agents VALUES (%s, %s)", (new_agent_name, new_agent_description))
            conn.commit()

    # Title of the page

    elif agent_choice != 'New Agent':
        # Show a list of existing agents
        st.write(f"Selected Agent: {agent_choice}")
        
        # Create a text area for the user to input their question
        question = st.text_area("Ask an AI Question")

        if st.button('Submit'):
            # Code here would typically involve interacting with an LLM, but 
            # for simplicity we'll just print out a mock response.
            responses = ["The answer is 42.", "It's a trick question. The answer is actually 23.", "I'm not sure."]
            response = st.write(responses[0])
    
    cursor.close()


if __name__ == "__main__":
    main()