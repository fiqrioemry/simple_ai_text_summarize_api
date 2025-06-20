# app/services/transcription.py
import whisper


whisper_model = whisper.load_model("base") 

async def transcribe_audio_chunk(audio_path: str) -> str:
    try:
        # Transkripsi file audio dengan Bahasa Indonesia
        result = whisper_model.transcribe(audio_path, language="id")
        text = result["text"].strip()
        return text
    except Exception as e:
        raise Exception(f"Failed to transcribe audio chunk {audio_path}: {str(e)}")
