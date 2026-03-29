import asyncio
from typing import Dict
from .models import JobStatus

job_store: Dict[str, JobStatus] = {}
log_queues: Dict[str, asyncio.Queue] = {}
