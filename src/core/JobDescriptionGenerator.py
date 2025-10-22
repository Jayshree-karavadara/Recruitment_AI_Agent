import os
import json
from dotenv import load_dotenv
from llm import LLMHandler  # Uses your generalized LLM interface
from text_extraction import extract_job_description_text


class JobDescriptionGenerator:

    def __init__(self, temperature: float = 0.2):
        load_dotenv()
        self.llm = LLMHandler(temperature=temperature)

    def _build_prompt(self, combined_text: str) -> tuple:

        system_prompt = (
            "You are an expert HR assistant and job description specialist. "
            "Your job is to read and generate well-structured, professional, and ATS-optimized job descriptions. "
            "Output must be in pure JSON format — no markdown, commentary, or additional text."
        )

        user_prompt = f"""
        Using the following information provided by the user or extracted from the uploaded file,
        generate a detailed and complete **job description** in structured JSON format with the following fields:

        {{
            "data": {{
                "job_title": " ",
                "company_name": " ", 
                "location": " ",
                "employment_type": "Full-time/Part-time/Contract",
                "industry": " ",
                "years_of_experience": "n+ years / fresher / intern",
                "must_have_skills": ["skill1", "skill2"],
                "nice_to_have_skills": ["skillA", "skillB"],
                "roles_and_responsibilities": ["responsibility1", "responsibility2"],
                "education_requirements": ["degree or certification"],
                "salary_range": "optional",
                "job_summary": "2–3 line professional overview"
            }}
        }}

        Ensure:
        - No assumptions beyond the given context.
        - If a field is missing, keep it empty (" " or []).
        - Maintain a consistent and clean JSON schema.
        - Focus on clarity and ATS-friendly phrasing.

        User and extracted input:
        {combined_text}
        """

        return system_prompt, user_prompt

    async def generate(self, file=None, text=None):
        user_input_manual_text, jd_file_text = await extract_job_description_text(file, text)

        combined_text = f"""
        User Provided Input:
        {user_input_manual_text or ''}
        
        Extracted JD File Text:
        {jd_file_text or ''}
        """

        system_prompt, user_prompt = self._build_prompt(combined_text)
        jd_json = self.llm.get_llm_output(system_prompt, user_prompt)
        return jd_json
















# import json
# import re
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
# import os
# from dotenv import load_dotenv
# from text_extraction import extract_job_description_text

# def get_formated_jd(file, text):
#     user_input_manual_text, jd_file_text = extract_job_description_text(file, text)
#     jd_dict = get_formated_jd_report(user_input_manual_text, jd_file_text)
#     print()
#     print(f"jd_dict : -------------------- {jd_dict}")
#     print()
#     return jd_dict

# load_dotenv() 
# def get_formated_jd_report(user_input_manual_text: str, jd_file_text: str):
#     """
#     Takes raw job description text from manual input and/or extracted file text,
#     and returns a structured JSON format with detailed fields.
#     Works with both OpenAI (GPT) and Gemini (Google Generative AI) keys.
#     """

#     # Combine both text inputs
#     combined_text = f"""
#     User Provided Input:
#     {user_input_manual_text}

#     Extracted JD File Text:
#     {jd_file_text}
#     """

#     # ---- Detect provider ----
#     openai_key = os.getenv("OPENAI_API_KEY")
#     google_key = os.getenv("GOOGLE_API_KEY")

#     if openai_key:
#         model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
#         llm = ChatOpenAI(model=model_name, temperature=0.2)
#         provider = "openai"
#     elif google_key:
#         model_name = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
#         llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.2)
#         provider = "gemini"
#     else:
#         raise ValueError("No API key found. Please set either OPENAI_API_KEY or GOOGLE_API_KEY.")

#         # ---- Prompt ----
#         # ---- Prompt ----
    # prompt = [
    #     SystemMessage(content=(
    #         "You are an expert HR assistant and ATS optimization specialist. "
    #         "Read the provided job description carefully and extract structured information in pure JSON format. "
    #         "Do NOT include markdown, explanations, or text outside the JSON. "
    #         "Focus on the most relevant details for resume-job matching and ATS parsing."
    #     )),
    #     HumanMessage(content=f"""
    #     From the following job description text, extract all possible structured information 
    #     into a JSON with the following **mandatory** keys under "data":

    #     ○ Job Title  
    #     ○ Years of Experience  
    #     ○ Must-have Skills (comma-separated)  
    #     ○ Company Name  
    #     ○ Employment Type (Full-time, Part-time, etc.)  
    #     ○ Industry  
    #     ○ Location  

    #     Include **additional fields only if** they provide value for ATS optimization or resume matching 
    #     (for example: roles_and_responsibilities, education_requirements, salary_range, job_summary, nice_to_have_skills).

    #     **Do not mention any assumption if information is not giving like company name or location...**

    #     Output Example:
    #     {{
    #       "data": {{
    #         "job_title": " ",
    #         "years_of_experience": "n+ years/n to m years/fresher/intern..",
    #         "must_have_skills": ["skill1", "skill2", "skill3"],
    #         "company_name": " ",
    #         "employment_type": "Full-time/Partime/freelancer...",
    #         "industry": "IT/farma/agriculture/banking...",
    #         "location": " ",
    #         "other": {{"roles_and_responsibilities": ["Develop AI agents using LLM", "Implement RAG workflows", "xyz"]}}
    #       }}
    #     }}

    #     Only output valid JSON — no text, explanations, or markdown formatting.

    #     Job Description Text:
    #     {combined_text}
    #     """)
    # ]

#     # ---- Call Model ----
#     response = llm.invoke(prompt)
#     content = response.content.strip()

#     # ---- Parse JSON ----
#     try:
#         jd_json = json.loads(content)
#     except json.JSONDecodeError:
#         json_match = re.search(r'\{.*\}', content, re.DOTALL)
#         if json_match:
#             jd_json = json.loads(json_match.group(0))
#         else:
#             raise ValueError(f"Model returned invalid JSON: {content}")

#     return jd_json

# def get_formated_jd(file, text):
#     user_input_manual_text, jd_file_text = extract_job_description_text(file, text)
#     jd_dict = get_formated_jd_report(user_input_manual_text, jd_file_text)
#     print()
#     print(f"jd_dict : -------------------- {jd_dict}")
#     print()
#     return jd_dict

    

