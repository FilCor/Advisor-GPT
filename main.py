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

@app.get("/status/{company}")
async def get_status(company: str):
    status = analysis_status.get(company, "Not Started")
    return {"status": status}

@app.get("/result/{company}")
async def get_result(company: str):
    safe_company_name = "".join(x for x in company if x.isalnum())
    filename = f"{safe_company_name}_latest.txt"  # Assuming you save it with this pattern
    if os.path.exists(filename):
        with open(filename, "r") as file:
            content = file.read()
        return {"result": content}
    return {"result": "Analysis not complete or file not found"}

@app.post("/analyze/")
async def analyze_company(company_data: CompanyData, background_tasks: BackgroundTasks):
    company = company_data.company
    task_id = str(uuid.uuid4())
    analysis_status[task_id] = "In Progress"
    background_tasks.add_task(run_analysis, company, task_id)
    return {"message": f"Analysis started for {company}", "task_id": task_id}

async def run_analysis(company, task_id):
    try:
        financial_crew = FinancialCrew(company)
        result = financial_crew.run()
        safe_company_name = "".join(x for x in company if x.isalnum())
        filename = f"{safe_company_name}_{task_id}_latest.txt"
        with open(filename, "w") as file:
            file.write(result)
        analysis_status[task_id] = "Complete"
    except Exception as e:
        analysis_status[task_id] = "Failed"
        print(f"An error occurred: {e}")

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

