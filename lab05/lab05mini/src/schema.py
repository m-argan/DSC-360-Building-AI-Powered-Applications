"""
src/schema.py
--------------------------------
Defines the Pydantic schema for structured course data.

INSTRUCTIONS FOR STUDENTS:
  • This file defines the schema the model will use when returning structured JSON.
  • See the lab instructions for the full list of fields and constraints.
  • Add the missing fields (between 'program' and 'tags') and any validators
    needed to enforce the rules described in the lab.
  • Use None for optional or missing values.
"""

from pydantic import BaseModel, field_validator
from typing import Optional
import re

class SectionRow(BaseModel):
    program: str
    number:str
    section:Optional[str] = None
    title:str
    credits: float
    days:Optional[str] = None
    times:Optional[str] = None
    room:Optional[str] = None
    faculty:str
    # Add your other fields here (see README)
    tags: Optional[str] = None

    @field_validator("program")
    @classmethod
    def validate_program(cls, v: str) -> str:
        """Program must be three uppercase letters like CSC or MAT."""
        if not re.fullmatch(r"[A-Z]{3}", v):
            raise ValueError("program must be three uppercase letters")
        return v
    
    @field_validator("number")
    @classmethod
    def validate_number(cls, v: str) -> str:
        """Number must be three digits, optionally followed by the letter l."""
        if not re.fullmatch(r"\d{3}[L]?", v):
            raise ValueError("number must be three digits, optionally followed by a letter")
        return v
    
    @field_validator("section")
    @classmethod
    def validate_section(cls, v: Optional[str]) -> Optional[str]:
        """Section, if present, must be a a single letter a-d letter."""
        if v is None:
            return None
        if not re.fullmatch(r"[a-d]", v):
            raise ValueError("section must be a single letter a-d")
        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        print("title:",v)
        """Title must be a non-empty string"""
        if v is None:
            raise ValueError("title must be a non-empty string")
        return v
    
    @field_validator("credits")
    @classmethod
    def validate_credits(cls, v: float) -> float:
        """Credits must be a number between 0.5 and 4.0."""
        if not (0.5 <= v <= 4.0):
            raise ValueError("credits must be between 0.5 and 4.0")
        return v
    
    @field_validator("days")
    @classmethod
    def validate_days(cls, v: Optional[str]) -> Optional[str]:
        print(repr(v), repr(v.strip()))
        '''Days should either be ------ or -M-W-F-, or --T-R--'''
        if v.strip() == '-------':
            print("its a match!")
            return None
        elif v.strip() != ('-M-W-F-') or ('--T-R--') or ('--T----') or ('----R--') or ('-M-----') or ('-----F-') or ('-M--W--') or ('--W--F-') or ('---W---') or ('------'):
            raise ValueError("days should contain 7 elements representing days of the week, with dashes for no class and letters for class days")
        return v.strip()
    
    @field_validator("times")
    @classmethod
    def validate_times(cls, v: Optional[str]) -> Optional[str]:
        '''Times should either be TBA or in the format HH:MM'''
        if v == "TBA":
            return None
        elif not re.fullmatch(r"^\d{1,2}:\d{2}-\d{1,2}:\d{2}(?:AM|PM)$", v):
            raise ValueError("times should be in the format HH:MM AM/PM")
        return v
    

    # Add other validators here as needed
