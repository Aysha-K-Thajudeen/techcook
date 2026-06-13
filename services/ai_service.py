import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


prompt = f"""
You are an expert chef.

Return the recipe in this EXACT format. Do NOT skip any section.

Recipe Name: <name>

Preparation Time: <time>

Ingredients:
- item 1
- item 2

Steps:
1. step one
2. step two

Chef Tips:
- tip 1
- tip 2

Nutritional Info:
Calories: <number>
Protein: <number>
Carbohydrates: <number>
Fat: <number>

Rules:
- Always include Nutritional Info section
- Always estimate values if not provided
- Do NOT use ** or markdown symbols
- Keep format clean and consistent
"""