
from crew.crew import FinancialCrew
import os
import uuid
# Altri import necessari per le tue task...
from celery_app import celery_app
import redis
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)
# Configura il client Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@celery_app.task(bind=True)
def run_analysis(self, company):
    # Crea una chiave unica per la cache basata sul nome dell'azienda
    cache_key = f"analysis_result:{company}"
    # Prova a recuperare il risultato dalla cache
    cached_result = redis_client.get(cache_key)
    if cached_result is not None:
        # Se il risultato è presente in cache, deserializzalo e restituiscilo
        logger.info(f"Restituito risultato da cache per {company}")
        return cached_result.decode("utf-8")
    
    # Se non è presente in cache, procedi con l'analisi
    try:
        financial_crew = FinancialCrew(company)
        result = financial_crew.run()
        # Salva il risultato in cache con scadenza di 24 ore (86400 secondi)
        redis_client.setex(cache_key, 86400, result)
        return result
    except Exception as e:
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        raise e


# @celery_app.task(bind=True)
# def run_analysis(self, company):
#     try:
#         financial_crew = FinancialCrew(company)
#         result = financial_crew.run()
#         return result  # Il risultato dell'analisi
#     except Exception as e:
#         self.update_state(state='FAILURE', meta={'exc': str(e)})
#         raise e


# @celery_app.task(bind=True)
# def run_analysis(self, company):
#     task_id = str(uuid.uuid4())
#     try:
#         financial_crew = FinancialCrew(company)
#         result = financial_crew.run()
#         return result  # Il risultato dell'analisi
#     #     safe_company_name = "".join(x for x in company if x.isalnum())
#     #     filename = f"{safe_company_name}_{task_id}_latest.txt"
#     #     with open(filename, "w") as file:
#     #         file.write(result)
#     #     return {"task_id": task_id, "status": "Complete"}
#     except Exception as e:
#         return {"task_id": task_id, "status": "Failed", "error": str(e)}
