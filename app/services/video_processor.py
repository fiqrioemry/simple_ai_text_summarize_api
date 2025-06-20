

import os
import shutil
from fastapi import UploadFile
from pydub import AudioSegment
from moviepy.editor import VideoFileClip

# utils
from app.utils.generate_file import generate_pdf_file

# core functions
from app.core.cloudinary import upload_to_cloudinary
from app.core.audio.extract import extract_audio_from_video
from app.core.audio.chunking import split_audio_into_chunks
from app.core.audio.preprocess import normalize_audio, denoise_audio,remove_silence

# services
from app.services.transcription import transcribe_audio_chunk
from app.services.save_to_supabase import save_video_summarize
from app.services.ai_summarizer import generate_summary_from_video_text


async def process_video_summary(file: UploadFile, user_id: str):
    # ensure the temp exist
    os.makedirs("temp", exist_ok=True)

   # save video file to temporary path
    temp_path = f"temp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    # extract audio from video
    audio_file = await extract_audio_from_video(file)

    # normalize audio
    normalized_audio = await normalize_audio(audio_file)

    # noise reduction
    denoised_audio = await denoise_audio(normalized_audio)

    # remove silence from audio
    silenced_audio = await remove_silence(denoised_audio)   


    # get audio duration
    audio_segment = AudioSegment.from_file(silenced_audio)
    audio_duration = int(audio_segment.duration_seconds)

    # split audio into chunks
    audio_chunks = await split_audio_into_chunks(silenced_audio)


    # transcribe each audio chunk - whisper ai
    combined_transcription = []
    for chunk in audio_chunks:
        transcription = await transcribe_audio_chunk(chunk)
        combined_transcription.append(transcription)

    # combine all transcriptions into a single string
    combined_transcription = " ".join(combined_transcription)

    # summarize the combined transcription
    summary = await generate_summary_from_video_text(combined_transcription)

    # generate PDF report
    pdf_result = await generate_pdf_file(summary)

    # upload PDF to cloudinary
    pdf_url = await upload_to_cloudinary(pdf_result)

    # get video file metadata
    file_size = os.path.getsize(temp_path)
    video_clip = VideoFileClip(temp_path)
    video_duration = int(video_clip.duration)
    video_clip.close()

    # delete temporary video file
    os.remove(temp_path)

    # save metadata to database supabase
    video_metadata = await save_video_summarize(
        user_id=user_id,
        pdf_url=pdf_url,
        summary_text=summary,
        file_size=file_size,
        video_duration=video_duration,
        audio_duration=audio_duration,
        original_filename=file.filename,
        transcript_text=combined_transcription
    )

    return video_metadata
