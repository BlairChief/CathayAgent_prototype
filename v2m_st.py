import streamlit as st
from v2m import initv2m
from agents import WebAgent, YfinanceAgent, EmailAgent
from tools.recorder import AudioHandler

# 初始化全局狀態
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.debug_mode = False
    st.session_state.messages = []
    st.session_state.audio_processed = False
    
    # 只在第一次初始化時執行
    try:
        st.session_state.web_agent = WebAgent()
        st.session_state.yfinance_agent = YfinanceAgent()
        st.session_state.email_agent = EmailAgent()
        st.session_state.audio_handler = AudioHandler()
        st.session_state.initialized = True
        print("所有agents初始化成功")
        print("初始化聊天記錄")
        print("程式啟動...")
    except Exception as e:
        print(f"Agent初始化錯誤: {str(e)}")
        st.error("系統初始化失敗，請檢查設置")

def process_input(text_prompt):
    """處理輸入文字並回傳結果"""
    try:
        with st.chat_message("user"):
            st.markdown(text_prompt)

        print(f"收到新的輸入: {text_prompt[:50]}...")
        v2m_team = initv2m()
        response_text = ""
        
        # 處理助理回應
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            for response in v2m_team.ask(text_prompt):
                response_text += response
                message_placeholder.markdown(response_text + "...▌")
                    
            message_placeholder.markdown(response_text)
            print("回應生成完成")
            
        # 保存回應到歷史記錄
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        print("已添加助理回應到歷史記錄")
        
    except Exception as e:
        print(f"處理錯誤: {str(e)}")
        st.error(f"處理錯誤: {str(e)}")

def handle_transcription(transcription):
    if transcription:
        print(f"開始處理轉譯結果")
        try:
            # 顯示使用者語音輸入
            with st.chat_message("user"):
                st.markdown(transcription)
            
            # 處理並生成回應
            process_input(transcription)
            
            print("語音輸入處理完成")
            
        except Exception as e:
            print(f"處理語音輸入時發生錯誤: {str(e)}")
            st.error("處理語音輸入時發生錯誤")

def main():
    st.title("V2M Agent")

    # 新增輸入類型狀態
    if 'input_type' not in st.session_state:
        st.session_state.input_type = None

    # Debug模式切換
    if st.sidebar.checkbox("Debug模式"):
        st.session_state.debug_mode = True
    else:
        st.session_state.debug_mode = False

    # 顯示歷史訊息
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 底部輸入區域
    with st.container():
        col1, col2 = st.columns([0.85, 0.15])
        with col2:
            if st.session_state.initialized:
                audio_bytes = st.session_state.audio_handler.setup_recorder()
                if audio_bytes and not st.session_state.audio_processed:
                    st.session_state.audio_processed = True
                    st.session_state.audio_handler.process_audio(audio_bytes, handle_transcription)
                    st.session_state.audio_processed = False
                    st.session_state.input_type = None  # 重置輸入類型
                    
                
        with col1:
            if prompt := st.chat_input("輸入訊息:"):
                st.session_state.input_type = "text"
                process_input(prompt)
                st.session_state.input_type = None
                
if __name__ == "__main__":
    main()