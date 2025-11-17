# === STUDENT INSTRUCTIONS =======================================================
# extract.py — Structured extraction with Pydantic + Ollama (gemma3:4b)
#
# Goal (10–12 min): Validate + normalize ONE course code extracted by the model.
#
# Spec you must enforce in Python (no regex):
#   • course_code is exactly 6 characters: first 3 letters (A–Z), next 3 digits (0–9)
#   • course_code must appear in ALLOWED_COURSES (list below)
#   • Accept None when no code is present; otherwise raise ValueError("invalid course code")
#
# Your tasks:
#   • TODO #1: write the field validator on CourseCode.course_code
#   • TODO #2: extend the system prompt so the model knows the 3-letter program names
#              (MAT/CSC/DSC) and the specific aliases (“CS1” → CSC170, “Calculus 1” → MAT165)
#
# When done, the output should look like:
#   • Correctly extracted (prints the code): MAT165 (twice), MAT130 (once), CSC170 (twice), DSC340 (once)
#   • Rejected as invalid: CSC340, ENG101
#   • When no course is present: prints “No course code found”
# ===============================================================================

from __future__ import annotations
from typing import Optional, Any, Dict, List
from pydantic import BaseModel, field_validator, ValidationError
from ollama import chat
import json
import re

# Allowed courses for this mini (do NOT edit)
ALLOWED_COURSES: List[str] = [
    "MAT130", "MAT165",
    "CSC170", "CSC270", "CSC370",
    "DSC270", "DSC280", "DSC340", "DSC360",
]

# -------------------- Schema --------------------

class CourseCode(BaseModel):
    course_code: Optional[str] = None  # e.g., "CSC170" or None if not present

    @field_validator("course_code", mode="before")
    @classmethod
    def trim_whitespace(cls, v: Any):
        if isinstance(v, str):
            return v.strip()
        return v

    # ===== TODO #1: FIELD VALIDATOR ============================================
    @field_validator("course_code")
    @classmethod
    def validate_course_code(cls, code: Optional[str]) -> Optional[str]:
        """
        Validate a single course code string.

        Requirements:
        - Return None unchanged if code is None (no code found).
        - Otherwise, normalize and confirm:
            * length == 6
            * first 3 characters are letters (A–Z), uppercase
            * last 3 characters are digits (0–9)
            * the final normalized code is listed in ALLOWED_COURSES
        - On any failure, raise ValueError("invalid course code").
        """
        # --- your code here ---
        if code is None:
            return None
        if not re.fullmatch(r"[A-Z]{3}\d{3}", code) or code not in ALLOWED_COURSES or len(code) != 6:
            raise ValueError("invalid course code")
        return code  # placeholder so the script runs
    # ===========================================================================

# JSON schema for Ollama structured output
JSON_SCHEMA: Dict[str, Any] = CourseCode.model_json_schema()

# -------------------- Prompt --------------------

# ===== TODO #2: SYSTEM INSTRUCTIONS (EDIT THIS STRING) =========================
SYSTEM_MSG = (
    """Extract the single Centre College course code from the user text. 
    Return ONLY a JSON object like {"course_code": "CSC170"}; use null if absent. 
    The code has 3 letters followed by 3 digits. The three-letter program names are usually
    made up of the first 3 letters of the subject name, (For example, math is MAT) or, if a program is several words, the first
    letters of the words, plus an extra "C" for class if the program only contains two words. (For example,
    Computer Science is CSC, Data Science is DSC)."""
    # Students: extend with program names (MAT/CSC/DSC) and aliases:
    # “CS1” → CSC170; “Calculus 1” → MAT165.
)
# ==============================================================================

USER_TEMPLATE = """Text: {message}
Return JSON like: {{"course_code": "DSC360"}}"""

# -------------------- LLM call --------------------

def extract_course(message: str, model: str = "gemma3:4b") -> CourseCode:
    resp = chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user",   "content": USER_TEMPLATE.format(message=message)},
        ],
        format=JSON_SCHEMA,           # ask Ollama to follow this schema
        options={"temperature": 0},   # deterministic for grading
    )
    content = resp["message"]["content"]
    print("content:", content)
    try:
        return CourseCode.model_validate_json(content)
    except ValidationError as ve:
        raise ValueError(f"Invalid structured output: {ve}") from ve
    except json.JSONDecodeError as je:
        raise ValueError(f"Malformed JSON: {je}") from je

# -------------------- Demo cases --------------------

EXAMPLES = [
    "Please enroll me in csc 340 next term.",
    "Math 165 is full",
    "What about Calc 1?",
    "You should take Mat 130 intro stats first. I think the 8AM section is still open.",
    "I think you should take CS1",
    "Take CSC 170-b at 1:50 PM.",
    "No code here, just chatting about classes.",
    "English 101 maybe?",
    "Everyone should absolutely take my Data Science 340 class. Random forests! How cool!",
]

def pretty(cc: CourseCode | None) -> str:
    if not cc or not cc.course_code:
        return "No course code found"
    return cc.course_code

def main():
    for text in EXAMPLES:
        try:
            parsed = extract_course(text)
            print(f"{text!r} -> {pretty(parsed)}")
        except ValueError:
            print(f"{text!r} -> Invalid course code")
        except Exception as e:
            print(f"{text!r} -> ERROR ({e.__class__.__name__}: {e})")

if __name__ == "__main__":
    main()
