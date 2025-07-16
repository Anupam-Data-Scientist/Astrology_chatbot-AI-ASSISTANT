from fastapi import FastAPI
from backend.routes.chatbot import chatbot_router
from dotenv import load_dotenv


load_dotenv()

app = FastAPI(title="Astrology Chatbot API")

app.include_router(chatbot_router)