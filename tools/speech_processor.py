from faster_whisper import WhisperModel
from typing import Optional

class SpeechProcessor:
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            print("初始化語音處理模型...")
            cls._instance = super(SpeechProcessor, cls).__new__(cls)
            cls._model = WhisperModel(model_size_or_path="medium")
        return cls._instance
    
    def process_audio(self, audio_file_path: str) -> Optional[str]:
        """
        將語音檔案轉換為文字
        """
        try:
            print("即將開始處理語音檔案...")
            # transcribe返回(segments, info)的tuple
            segments, info = self._model.transcribe(audio_file_path, language="zh")
            
            # 使用list comprehension收集所有segments的文字
            print("正在處理語音檔案...")
            text_segments = []
            for segment in segments:  # 正確迭代generator
                text_segments.append(segment.text.strip())
            print("處理完成")
            
            # 將所有文字片段組合
            transcription = " ".join(text_segments)
            print(f"語音轉換結果: {transcription}")
            
            return transcription
            
        except Exception as e:
            print(f"語音處理錯誤: {e}")
            # 加入更詳細的錯誤資訊
            import traceback
            print(f"詳細錯誤: {traceback.format_exc()}")
            return None