from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional

from src.core.document_processor import DocumentProcessor
from src.core.evaluation_engine import EvaluationEngine
from src.llm import get_llm_client
from src.prompts.manager import PromptManager
from pathlib import Path

router = APIRouter()

# Build a robust path to the templates directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Renders the index.html template for the initial page load."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/evaluate", response_class=HTMLResponse)
async def evaluate(
    request: Request,
    resume_files: List[UploadFile] = File(...),
    jd_file: Optional[UploadFile] = File(None),
    jd_text: Optional[str] = Form(None),
    job_title: Optional[str] = Form(None),
    experience: Optional[str] = Form(None),
    skills: Optional[str] = Form(None),
    company_name: Optional[str] = Form(None),
    employment_type: Optional[str] = Form(None),
    industry: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
):
    """Evaluates resumes against a job description and generates emails."""
    llm_client = get_llm_client()
    document_processor = DocumentProcessor()
    prompt_manager = PromptManager(BASE_DIR / "config/prompts.yaml")
    evaluation_engine = EvaluationEngine(
        llm_client, document_processor, prompt_manager
    )

    jd_generation_details = {
        "job_title": job_title,
        "experience": experience,
        "skills": skills,
        "company_name": company_name,
        "employment_type": employment_type,
        "industry": industry,
        "location": location,
    }

    results = await evaluation_engine.evaluate_candidates(
        resume_files=resume_files,
        jd_file=jd_file,
        jd_text=jd_text,
        jd_generation_details=jd_generation_details,
    )

    interview_email = None
    rejection_email = None
    role = job_title or "the position"

    if results and "error" not in results[0]:
        top_candidate_name = results[0]["filename"].split('.')[0]
        interview_email = llm_client.generate_interview_email(
            candidate_name=top_candidate_name, role=role
        )
        rejection_email = llm_client.generate_rejection_email(
            candidate_name="Candidate", role=role
        )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "results": results,
            "interview_email": interview_email,
            "rejection_email": rejection_email,
        },
    )
