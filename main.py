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
    # Immediate response to user
    company = company_data.company
    message = f"I've started the agent to work on {company}"

    # Add the actual work to background tasks
    background_tasks.add_task(run_analysis, company)

    return {"message": message}

async def run_analysis(company):
    analysis_status[company] = "In Progress"
    try:
        financial_crew = FinancialCrew(company)
        result = financial_crew.run()

        # Ensure valid filename and handle file writing appropriately
        safe_company_name = "".join(x for x in company if x.isalnum())
        filename = f"{safe_company_name}_latest.txt"

        # Consider using an async file writer if you're handling large files or a high load
        with open(filename, "w") as file:
            file.write(result)
        analysis_status[company] = "Complete"

    except Exception as e:
        # Add logging or more sophisticated error handling here
        print(f"An error occurred: {e}")

