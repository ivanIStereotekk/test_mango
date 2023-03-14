import openai
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import FileResponse

from app.db import User
from app.users import fastapi_users
from settings import OPEN_AI_API_KEY

openai.api_key = OPEN_AI_API_KEY
tried_models = ["code-cushman-001", ]

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

current_user = fastapi_users.current_user(active=True)


def show_list_models():
    models = openai.Model.list()
    return models.data


def send_prompt(gpt_prompt: str):
    raw_response = openai.Completion.create(
        engine="code-cushman-001",
        prompt=gpt_prompt,
        max_tokens=256,
    )
    proper_response = raw_response['choices'][0]['text']
    return proper_response

@router.get("/do",
            status_code=status.HTTP_200_OK)
async def make_prompt(prompt: str,
                      user: User = Depends(current_user)):
    """
    Method to send prompt to the OpenAI ChatGPT.
    :param prompt:
    :param user:
    :return: answer
    """
    if user.is_active:
        result = send_prompt(prompt)
        return {"answer": result}
    else:
        raise HTTPException(status_code=400, detail="Inactive user")


@router.get("/image",
            status_code=status.HTTP_200_OK)
async def make_image(prompt: str, image_size: str,
                     user: User = Depends(current_user)):
    """
    Method to send OpenAI Prompt to Image generation (DALL·E) (Default value: 512x512).
    :param prompt:
    :param user:
    :return: answer
    """
    if user.is_active:
        if not image_size:
            image_size = "512x512"
            image_resp = openai.Image.create(prompt=prompt, n=4, size=image_size)
            return FileResponse(image_resp)
        else:
            image_resp = openai.Image.create(prompt=prompt, n=4, size=image_size)
            return FileResponse(image_resp)
    else:
        raise HTTPException(status_code=400, detail="Error")


@router.get("/engines",
            status_code=status.HTTP_200_OK)
async def list_engines(user: User = Depends(current_user)):
    if user.is_active:
        try:
            result = show_list_models()
            return {"engines": result}
        except BaseException as e:
            raise HTTPException(status_code=400, detail=str(e))

            # image_resp = openai.Image.create(prompt="two dogs playing chess, oil painting", n=4, size="512x512")
