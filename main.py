from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from datetime import datetime
from textwrap import dedent
from dotenv import load_dotenv
from pydantic import BaseModel, constr, validator
load_dotenv()
from crew.crew import FinancialCrew
from tasks import run_analysis
from celery.result import AsyncResult
from celery_app import celery_app
from celery.utils.log import get_task_logger
import re
import requests
from aws_utilis import get_aws_parameter

logger = get_task_logger(__name__)
# Inizializza il limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
openai_api_key = get_aws_parameter("OPENAI_API_KEY", decrypt=True)

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

# Registra il gestore degli errori per le violazioni del rate limit
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class CompanyData(BaseModel):
    company: str
     # Validator per sanificare l'input dell'azienda
    @validator('company')
    def sanitize_company_name(cls, value):
        # Rimuovi script, tag HTML e contenuti potenzialmente pericolosi
        sanitized_value = re.sub(r'<[^>]*?>', '', value)  # Rimuove i tag HTML
        sanitized_value = re.sub(r'[^\w\s]', '', sanitized_value)  # Rimuove caratteri speciali, mantenendo solo lettere, numeri, underscore e spazi
        # Aggiungi ulteriori regole di sanificazione se necessario
        return sanitized_value.strip()


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze/")
@limiter.limit("2/minute")  # Per esempio, limita a 5 richieste al minuto per IP
async def analyze_company(request: Request, company_data: CompanyData):
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
            result = task_result.get()  # Usa .get() con parentesi e specifica un timeout se necessario
            print(f"Task {task_id} completed with result: {result}")  # Log per debug
            return {"result": result}
        except Exception as e:
            print(f"Error retrieving result for task {task_id}: {e}")  # Log per debug
            return {"error": str(e)}
    else:
        print(f"Task {task_id} is still in progress.") # Log per debug
    return {"result": "Analysis not complete or task not found"}

@app.get("/openai-usage")
async def get_openai_usage():
    openai_api_key = get_aws_parameter("OPENAI_API_KEY", decrypt=True)
    response = requests.get(
        "https://api.openai.com/v1/usage",
        headers={"Authorization": f"Bearer {openai_api_key}"}
    )
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve OpenAI usage information"}

