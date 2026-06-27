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

    commands = {
        "select-all": lambda: keyboard.select_all(),
        "copy": lambda: keyboard.copy(),
        "paste": lambda: keyboard.paste(),
        "delete": lambda: keyboard.delete(),
        "backspace": lambda: keyboard.backspace(),
        "enter": lambda: keyboard.press_key("enter"),
        "tab": lambda: keyboard.press_key("tab"),
        "escape": lambda: keyboard.press_key("escape"),

        "up": lambda: keyboard.press_key("up"),
        "down": lambda: keyboard.press_key("down"),
        "left": lambda: keyboard.press_key("left"),
        "right": lambda: keyboard.press_key("right"),

        "alt-tab": lambda: keyboard.hotkey("alt", "tab"),
        "win-tab": lambda: keyboard.hotkey("win", "tab"),
        "win-d": lambda: keyboard.hotkey("win", "d"),
        "win-e": lambda: keyboard.hotkey("win", "e"),
        "win-r": lambda: keyboard.hotkey("win", "r"),
        "alt-f4": lambda: keyboard.hotkey("alt", "f4"),
        "ctrl-esc": lambda: keyboard.hotkey("ctrl", "escape"),
        "task-manager": lambda: keyboard.hotkey("ctrl", "shift", "escape"),

        "snap-left": lambda: keyboard.hotkey("win", "left"),
        "snap-right": lambda: keyboard.hotkey("win", "right"),
        "maximize": lambda: keyboard.hotkey("win", "up"),
        "minimize": lambda: keyboard.hotkey("win", "down"),
    }

    if command_name not in commands:
        return {"success": False, "error": f"Unsupported command: {command_name}"}

    commands[command_name]()
    return {"success": True, "command": command_name}


@app.post("/ui/command/{command_name}")
def ui_run_command(command_name: str):
    run_command(command_name)
    return RedirectResponse("/", status_code=303)