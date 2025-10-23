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
        """Title must be a non-empty string"""
        if v is None:
            raise ValueError("title must be a non-empty string")
        return v
    
    @field_validator("credits")
    @classmethod
    def validate_credits(cls, v: float) -> float:
        """Credits must be a number between 0.5 and 4.0."""
        if not (0 <= v <= 4.0):
            raise ValueError("credits must be between 0.5 and 4.0")
        return v
    
    @field_validator("days")
    @classmethod
    def validate_days(cls, v: Optional[str]) -> Optional[str]:
        """Days should either be ------- or a string like -M-W-F- representing days of the week."""
        if not v:
            return None
        cleaned = ''.join(v.split()).replace('\u200b', '').replace('\xa0', '')
        print("cleaned repr:", repr(cleaned))

        valid_patterns = {'-M-W-F-', '--T-R--', '--T----', '---R---', '-M-----', '-----F-', '-M--W--', '--W--F-', '---W---', '-------'}
        if cleaned == '-------':
            return None

        if cleaned not in valid_patterns:
            raise ValueError("days should contain 7 elements representing days of the week, with dashes for no class and letters for class days")
        return cleaned
    
    @field_validator("times")
    @classmethod
    def validate_times(cls, v: Optional[str]) -> Optional[str]:
        '''Times should either be TBA or in the format HH:MM'''
        if v == "TBA":
            return None
        elif not re.fullmatch(r"^\d{1,2}:\d{2}-\d{1,2}:\d{2}(?:AM|PM)$", v):
            raise ValueError("times should be in the format HH:MM AM/PM")
        return v
    
    @field_validator("room")
    @classmethod
    def validate_room(cls, v: Optional[str]) -> Optional[str]:
        '''Rooms should be a capitalized word followed by a space and a number.'''
        if v == "TBA" or v is None:
            return None
        elif not re.fullmatch(r"[A-Z]*\s\d+\b", v):
            raise ValueError("Rooms should be a capitalized word followed by a space and a number.")
        return v
    
    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: Optional[str]) -> Optional[str]:
        '''Tags, if they are present, should be a comma-separated list of words/numbers.'''
        if v is None:
            return None
        if not re.fullmatch(r"^\w+(?:,\s*\w+)*$", v):
            raise ValueError("Tags should be words, seperated by commas")
        return v
    # Add other validators here as needed
