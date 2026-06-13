from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="techcook/static"), name="static")


@app.get("/")
def home():
    return FileResponse("techcook/templates/index.html")


# ✅ GROQ CLIENT
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ✅ REQUEST MODEL
class IngredientRequest(BaseModel):
    ingredients: str
    style: str


# ✅ AI FUNCTION
def generate_recipe(ingredients: str, style: str):

    prompt = f"""
You are an expert chef AI.

Create a detailed recipe using the given inputs.

Ingredients:
{ingredients}

Cuisine:
{style}

Return EXACT format:

Recipe Name:
Preparation Time:

Ingredients:
- item

Steps:
1. step

Chef Tips:
- tip

Nutritional Info:
Calories: number
Protein: grams
Carbohydrates: grams
Fat: grams

Rules:
- Do NOT use markdown (** or *)
- Always include ALL sections
- Always estimate nutrition values
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# ✅ API ENDPOINT
@app.post("/generate-recipe")
def generate(data: IngredientRequest):

    try:
        recipe = generate_recipe(data.ingredients, data.style)
        return {"recipe": recipe}

    except Exception as e:
        return {"recipe": f"ERROR: {str(e)}"}