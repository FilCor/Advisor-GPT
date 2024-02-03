
from crew.crew import FinancialCrew
import os
import uuid
# Altri import necessari per le tue task...
from from celery_app import celery_app


@celery_app.task(bind=True)
def run_analysis(self, company):
    task_id = str(uuid.uuid4())
    try:
        financial_crew = FinancialCrew(company)
        result = financial_crew.run()
        safe_company_name = "".join(x for x in company if x.isalnum())
        filename = f"{safe_company_name}_{task_id}_latest.txt"
        with open(filename, "w") as file:
            file.write(result)
        return {"task_id": task_id, "status": "Complete"}
    except Exception as e:
        return {"task_id": task_id, "status": "Failed", "error": str(e)}
