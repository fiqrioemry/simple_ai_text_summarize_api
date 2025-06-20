from app.core.supabase import supabase
from datetime import datetime
from typing import Optional

async def save_video_summarize(
    user_id: str,
    pdf_url: str,
    summary_text: str,
    original_filename: str,
    file_size: Optional[int],
    video_duration: Optional[int],
    audio_duration: Optional[int],
    transcript_text: Optional[str]
):
    data = {
        "user_id": user_id,
        "pdf_url": pdf_url,
        "file_size": file_size,
        "summary_text": summary_text,
        "video_duration": video_duration,
        "audio_duration": audio_duration,
        "transcript_text": transcript_text,
        "original_filename": original_filename,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }

    response = supabase.table("video_summaries").insert(data).execute()

    if response.error:
        raise Exception(f"Supabase insert error: {response.error.message}")

    return response.data[0]
