from pydantic import BaseModel
from typing import List, Dict

class Task(BaseModel):
    # tasks":[{"title":"Task {i+1}: string","description":"string", "difficulty": "string", "techStacks":[{"name":"string","type":"string", "description": "string"}],'
    title : str
    description : str
    difficulty : str
    techStacks : List[Dict[str, str]]
    skills : List[Dict[str, str]]

class TrainingPlanRequest(BaseModel):
    position : str
    division : str
    total_hrs : int
    daily_duty_hrs : int

class TrainingPlan(BaseModel):
    title : str
    description : str
    durationInHrs : int
    totalTasks : int
    easyTasksCount : int
    mediumTasksCount : int
    hardTasksCount : int
    tasks : List[Task]