from fastapi import FastAPI
from pydantic import BaseModel

# Import your logic
from QUESTION_ANALYSIS import rate_question

app = FastAPI(title="Question Quality Evaluator")


class QuestionInput(BaseModel):
    question: str


@app.post("/evaluate")
def evaluate_question(data: QuestionInput):
    """
    API endpoint to evaluate question quality.
    """
    return rate_question(data.question)



