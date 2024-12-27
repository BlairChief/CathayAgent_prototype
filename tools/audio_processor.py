from streamlit_webrtc import AudioProcessorBase
import av

class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.buffer = []
        print("AudioRecorder initialized")
    
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.buffer.append(frame.to_ndarray().copy())
        return frame
    
    def get_audio_data(self) -> bytes:
        """
        將錄音數據轉換為 bytes。
        
        返回:
            bytes: 錄音的原始數據。
        """
        print("AudioRecorder: Converting audio frames to bytes")
        audio_data = b''.join([frame.tobytes() for frame in self.buffer])
        return audio_data
