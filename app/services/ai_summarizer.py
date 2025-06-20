


from openai import OpenAI
from xml.parsers.expat import model
import google.generativeai as genai
from app.core.config import settings


genai.configure(api_key=settings.GEMINI_API_KEY)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# generate summary for data analysis
async def generate_summary_from_eda(csv_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are an expert data analyst. Analyze the CSV data provided below and give insight in Bahasa. "
                "Write insight like a brief report: mention interesting patterns, anomalies, important columns, and suggestions for further analysis."
            )},
            {"role": "user", "content": f"Berikut adalah sebagian isi file CSV:\n\n{csv_text}"}
        ],
        max_tokens=600,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


# generate summary for data analysis
async def generate_eda_insight(csv_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are an expert data analyst. Analyze the CSV data provided below and give insight in Bahasa. "
                "Write insight like a brief report: mention interesting patterns, anomalies, important columns, and suggestions for further analysis."
            )},
            {"role": "user", "content": f"Berikut adalah sebagian isi file CSV:\n\n{csv_text}"}
        ],
        max_tokens=600,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

#  generate summary from transcribed text of video
async def generate_summary_from_video_text(transcribed_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional assistant that summarizes spoken content into clear, concise, and structured summaries. "
                    "Your goal is to simplify the content while preserving all key points. "
                    "Highlight the most important ideas, steps, or conclusions. Use Bahasa Indonesia."
                )
            },
            {
                "role": "user",
                "content": (
                    "Berikut adalah hasil transkripsi dari sebuah video:\n\n"
                    f"{transcribed_text}\n\n"
                    "Tolong buat ringkasan dalam Bahasa Indonesia yang profesional dan mudah dipahami. "
                    "Fokus pada poin-poin penting, ide utama, atau langkah-langkah penting yang disebutkan."
                )
            }
        ],
        max_tokens=800,
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()




# async def generate_eda_insight(csv_text: str) -> str:
#     try:
#         model = genai.GenerativeModel("models/gemini-1.5-flash")
#         response = model.generate_content(
#             contents=[
#                 {
#                     "role": "user",
#                     "parts": [
#                         "Kamu adalah data analyst profesional. Lakukan EDA berdasarkan data CSV berikut dan beri insight dalam Bahasa Indonesia. "
#                         "Sebutkan pola menarik, anomali, dan saran lanjutan.\n\n"
#                         f"{csv_text}"
#                     ]
#                 }
#             ],
#             generation_config={
#                 "temperature": 0.7,
#                 "max_output_tokens": 600
#             }
#         )
#         return response.text.strip()
#     except Exception as e:
#         return f"Error during Gemini insight generation: {str(e)}"