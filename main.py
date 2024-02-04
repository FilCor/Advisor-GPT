from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from textwrap import dedent
from dotenv import load_dotenv
from pydantic import BaseModel, constr
load_dotenv()
from crew.crew import FinancialCrew
from tasks import run_analysis
from celery.result import AsyncResult
from celery_app import celery_app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

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
    task_result = AsyncResult(task_id, app=celery_app)
    # Log dello stato per debug
    logger.info(f"Task {task_id} stato: {task_result.status}")
    return {"status": task_result.status}


@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.ready():
        try:
            result = task_result.get  # Aggiunto timeout per sicurezza
            print(f"Task {task_id} completed with result: {result}")  # Log per debug
            return {"result": result}
        except Exception as e:
            print(f"Error retrieving result for task {task_id}: {e}")  # Log per debug
            return {"error": str(e)}
    else:
        print(f"Task {task_id} is still in progress.")  # Log per debug
    return {"result": "Analysis not complete or task not found"}

