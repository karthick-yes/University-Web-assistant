from unias import generate_text 
from fastapi import FastAPI, HTTPException
from mangum import Mangum

MAX_LEN = 100
app = FastAPI()
handler = Mangum(app)

@app.get("/generate_text")
async def generate_text_api(user_prompt:str, user_template:str=None, template_name:str=None):
    validate_length(user_prompt)
    text = generate_text(user_prompt, user_template, template_name)
    return {"text":text}
# uvicorn unias_api:app --reload  

def validate_length(user_prompt: str) :
    if len(user_prompt) >=  MAX_LEN:
        raise HTTPException(status_code=400, detail="Input length is more than the limit") 