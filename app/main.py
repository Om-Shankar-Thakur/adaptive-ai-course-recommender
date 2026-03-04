from fastapi import FastAPI
from app.api.quiz_routes import router as quiz_router
from app.api.recommendation_routes import router as recommendation_router
from app.api.progress_routes import router as progress_router


app = FastAPI()

app.include_router(quiz_router)
app.include_router(recommendation_router)
app.include_router(progress_router)