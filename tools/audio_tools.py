from typing import Union, List
from phi.tools import Toolkit
from faster_whisper import WhisperModel
import tempfile
import os
from pydub import AudioSegment

class AudioTools(Toolkit):
    def __init__(self, model_size: str = "small"):
        """
        初始化 FasterWhisper 模型並註冊轉錄函數。
        
        參數:
            model_size (str): 使用的模型大小（例如："tiny", "base", "small", "medium", "large"）。
        """
        super().__init__(name="audio_tools")
        print(f"Initializing AudioTools with model_size={model_size}")
        self.model = WhisperModel(model_size)
        self.register(self.transcribe_audio)
    
    def transcribe_audio(self, audio_path: str, language: Union[str, None] = None) -> str:
        """
        將音頻文件轉錄為文字。
        
        參數:
            audio_path (str): 音頻文件的路徑。
            language (str, optional): 音頻的語言，若為 None，模型將自動檢測語言。
        
        返回:
            str: 轉錄的文字內容或錯誤訊息。
        """
        print(f"開始轉錄音頻: {audio_path}")
        try:
            segments, info = self.model.transcribe(audio_path, language=language)
            transcript = "\n".join([segment.text for segment in segments])
            print(f"轉錄完成，總長度: {info.duration} 秒")
            return transcript
        except Exception as e:
            print(f"轉錄音頻失敗: {e}")
            return f"錯誤: {e}"
    
    def save_audio(self, audio_data: bytes, sample_width: int, frame_rate: int, channels: int) -> Union[str, bytes]:
        """
        將錄音數據保存為 WAV 文件。
        
        參數:
            audio_data (bytes): 錄音的原始數據。
            sample_width (int): 每個樣本的位數。
            frame_rate (int): 取樣率。
            channels (int): 聲道數。
        
        返回:
            str: 保存的音頻文件路徑或錯誤訊息。
        """
        print("保存錄音數據為 WAV 文件")
        try:
            temp_dir = tempfile.gettempdir()
            audio_path = os.path.join(temp_dir, "recorded_audio.wav")
            audio = AudioSegment(
                data=audio_data,
                sample_width=sample_width,
                frame_rate=frame_rate,
                channels=channels
            )
            audio.export(audio_path, format="wav")
            print(f"音頻文件已保存至: {audio_path}")
            return audio_path
        except Exception as e:
            print(f"保存音頻文件失敗: {e}")
            return f"錯誤: {e}"
