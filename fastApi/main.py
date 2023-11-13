import openai

from fastapi import FastAPI

from .setting import Settings


app = FastAPI()


@app.get("/")
async def ping():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def test(item_id: int):
    return {"message": "Hellasdfasdfasdfasdfo World", "item_id": item_id}


@app.get("/prompt/{prompt}")
async def prompt(prompt: str):
    openai.api_key = "empty"
    openai.api_base = Settings().llm_server_URL
    completion = openai.Completion.create(
        model="lmsys/vicuna-7b-v1.3", prompt=prompt, max_tokens=30
    )
    return {"message": completion.choices[0].text}
