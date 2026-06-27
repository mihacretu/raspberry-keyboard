from fastapi import FastAPI, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.hid.keyboard import HidKeyboard

app = FastAPI(title="Mivi Agent")

keyboard = HidKeyboard()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "status": "online",
            "service": "mivi-agent",
        },
    )

@app.get("/health")
def health():
    return {
        "status": "online",
        "service": "mivi-agent",
        "keyboard_device": "/dev/hidg0",
    }


@app.post("/type")
def type_text(text: str = Query(...)):
    keyboard.type_text(text)
    return {"success": True, "typed": text}


@app.post("/ui/type")
def ui_type_text(text: str = Form(...)):
    keyboard.type_text(text)
    return RedirectResponse("/", status_code=303)


@app.post("/command/{command_name}")
def run_command(command_name: str):
    command_name = command_name.lower()

    if command_name == "select-all":
        keyboard.select_all()
    elif command_name == "copy":
        keyboard.copy()
    elif command_name == "paste":
        keyboard.paste()
    elif command_name == "delete":
        keyboard.delete()
    elif command_name == "backspace":
        keyboard.backspace()
    elif command_name == "enter":
        keyboard.press_key("enter")
    elif command_name == "tab":
        keyboard.press_key("tab")
    elif command_name == "escape":
        keyboard.press_key("escape")
    else:
        return {"success": False, "error": f"Unsupported command: {command_name}"}

    return {"success": True, "command": command_name}


@app.post("/ui/command/{command_name}")
def ui_run_command(command_name: str):
    run_command(command_name)
    return RedirectResponse("/", status_code=303)