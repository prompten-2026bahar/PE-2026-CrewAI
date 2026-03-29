import asyncio
import os
import time
import json
import re
from datetime import datetime
from crewai import Crew
from config import get_llm, REPORTS_DIR, get_active_model_name
from api.store import job_store, log_queues
from agents import get_cv_parser, get_job_analyst, get_gap_detector, get_translator
from tasks import get_parse_cv_task, get_parse_job_task, get_gap_task, get_translate_task


def _generate_report_directly(llm, cv_output: str, job_output: str, job_id: str) -> str:
    """
    Small LLMs (llama3.1:8b etc.) often hallucinate tool calls instead of
    actually invoking ReportSaverTool.  After crew.kickoff() we call the LLM
    directly with a tightly-scoped prompt so we always get a real report.
    """
    prompt = f"""You are a career analyst. Using the CV data and job posting data below,
write a complete Gap Analysis report in Markdown. Output ONLY the Markdown report — 
no preamble, no explanation, no code blocks, no tool call descriptions.

=== CV DATA ===
{cv_output}

=== JOB POSTING DATA ===
{job_output}

Write the report using this exact structure:

# Gap Analysis: [Position Title]
## Compatibility Score: X/100

### Score Breakdown
| Category | Weight | Sub-score |
| --- | --- | --- |
| Hard Required Skills | 60% | X/60 |
| Soft Skills + Culture Fit | 25% | X/25 |
| Education + Certifications | 15% | X/15 |

## Skill Match Table
| Skill | Type | Status | Notes |
| --- | --- | --- | --- |
| ... | HARD_REQUIRED | 🟢/🟡/🔴 | ... |

## Strong Points 🟢
- ...

## Partial Matches 🟡
- ...

## Critical Gaps 🔴
- ...

## Hidden Expectation Alignment
...

## Strategic Recommendation
**Top 3 Strengths to Emphasize:**
1. ...
2. ...
3. ...

**Top 3 Gaps to Address Before Applying:**
1. ...
2. ...
3. ...

**Verdict:** Apply now / Prepare first / Do not apply
"""
    response = llm.call([{"role": "user", "content": prompt}])
    return response if isinstance(response, str) else str(response)

def _translate_report_directly(llm, english_content: str) -> str:
    """
    Directly translates the English Markdown report into Turkish.
    Maintains all formatting, tables, and emojis.
    """
    prompt = f"""You are an expert translator. Translate the following English Gap Analysis report 
into professional, natural Turkish. 

RULES:
- Maintain ALL Markdown formatting (headers, tables, bolding).
- Keep all emojis (🟢, 🟡, 🔴) in place.
- Translate technical terms like 'Hard Skills', 'Gap Analysis', 'Score Breakdown' 
  into their professional Turkish business equivalents.
- Output ONLY the translated Markdown. No preamble.

=== ENGLISH REPORT ===
{english_content}
"""
    response = llm.call([{"role": "user", "content": prompt}])
    return response if isinstance(response, str) else str(response)

def _sanitize_filename(text: str) -> str:
    """Removes or replaces characters that are invalid in filenames"""
    # Replace spaces and common delimiters with underscores
    s = re.sub(r'[\s\-/\\:;*?"<>|]+', '_', text)
    # Remove any other non-alphanumeric (except underscores and dots)
    s = re.sub(r'[^\w\._]', '', s)
    return s.strip('_')

def _extract_from_json(text: str, keys: list) -> dict:
    """Attempts to find and parse JSON to extract specific keys"""
    try:
        # Try to find JSON block in markdown
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return {k: data.get(k) for k in keys if k in data}
    except:
        pass
    
    # Fallback to simple regex if JSON fails
    results = {}
    for key in keys:
        pattern = rf'"{key}"\s*:\s*"([^"]+)"'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            results[key] = match.group(1)
    return results


async def run_phase1(job_id: str, cv_path: str, job_path: str, provider: str = None, model: str = None):
    job_store[job_id].status = "running"

    llm = get_llm(provider=provider, model=model)
    
    # Use selected info for filename construction
    model_name_for_file = get_active_model_name(provider=provider, model=model)

    cv_parser = get_cv_parser(llm)
    job_analyst = get_job_analyst(llm)
    gap_detector = get_gap_detector(llm)

    cv_task = get_parse_cv_task(cv_parser, cv_path)
    job_task = get_parse_job_task(job_analyst, job_path)
    gap_task = get_gap_task(gap_detector, cv_task, job_task, job_id)

    # Added Translator Agent & Task
    translator = get_translator(llm)
    translate_task = get_translate_task(translator, gap_task, job_id)

    def step_callback(agent_output):
        try:
            agent_name = getattr(agent_output, 'agent', 'Unknown Agent')
            output_text = getattr(agent_output, 'output', str(agent_output))
            output_snippet = output_text[:200] + ("..." if len(output_text) > 200 else "")
            log_queues[job_id].put_nowait({
                "type": "log",
                "data": f"[{agent_name}] {output_snippet}"
            })
        except Exception as e:
            log_queues[job_id].put_nowait({
                "type": "log",
                "data": f"[System Log] Error parsing agent output: {str(e)}"
            })

    start_time = time.time()
    try:
        crew = Crew(
            agents=[cv_parser, job_analyst, gap_detector, translator],
            tasks=[cv_task, job_task, gap_task, translate_task],
            verbose=True,
            step_callback=step_callback
        )

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, crew.kickoff)
        
        # Calculate duration
        duration_mins = round((time.time() - start_time) / 60, 2)
        duration_text = f"**Analysis Duration:** {duration_mins} minutes"
        tr_duration_text = f"**Analiz Süresi:** {duration_mins} dakika"

        # --- Dynamic Filename Construction ---
        cv_raw = getattr(cv_task.output, "raw", "") if cv_task.output else ""
        job_raw = getattr(job_task.output, "raw", "") if job_task.output else ""
        
        cv_info = _extract_from_json(cv_raw, ["NAME", "name"])
        job_info = _extract_from_json(job_raw, ["Position title", "position_title", "title"])
        
        candidate_name = cv_info.get("NAME") or cv_info.get("name") or "Candidate"
        job_title = job_info.get("Position title") or job_info.get("position_title") or job_info.get("title") or "Position"
        
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        base_name = _sanitize_filename(f"{job_title}_{candidate_name}_{timestamp_str}_{model_name_for_file}")
        report_filename = f"{base_name}.md"
        report_path = os.path.join(REPORTS_DIR, report_filename)

        log_queues[job_id].put_nowait({
            "type": "log",
            "data": f"[System] Generating readable report for {candidate_name}..."
        })

        cv_raw = getattr(cv_task.output, "raw", "") if cv_task.output else ""
        job_raw = getattr(job_task.output, "raw", "") if job_task.output else ""

        report_content = await loop.run_in_executor(
            None, _generate_report_directly, llm, cv_raw, job_raw, job_id
        )

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"<!-- Report Generated At: {timestamp} -->\n{duration_text}\n\n{report_content}")

        log_queues[job_id].put_nowait({
            "type": "log",
            "data": f"[System] English report saved: {report_filename}"
        })

        # --- Direct Translation Step ---
        tr_report_filename = f"{base_name}_tr.md"
        tr_report_path = os.path.join(REPORTS_DIR, tr_report_filename)

        log_queues[job_id].put_nowait({
            "type": "log",
            "data": "[System] Translating report to Turkish via direct LLM call..."
        })

        tr_report_content = await loop.run_in_executor(
            None, _translate_report_directly, llm, report_content
        )

        with open(tr_report_path, "w", encoding="utf-8") as f:
            f.write(f"<!-- Report Generated At: {timestamp} -->\n{tr_duration_text}\n\n{tr_report_content}")

        log_queues[job_id].put_nowait({
            "type": "log",
            "data": f"[System] Turkish report saved: {tr_report_filename}"
        })

        job_store[job_id].status = "completed"
        job_store[job_id].report_files = [report_filename, tr_report_filename]
        job_store[job_id].completed_at = time.strftime("%Y-%m-%dT%H:%M:%S")

    except Exception as e:
        job_store[job_id].status = "failed"
        job_store[job_id].error = str(e)
        if job_id in log_queues:
            log_queues[job_id].put_nowait({
                "type": "log",
                "data": f"[System] Job failed with error: {str(e)}"
            })
    finally:
        if job_id in log_queues:
            log_queues[job_id].put_nowait({"type": "done"})