import streamlit as st
from agents import WebAgent, PresentationAgent, RetrievalAgent
from managers import KnowledgeBaseManager
from teams import PresentationTeam

web_agent = WebAgent()

knowledge_base = KnowledgeBaseManager()
knowledge_base.initialize_knowledge_base()

# knowledge_base.pdf_knowledge_base.load(recreate=True, upsert=True)

retrieval_agent = RetrievalAgent(knowledge_base.pdf_knowledge_base)

presentation_agent = PresentationAgent()

presentation_team = PresentationTeam(
    web_agent=web_agent.agent,
    retrieval_agent=retrieval_agent.agent,
    presentation_agent=presentation_agent.agent
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