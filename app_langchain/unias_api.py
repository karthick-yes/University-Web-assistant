from unias import generate_text, validate_input_length
from fastapi import FastAPI, HTTPException
from mangum import Mangum

MAX_LEN = 100
app = FastAPI()
handler = Mangum(app)

@app.get('/')
async def root():
    print({'message':'Hello'})

@app.get("/generate_text")
async def generate_text_api(user_prompt: str):
    if not validate_input_length(user_prompt):
        raise HTTPException(status_code=400, detail=f"Input length exceeds the limit of {MAX_LEN} characters")
    
    try:
        text = generate_text(user_prompt)
        return {"message": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

