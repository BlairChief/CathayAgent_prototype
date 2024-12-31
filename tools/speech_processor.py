from openai import OpenAI
from typing import Optional

client = OpenAI()

class SpeechProcessor:
    def __init__(self):
        return
        
    def transcribe(self, audio_file_path: str) -> str:
        with open(f"{audio_file_path}", "rb") as audio_file:
            return client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text",
                temperature=0.1
            )
    
    def process_audio(self, audio_file_path: str) -> Optional[str]:
        """
        將語音檔案轉換為文字
        """
        try:
            print("即將開始處理語音檔案...")
            transcription = self.transcribe(audio_file_path) 
            if not transcription:
                print("未取得轉換結果")
                return None
                
            print(f"語音轉換結果: {transcription}")
            return transcription
        
        except FileNotFoundError as e:
            print(f"找不到檔案: {audio_file_path}")
            return None
        
        except Exception as e:
            print(f"語音處理錯誤: {e}")
            # 加入更詳細的錯誤資訊
            import traceback
            print(f"詳細錯誤: {traceback.format_exc()}")
            return None