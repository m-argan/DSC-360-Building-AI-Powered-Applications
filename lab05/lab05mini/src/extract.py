"""
Part 1 — Structured Extraction

This script converts unstructured course text (e.g., “CSC 170 Programming and
Problem Solving 4 a T. Allen 1:50–3:50PM -M-W-F- OLIN 208”) into structured,
validated rows using a Pydantic model defined in schema.py.

In Part 1, your task is to:

- Write code in `extract_structured_record()` that uses your local LLM
  (through Ollama) to extract structured data following the schema.

- Pass SectionRow.model_json_schema() as the `format` argument when calling
  the model so it returns a valid JSON object.

- Parse the model output, validate it with SectionRow(**data), and return
  the resulting object.

For now, the provided stub runs end-to-end with a placeholder that returns
blank fields. This allows you to test the pipeline and see how the validation
and scoring work before adding your model logic.
"""

import csv
import json
import ollama
from pydantic import ValidationError
from schema import SectionRow
MODEL = "gemma3:12b"

def extract_structured_record(line: str) -> SectionRow:
    #print("ll",line)
    """
    Use an LLM to extract structured data for one course listing.

    TODO:
      - Write a prompt that tells the model what to extract.
      - Call your chosen Ollama model (e.g., gemma3:4b, granite3:2b, etc.).
      - Pass SectionRow.model_json_schema() so the model knows the expected format.
      - Parse the model's JSON response.
      - Validate the result with SectionRow(**data).
    """
    schema = SectionRow.model_json_schema()
    SYSTEM_MSG = f"""extract structured course data from the following line according to the format, and respond in JSON format. The only fields which will have dashes
    is "days", which will be formatted using letters and dashes, letters (either M,W,F,T or R) to represent days of the week when class is being taught, 
    and dashes to represent days when class is not being taught. For example, -M-W-F- means class is being taught only on Monday, Wednesday, and Friday. the "room" field
    will be comprised of a building code, in all caps, and a room number. The room should always end with a number, anything that comes after the room number should be considered as a tag.
    Here is an example of a line you might receive: 'THR 111 Lighting Practicum 1.0 A. Kuznetsova 8:00-9:00AM ------- OLIN 128', and here is an example of 
    a properly formatted response: 
    {{'program': 'THR', 
    'number': '111',
    'section': None,
    'title': 'Lighting Practicum',
    'credits': 1.0,
    'days': -------,
    'times': 8:00-9:00AM,
    'room': OLIN 128,
    'faculty': 'A. Kuznetsova',
    'tags': None}}. Here is another example line: CHE 132L CHE 132 Lab 0 a E. Wachter 8:00-11:00AM --T---- YOUN 202. Here is the properly formatted response for that line:
    {{'program': 'CHE', 
    'number': '132L',
    'section': a,
    'title': 'CHE 132 Lab',
    'credits': 0.0,
    'days': --T----,
    'times': 8:00-11:00AM,
    'room': YOUN 202,
    'faculty': 'E. Wachter',
    'tags': None}}. 
    A proper JSON response must include all fields from the following schema:{schema}. The JSON response must include program, number, section, title, credits, 
    days, times, room, faculty and tags, IN THAT ORDER. If section is not present, include it in the response and set it to null."""

    USER_TEMPLATE = 'You have been provided a line of course information which is formatted in the following way: program, number, title, credits, section' \
    'faculty, times, days, room, tags. Extract structured course data from this line according to the format, and provide the response in JSON format:'+ line+'.'
    resp = ollama.chat(
    model=MODEL,
    messages=[
        {"role": "system", "content": SYSTEM_MSG},  # global variable defined above
        {"role": "user", "content": USER_TEMPLATE.format(message=line)}, # substitutes for {message} in variable USER_TEMPLATE defined above
    ],
    format=schema,            # Ask for structured output that matches our schema
    options={"temperature": 0},    # Deterministic extraction for labs/grading
    )

    content = resp["message"]["content"]
    data = json.loads(content)
    #print("response", content)
    '''
    response = ollama.chat(messages = [{"role" : "user", "content" : prompt}], model = MODEL, format = schema)

    content = response["message"]["content"]
    data = json.loads(content)
    print("response", response)
'''
    # The placeholder below produces an "empty" valid record.
    # It lets you test the pipeline without errors,
    # but it will score 0.00 on the evaluation.
    '''
    data = {
        "program": "",
        "number": "",
        "section": "",
        "title": "",
        "credits": 0.0,
        "days": "",
        "times": "",
        "room": "",
        "faculty": "",
        "tags": None,
    }'''
    return SectionRow(**data)


def process_file(in_path: str, out_path: str):
    """
    Read unstructured text from in_path, extract structured data for each line,
    and write results to out_path as a semicolon-delimited CSV.
    """
    with open(in_path, encoding="utf-8") as fin, open(out_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.writer(fout, delimiter=";")
        
        # Write CSV header based on schema fields
        writer.writerow(SectionRow.model_fields.keys())
        failures = []
        count = 0
        #limit = 4  # set a small limit for debugging; change to -1 for no limit ...

        for line in fin:
            print("line number ",count+1,": ",line)
            if not line.strip():
                continue

            #if count >= limit:  # or you could just remove these two lines for no limit
            #    break

            try:
                record = extract_structured_record(line)
                #print("record:", record)
                # Optional: view the validated record for debugging
                #print("worked!",record.model_dump_json(indent=2))

                writer.writerow(record.model_dump().values())

            except ValidationError as e:
                print("Validation test failed — skipping this line.")
                print(f"  Input: {line.strip()}")
                failures.append((count))
                for err in e.errors():
                    loc = ".".join(str(x) for x in err["loc"])
                    msg = err["msg"]
                    val = err.get("input_value", "")
                    print(f"    Field: {loc} | Problem: {msg} | Value: {val}")

            except Exception as e:
                print(f"Unexpected error — skipping line: {line.strip()}")
                print(f"  {type(e).__name__}: {e}")

            count += 1
        print(f"Processed {count} lines with {len(failures)} failures.")
        print("Failed line numbers:", failures)

if __name__ == "__main__":
    # Process training data (Part 1)
    #process_file("raw/training.txt", "out/sections_train.csv")

    # Later, after refinement, uncomment to process the test set (Part 2)
    process_file("raw/testing.txt", "out/sections_test.csv")
