import os
import uuid
import asyncio
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks
from sse_starlette.sse import EventSourceResponse

import httpx
from config import INPUTS_DIR, REPORTS_DIR, LLM_PROVIDER, GEMINI_MODELS, OLLAMA_BASE_URL, get_llm
from .models import Phase1Request, JobStatus, ReportResponse, ConnectionTestRequest, LLMModelsResponse, LLMModel
from .store import job_store, log_queues
from crew_runner import run_phase1

router = APIRouter()

@router.post("/phase1", response_model=JobStatus)
async def start_phase1(request: Phase1Request, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    
    cv_path = os.path.join(INPUTS_DIR, f"cv_{job_id}.txt")
    job_path = os.path.join(INPUTS_DIR, f"job_{job_id}.txt")
    
    # Save inputs
    with open(cv_path, "w", encoding="utf-8") as f:
        f.write(request.cv_text)
    with open(job_path, "w", encoding="utf-8") as f:
        f.write(request.job_text)
        
    # Initialize store
    job_store[job_id] = JobStatus(
        job_id=job_id,
        status="pending",
        phase=1,
        created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        report_files=[]
    )
    log_queues[job_id] = asyncio.Queue()
    
    # Background task
    background_tasks.add_task(
        run_phase1, 
        job_id, 
        cv_path, 
        job_path, 
        request.llm_provider, 
        request.model_name
    )
    
    return job_store[job_id]

@router.get("/llm/models", response_model=LLMModelsResponse)
async def list_llm_models(provider: str):
    p = provider.lower()
    models = []
    
    if p == "ollama":
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    for m in data.get("models", []):
                        models.append(LLMModel(name=m["name"], details=m.get("details", {}).get("parameter_size")))
        except Exception as e:
            # Fallback or empty if Ollama is unreachable
            pass
    elif p == "gemini":
        for m in GEMINI_MODELS:
            models.append(LLMModel(name=m))
            
    return LLMModelsResponse(provider=provider, models=models)

@router.post("/llm/test")
async def test_llm_connection(request: ConnectionTestRequest):
    try:
        llm = get_llm(provider=request.provider, model=request.model, api_key=request.api_key)
        # Try a very small ping/prompt
        loop = asyncio.get_running_loop()
        # Use a minimal prompt to test connectivity
        response = await loop.run_in_executor(None, llm.call, [{"role": "user", "content": "hi"}])
        if response:
            return {"status": "success", "message": "Connection successful"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    return {"status": "error", "message": "Unknown error during connection test"}

@router.get("/status/{job_id}", response_model=JobStatus)
async def get_status(job_id: str):
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_store[job_id]

@router.get("/reports")
async def list_reports():
    reports = []
    if os.path.exists(REPORTS_DIR):
        for filename in os.listdir(REPORTS_DIR):
            if filename.endswith(".md"):
                filepath = os.path.join(REPORTS_DIR, filename)
                size_kb = round(os.path.getsize(filepath) / 1024, 2)
                created_at = datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%Y-%m-%dT%H:%M:%S")
                reports.append({
                    "filename": filename,
                    "size_kb": size_kb,
                    "created_at": created_at
                })
    return reports

@router.get("/reports/{filename}", response_model=ReportResponse)
async def get_report(filename: str):
    filepath = os.path.join(REPORTS_DIR, filename)
    if not os.path.exists(filepath) or not filename.endswith(".md"):
        raise HTTPException(status_code=404, detail="Report not found")
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    created_at = datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%Y-%m-%dT%H:%M:%S")
    return ReportResponse(filename=filename, content=content, created_at=created_at)

@router.get("/logs/{job_id}")
async def get_logs(job_id: str):
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job_id not in log_queues:
        raise HTTPException(status_code=404, detail="Logs not found for this job")
        
    async def event_generator():
        queue = log_queues[job_id]
        try:
            while True:
                log_entry = await queue.get()
                if log_entry.get("type") == "done":
                    yield {"event": "done", "data": "Job completed"}
                    break
                yield {"event": "log", "data": log_entry.get("data", "")}
        except asyncio.CancelledError:
            # Client disconnected
            pass

    return EventSourceResponse(event_generator())

@router.get("/health")
async def get_health():
    return {
        "status": "ok",
        "llm_provider": LLM_PROVIDER,
        "version": "1.0.0"
    }
