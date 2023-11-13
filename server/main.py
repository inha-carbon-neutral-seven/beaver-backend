import openai
from fastapi import FastAPI
from .setting import Settings


app = FastAPI()


@app.get("/")
async def ping():
    return {"message": "Hello World"}

@app.get("/prompt/{prompt}")
async def do_prompt(prompt: str):
    openai.api_key = "empty"
    openai.api_base = Settings().llm_server_URL
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]
    message = prompt
    messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
      model=Settings().llm_server_ChatCompletion,
      messages=messages
    )

    chat_message = response['choices'][0]['message']['content']
    return {"message" : chat_message}
