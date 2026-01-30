from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import your logic
from QUESTION_ANALYSIS import rate_question

app = FastAPI(title="Question Quality Evaluator")

# -----------------------------------
# CORS CONFIGURATION (IMPORTANT)
# -----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://chatgpt.com"
    ],  # allow only ChatGPT
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# Request schema
# -----------------------------------
class QuestionInput(BaseModel):
    question: str

# -----------------------------------
# API Endpoint
# -----------------------------------
@app.post("/evaluate")
def evaluate_question(data: QuestionInput):
    """
    API endpoint to evaluate question quality.
    """
    return rate_question(data.question)


