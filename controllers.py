from fastapi import FastAPI
from services import generate_plan
from models import TrainingPlanRequest, TrainingPlan

app = FastAPI()

@app.get('/')
def health_check():
    return {
        "status": "healthy",
        "api": "UP"
    }

@app.post('/training/plan', response_model= TrainingPlan)
def generate_training_plan(request: TrainingPlanRequest):
    training_plan = generate_plan(request.position, request.division, request.total_hrs, request.daily_duty_hrs)
    return training_plan