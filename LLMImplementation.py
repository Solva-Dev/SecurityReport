import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

domain_data = {
    "domain": "example.com",
    "ns": ["ns1.example.com", "ns2.example.com"],
    "mx": ["mail.example.com", "mx2.example.com"],
    "technologies": ["WordPress 6.4", "Apache 2.4.58", "OpenSSL 1.1.1"]
}

with open("domain_data.json", "w") as f:
    json.dump(domain_data, f, indent=2)

prompt = f"""
Given the following JSON data:

{json.dumps(domain_data, indent=2)}

Search for any related CVEs (Common Vulnerabilities and Exposures)
based on the listed NS, MX, and technologies. The final report must include
a description of each technology and its known vulnerabilities. The report should be
at most 1 pragraph long for each technology. After that create a listing structure
describing potential vulnerabilities for the domain {domain_data['domain']} which 
belongs to the company Aprender-Salud. Each vulnerability mentioned should be listed 
in an item structure with its CVE identifier. At the end of the report include 
a suggestion section with recommendations to mitigate the identified vulnerabilities 
in a paragraph structure. Generate the report with an HTML format.
"""
load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("No se encontró la variable GEMINI_API_KEY en el archivo .env")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content(prompt)

file_name = "report.txt"
try:
    with open(file_name, "w") as file:
        file.write(response.text)
    print(f"String successfully saved to '{file_name}'")
except IOError as e:
    print(f"Error saving string to file: {e}")


