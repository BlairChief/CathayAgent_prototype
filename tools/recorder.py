import os
from audio_recorder_streamlit import audio_recorder
import streamlit as st
from tools import SpeechProcessor

class AudioHandler:
    def __init__(self):
        """初始化錄音處理器"""
        self.speech_processor = SpeechProcessor()
        self.save_dir = os.getcwd()  # 設定儲存目錄為當前執行路徑

    def setup_recorder(self, 
                      pause_threshold=2.0,
                      sample_rate=44100,
                      recording_color="#e87474",
                      neutral_color="#6aa36f"):
        """設置錄音按鈕"""
        return audio_recorder(
            pause_threshold=pause_threshold,
            sample_rate=sample_rate,
            text="",
            recording_color=recording_color,
            neutral_color=neutral_color
        )

    def process_audio(self, audio_bytes, callback=None):
        """處理錄音並轉換為文字
        
        Args:
            audio_bytes: 錄音的二進位資料
            callback: 處理轉譯文字的回調函數
        """
        logger.info("開始處理語音輸入")
        if not audio_bytes:
            return

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            logger.info(f"已建立儲存目錄: {self.save_dir}")

        temp_audio_path = os.path.join(self.save_dir, "temp_audio.wav")
        try:
            with open(temp_audio_path, 'wb') as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio.flush()
                os.fsync(temp_audio.fileno())  # 確保寫入磁碟
                logger.info(f"暫存語音檔案已建立: {temp_audio_path}")

            transcription = self.speech_processor.process_audio(temp_audio_path)

            if transcription:
                # 如果有提供callback，執行它
                if callback:
                    callback(transcription)
                return transcription

            else:
                logger.warning("語音轉譯失敗")
                st.error("語音轉譯失敗")
                return None

        finally:
            try:
                os.unlink(temp_audio_path)
                logger.info("清理暫存語音檔案")

            except FileNotFoundError:
                logger.warning(f"檔案已不存在：{temp_audio_path}，跳過刪除")
            except PermissionError:
                logger.error(f"無法刪除檔案（權限錯誤）：{temp_audio_path}，跳過刪除")
            except Exception as e:
                logger.error(f"清理檔案時發生其他錯誤：{str(e)}，跳過刪除")
