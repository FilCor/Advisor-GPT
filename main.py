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
    company: constr(strip_whitespace=True, min_length=1)


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/status/{company}")
async def get_status(company: str):
    safe_company_name = "".join(x for x in company if x.isalnum())
    status_key = f"{safe_company_name}_status"
    status = analysis_status.get(status_key, "Not Started")
    return {"status": status}

@app.get("/result/{company}")
async def get_result(company: str):
    safe_company_name = "".join(x for x in company if x.isalnum())
    result_key = f"{safe_company_name}_result"
    result = analysis_status.get(result_key, "Analysis not complete or result not found")
    return {"result": result}

@app.post("/analyze/")
async def analyze_company(company_data: CompanyData, background_tasks: BackgroundTasks):
    company = company_data.company
    unique_id = str(uuid.uuid4())  # Genera un identificatore unico
    message = f"I've started the agent to work on {company}. Task ID: {unique_id}"

    background_tasks.add_task(run_analysis, company, unique_id)

    return {"message": message, "task_id": unique_id}

async def run_analysis(company, task_id):
    try:
        financial_crew = FinancialCrew(company)
        result = financial_crew.run()

        # Usa task_id per creare un nome file unico
        safe_company_name = "".join(x for x in company if x.isalnum())
        filename = f"{safe_company_name}_{task_id}_latest.txt"

        with open(filename, "w") as file:
            file.write(result)

        analysis_status[company] = "Complete"

    except Exception as e:
        analysis_status[company] = f"Failed: {e}"
        print(f"An error occurred: {e}")

