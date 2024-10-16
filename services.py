import json
import os
import base64
from dotenv import load_dotenv
from groq import Groq
from firebase_config import db

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def generate_tasks(task_count, task_difficulty, start_index, total_hours, position, division, tasks_per_prompt):
    tasks = []
    easy_tasks_count = 0
    medium_tasks_count = 0
    hard_tasks_count = 0
    for i in range(0, task_count, tasks_per_prompt):
        tasks_left = min(tasks_per_prompt, task_count - i)
        prompt = (
            f"Give the JSON formatted training plan with {tasks_left} tasks (numbering of task starts at {start_index + i}) for a {total_hours}-hour internship of a {position} role in {division}. "
            f"All tasks should be {task_difficulty} difficulty."
            "Ensure the JSON strictly follows this schema, and only give the json and strictly no other texts: "
            '"tasks":[{"title":"Task {i+1}: string","description":"string", "difficulty": "string", "techStacks":[{"name":"string","type":"string", "description": "string"}],'
            '"skills":[{"name":"string","description":"string"}]}]}'
        )
        messages = [{"role": "user", "content": prompt}]
        output = client.chat.completions.create(
            messages=messages,
            model="llama3-groq-70b-8192-tool-use-preview",
        )
        generated_text = output.choices[0].message.content
        tasks.extend(json.loads(generated_text)["tasks"])
        for task in tasks:
            difficulty = task.get("difficulty", "").lower()
            if difficulty == "easy":
                easy_tasks_count += 1
            elif difficulty == "medium":
                medium_tasks_count += 1
            elif difficulty == "hard":
                hard_tasks_count += 1
    return tasks, easy_tasks_count, medium_tasks_count, hard_tasks_count

def generate_plan(position: str, division: str, total_hours: int, daily_duty_hrs : int):
    number_of_tasks = total_hours // (daily_duty_hrs * 5)
    tasks_per_prompt = 3
    easy_tasks = int(number_of_tasks * 0.4)
    medium_tasks = int(number_of_tasks * 0.4)
    hard_tasks = number_of_tasks - easy_tasks - medium_tasks

    training_plan = {
        "title": f"{position} Internship Training Plan",
        "description": f"A comprehensive training plan for a {total_hours}-hour internship in {division}, designed to equip interns with the necessary skills and knowledge to excel as a {position}.",
        "durationInHrs": total_hours,
        "totalTasks" : 0,
        "easyTasksCount" : 0,
        "mediumTasksCount" : 0,
        "hardTasksCount" : 0,
        "tasks": []
    }

    easy_tasks, easy_count, _, _ = generate_tasks(easy_tasks, "Easy", 1, total_hours, position, division, tasks_per_prompt)
    medium_tasks, _, medium_count, _ = generate_tasks(medium_tasks, "Medium", easy_count + 1, total_hours, position, division, tasks_per_prompt)
    hard_tasks, _, _, hard_count = generate_tasks(hard_tasks, "Hard", easy_count + medium_count + 1, total_hours, position, division, tasks_per_prompt)

    training_plan["tasks"].extend(easy_tasks)
    training_plan["tasks"].extend(medium_tasks)
    training_plan["tasks"].extend(hard_tasks)

    training_plan["totalTasks"] = len(training_plan["tasks"])
    training_plan["easyTasksCount"] = easy_count
    training_plan["mediumTasksCount"] = medium_count
    training_plan["hardTasksCount"] = hard_count

    document_id = f"{position}_{division}_{total_hours}_hrs_{len(training_plan["tasks"])}_tasks"

    db.collection('trainingPlans').document(document_id).set(training_plan)

    return training_plan
