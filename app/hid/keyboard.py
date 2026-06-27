import time

CTRL = 0x01
SHIFT = 0x02
ALT = 0x04
WIN = 0x08

KEYS = {
    "a": 0x04, "b": 0x05, "c": 0x06, "d": 0x07, "e": 0x08,
    "f": 0x09, "g": 0x0A, "h": 0x0B, "i": 0x0C, "j": 0x0D,
    "k": 0x0E, "l": 0x0F, "m": 0x10, "n": 0x11, "o": 0x12,
    "p": 0x13, "q": 0x14, "r": 0x15, "s": 0x16, "t": 0x17,
    "u": 0x18, "v": 0x19, "w": 0x1A, "x": 0x1B, "y": 0x1C,
    "z": 0x1D,

    "1": 0x1E, "2": 0x1F, "3": 0x20, "4": 0x21, "5": 0x22,
    "6": 0x23, "7": 0x24, "8": 0x25, "9": 0x26, "0": 0x27,

    "\n": 0x28,
    "enter": 0x28,
    "escape": 0x29,
    "backspace": 0x2A,
    "tab": 0x2B,
    " ": 0x2C,
    "space": 0x2C,
    "-": 0x2D,
    "=": 0x2E,
    "[": 0x2F,
    "]": 0x30,
    "\\": 0x31,
    ";": 0x33,
    "'": 0x34,
    "`": 0x35,
    ",": 0x36,
    ".": 0x37,
    "/": 0x38,

    "delete": 0x4C,
    "right": 0x4F,
    "left": 0x50,
    "down": 0x51,
    "up": 0x52,
    "f4": 0x3D,
}

SHIFT_KEYS = {
    "A": 0x04, "B": 0x05, "C": 0x06, "D": 0x07, "E": 0x08,
    "F": 0x09, "G": 0x0A, "H": 0x0B, "I": 0x0C, "J": 0x0D,
    "K": 0x0E, "L": 0x0F, "M": 0x10, "N": 0x11, "O": 0x12,
    "P": 0x13, "Q": 0x14, "R": 0x15, "S": 0x16, "T": 0x17,
    "U": 0x18, "V": 0x19, "W": 0x1A, "X": 0x1B, "Y": 0x1C,
    "Z": 0x1D,

    "!": 0x1E, "@": 0x1F, "#": 0x20, "$": 0x21, "%": 0x22,
    "^": 0x23, "&": 0x24, "*": 0x25, "(": 0x26, ")": 0x27,
    "_": 0x2D, "+": 0x2E, "{": 0x2F, "}": 0x30, "|": 0x31,
    ":": 0x33, '"': 0x34, "~": 0x35, "<": 0x36, ">": 0x37,
    "?": 0x38,
}

MODIFIERS = {
    "ctrl": CTRL,
    "shift": SHIFT,
    "alt": ALT,
    "win": WIN,
    "windows": WIN,
}


class HidKeyboard:
    def __init__(self, device="/dev/hidg0"):
        self.device = device

    def _write_report(self, modifier, keycode):
        with open(self.device, "wb") as hid:
            hid.write(bytes([modifier, 0, keycode, 0, 0, 0, 0, 0]))
            hid.write(bytes([0, 0, 0, 0, 0, 0, 0, 0]))
        time.sleep(0.04)

    def type_text(self, text):
        for char in text:
            if char in KEYS:
                self._write_report(0, KEYS[char])
            elif char in SHIFT_KEYS:
                self._write_report(SHIFT, SHIFT_KEYS[char])

    def press_key(self, key_name: str):
        key_name = key_name.lower()
        if key_name not in KEYS:
            raise ValueError(f"Unsupported key: {key_name}")
        self._write_report(0, KEYS[key_name])

    def hotkey(self, *keys):
        modifier = 0
        keycode = None

        for key in keys:
            key = key.lower()

            if key in MODIFIERS:
                modifier |= MODIFIERS[key]
            elif key in KEYS:
                keycode = KEYS[key]
            else:
                raise ValueError(f"Unsupported hotkey part: {key}")

        if keycode is None:
            raise ValueError("Hotkey needs one normal key")

        self._write_report(modifier, keycode)

    def select_all(self):
        self.hotkey("ctrl", "a")

    def copy(self):
        self.hotkey("ctrl", "c")

    def paste(self):
        self.hotkey("ctrl", "v")

    def delete(self):
        self.press_key("delete")

    def backspace(self):
        self.press_key("backspace")