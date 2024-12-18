import streamlit as st
from agents import WebAgent

web_agent = WebAgent()

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
        stream=web_agent.ask(prompt)
        response = st.write_stream(stream)

    st.session_state.messages.append(
        {
            'role': 'assistant',
            'content': response
        }
    )