import os
from typing import List

class Config:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    GOOGLE_CLOUD_KEY: str = os.getenv("GOOGLE_CLOUD_KEY", "")

    AI_MODEL: str = "gpt-4o"
    AI_TEMPERATURE: float = 0.6
    MAX_TOKENS: int = 600

    THERAPY_APPROACHES: List[str] = [
        "Cognitive Behavioral Therapy (CBT)",
        "Dialectical Behavior Therapy (DBT)",
        "Acceptance and Commitment Therapy (ACT)",
        "General Supportive"
    ]

    DEFAULT_THERAPY_PROMPT: str = (
        "You are a compassionate, multilingual mental health therapist specializing in {therapy_style}. "
        "Your goal is to help users cope with issues such as anxiety, depression, ADHD, stress, and other mental health challenges. "
        "Use evidence-based techniques and maintain a calm, supportive tone in your responses. "
        "If the user is in crisis, recommend contacting a local mental health professional or emergency hotline. "
        "Please respond entirely in {language}. "
        "User says: \"{user_input}\""
    )

    AUTO_DELETE_DAYS: int = 30
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "")

    
    VOICE_LANGUAGES = {
    "English (US)": "en-US"
}


    VOICE_MODEL: str = "eleven_monolingual_v1"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///mindcare.db")