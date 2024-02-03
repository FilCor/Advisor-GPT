from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
from datetime import datetime
import os
from textwrap import dedent
from dotenv import load_dotenv
from pydantic import BaseModel, constr
load_dotenv()
from crew.crew import FinancialCrew
import uuid
from ..tasks import run_analysis




from stock_analysis_agents import StockAnalysisAgents
from stock_analysis_tasks import StockAnalysisTasks


# Your existing imports and FinancialCrew class here...

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
templates = Jinja2Templates(directory="templates")
analysis_status = {} 
app.mount("/static", StaticFiles(directory="static"), name="static")

class CompanyData(BaseModel):
    company: str


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze/")
async def analyze_company(company_data: CompanyData):
    task = run_analysis.delay(company_data.company)
    return {"message": "Analysis started", "task_id": task.id}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    status = analysis_status.get(task_id, "Not Started")
    return {"status": status}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    # Cerca il file con il task_id specifico
    for filename in os.listdir('.'):
        if filename.endswith(f"{task_id}_latest.txt"):
            with open(filename, "r") as file:
                content = file.read()
            return {"result": content}
    return {"result": "Analysis not complete or file not found"}

