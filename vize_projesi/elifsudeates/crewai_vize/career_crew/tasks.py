from crewai import Task
from tools import file_reader_tool, report_saver_tool

def get_parse_cv_task(agent, cv_path: str):
    return Task(
        description=(
            f"Read the CV from: {cv_path}\n\n"
            "Extract and structure ALL of:\n"
            "- NAME: The full name of the candidate (very important for naming the report)\n"
            "- HARD SKILLS: name, estimated proficiency level with reasoning\n"
            "- SOFT SKILLS: explicit + inferred from experience descriptions\n"
            "- EXPERIENCE: per role → company, title, duration, seniority, 3-bullet summary\n"
            "- EDUCATION: degree, institution, year\n"
            "- CERTIFICATIONS and ACHIEVEMENTS\n"
            "- RED FLAGS: employment gaps, vague descriptions, missing sections,\n"
            "  no measurable achievements, no GitHub/LinkedIn\n\n"
            "Return as structured JSON."
        ),
        expected_output="Complete structured JSON with candidate name and detailed CV data",
        agent=agent
    )

def get_parse_job_task(agent, job_path: str):
    return Task(
        description=(
            f"Read the job posting from: {job_path}\n\n"
            "LAYER 1 - EXPLICIT:\n"
            "- Position title\n"
            "- Required skills labeled: HARD_REQUIRED / HARD_PREFERRED / SOFT_REQUIRED\n"
            "- Experience and education requirements\n"
            "- Location, remote policy, salary if stated\n\n"
            "LAYER 2 - HIDDEN:\n"
            "- Company culture (startup vs corporate, tone analysis)\n"
            "- Unstated expectations (what does this role REALLY need?)\n"
            "- Interview red flags if any\n"
            "- ATS keywords: words and phrases candidate MUST use to pass screening\n\n"
            "Return as structured JSON including an ats_keywords array."
        ),
        expected_output="Structured JSON with explicit requirements and hidden signals",
        agent=agent
    )

def get_gap_task(agent, cv_task, job_task, job_id: str):
    return Task(
        description=(
            "You have CV data and job posting data from previous agents.\n\n"
            "STEP 1 - SKILL MATCHING:\n"
            "For every required skill, label as:\n"
            "🟢 STRONG MATCH: candidate clearly has it at required level\n"
            "🟡 PARTIAL MATCH: related but not exact fit\n"
            "🔴 CRITICAL GAP: missing or severely underdeveloped\n\n"
            "STEP 2 - SCORE (0-100):\n"
            "Hard required skills: 60%\n"
            "Soft skills + culture fit: 25%\n"
            "Education + certs: 15%\n"
            "Show sub-scores and calculation.\n\n"
            "STEP 3 - HIDDEN EXPECTATION MATCH:\n"
            "How well does the candidate align with unstated culture signals?\n\n"
            "STEP 4 - STRATEGIC ASSESSMENT:\n"
            "- Top 3 strengths to emphasize\n"
            "- Top 3 gaps to address before applying\n"
            "- Verdict: Apply now / Prepare first / Do not apply\n\n"
            f"Format as Markdown report with tables. When the report is complete, call ReportSaverTool\n"
            f"with these exact arguments: filename='01_gap_analysis', job_id='{job_id}', content=<the full Markdown report text>.\n\n"
            "Report structure:\n"
            "# Gap Analysis: [Position]\n"
            "## Compatibility Score: X/100\n"
            "## Skill Match Table\n"
            "## Strong Points 🟢\n"
            "## Partial Matches 🟡\n"
            "## Critical Gaps 🔴\n"
            "## Hidden Expectation Alignment\n"
            "## Strategic Recommendation"
        ),
        expected_output="Complete Markdown gap analysis saved to reports/",
        context=[cv_task, job_task],
        agent=agent
    )

def get_translate_task(agent, context_task, job_id: str):
    return Task(
        description=(
            "Translate the provided career report from English to Turkish.\n\n"
            "Ensure that all technical terms (e.g. 'Hard Skills', 'Gap Analysis') "
            "are translated into their appropriate, professional Turkish equivalents.\n"
            "Maintain the Markdown formatting (tables, bolding, emojis) exactly as in the original.\n\n"
            "Output the translated report as a clean Markdown string."
        ),
        expected_output="A professionally translated Turkish version of the Gap Analysis report.",
        context=[context_task],
        agent=agent
    )