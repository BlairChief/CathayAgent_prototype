import streamlit as st
from textwrap import dedent
from agents import WebAgent, PresentationAgent, RetrievalAgent
from knowledge_base import PdfKnowledgeBase
from teams import PresentationTeam

web_agent = WebAgent()

knowledge_base = PdfKnowledgeBase()
knowledge_base.initialize_knowledge_base()

# knowledge_base.pdf_knowledge_base.load(recreate=True, upsert=True)

retrieval_agent = RetrievalAgent(knowledge_base.pdf_knowledge_base)

presentation_agent = PresentationAgent(
    instructions=[
        "You are going to make a presentation using Marp (Visual Studio Code) in Markdown.",
        "You are going to use the sources you got from the internet and the sources we have in the database.",
        "When making the presentation, please include the source, as well as the references.",
        "Include mathematical equations and Python code if possible.",
        "When creating the presentation, you are going to follow the format provided.",
    ],
    expected_output=dedent("""
    ---
    marp: true
    title: Marp
    paginate: true
    theme: uncover
    ---

    # My Presentation

    ---

    ## Slides 1

    Something interesting happens in the first day

    ---

    ## Slides 2

    ![w:300](https://marp.app/assets/marp-logo.svg)

    ---

    ## Slides 3

    ```python
    def foo(self):
        pass
    ```
                
    ---

    ## Slides 4

    $$
    \beta = \alpha + \beta
    $$
    """
    ),
    save_location="data/presentations"
)

presentation_team = PresentationTeam(
    team=[web_agent.agent, retrieval_agent.agent, presentation_agent.agent],
    instructions=[
        "First, you go on the internet, search for the query keywords, and gather the query results."
        "Then, you would go on the database and look for relevant sources.",
        "Important: you are going to make a Marp presentation with the result that you got from the internet and the database",
        "Finally, generate an insightful presentation for technical and non-technical audience.",
    ]
)

if 'openai_model' not in st.session_state:
    st.session_state['openai_model'] = 'gpt-4o'

if 'messages' not in  st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input('What is up?'):
    st.session_state.messages.append(
        {
            'role': 'user',
            'content': prompt
        }
    )

    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        stream=presentation_team.ask(prompt)
        response = st.write_stream(stream)

    st.session_state.messages.append(
        {
            'role': 'assistant',
            'content': response
        }
    )