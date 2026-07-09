import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class GeminiExtractor:

    def __init__(self):
        pass

    def extract(self, document_text):

        prompt = f"""
You are an expert AI system that extracts metadata from rental agreements.

Your task is to carefully read the agreement and extract ONLY the following fields.

Return ONLY valid JSON.

VERY IMPORTANT

1. Aggrement Value

This means ONLY the MONTHLY RENT.

DO NOT calculate yearly rent.

DO NOT calculate total agreement value.

DO NOT multiply by the number of months.

Examples

Monthly Rent = Rs. 12000

Return

12000

Monthly Rent = Rs.6500

Return

6500


2. Aggrement Start Date

Return the agreement commencement date.

Format:

DD.MM.YYYY

Examples

1st April 2008

Return

01.04.2008

20th May 2007

Return

20.05.2007


3. Aggrement End Date

Return the agreement ending date.

Format:

DD.MM.YYYY


4. Renewal Notice (Days)

Return ONLY the number.

Examples

30

60


5. Party One

Party One is ALWAYS the Owner or Lessor.

Return ONLY the legal person's or company's name.

DO NOT include address.

DO NOT include titles.

DO NOT include descriptions.


6. Party Two

Party Two is ALWAYS the Tenant or Lessee.

Return ONLY the legal person's or company's name.

DO NOT include address.

DO NOT include titles.

DO NOT include descriptions.

If any field is unavailable, return an empty string.

Return ONLY this JSON:

{{
    "Aggrement Value":"",
    "Aggrement Start Date":"",
    "Aggrement End Date":"",
    "Renewal Notice (Days)":"",
    "Party One":"",
    "Party Two":""
}}

Document:

{document_text}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        result = response.text.strip()

        # Remove markdown if Gemini returns it
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        return json.loads(result)