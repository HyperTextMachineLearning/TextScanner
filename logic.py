import time
import tkinter
from threading import Thread
import json
import pyautogui
from PIL import ImageGrab, ImageDraw, ImageTk
# import uuid
from cv2 import cv2 as cv
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'Path\\To\\tesseract.exe'

# Controls the {start|stop}ing of showing the preview image
stop_preview = False

# Controls whether the data being saved is not anything but answer
text_type = ''

def setText(widget, preview_text, selection_preview, widget_type):
    preview_target_thread = Thread(target=previewTarget, kwargs={'selection_preview': selection_preview})
    preview_target_thread.start()
    snapshot = ImageGrab.grab().convert('LA')
    # opencv_img = np.array(snapshot.convert('RGB'))
    # opencv_img = cv.cvtColor(opencv_img, cv.COLOR_RGB2GRAY)
    for _ in [4, 3, 2, 1]:
        widget.config(text=f"{_}")
        time.sleep(1)
    root_ = widget.master.master
    orig_color = root_.cget("background")
    # text_orig_color = widget.cget("foreground")
    initial_coords = pyautogui.position()
    widget.config(text="Start")
    # widget.config(disabledforeground="white")
    root_.config(background="red")
    time.sleep(0.4)
    # widget.config(disabledforeground=text_orig_color)
    root_.config(background=orig_color)
    for _ in range(2, 0, -1):
        widget.config(text=f"{_}")
        time.sleep(1)
    time.sleep(0.4)
    final_coords = pyautogui.position()
    box = tuple(initial_coords+final_coords)
    # From .convert('RGB') starts StackOverflow Code
    snapshot = snapshot.crop(box).convert('RGB')
    opencv_img = np.array(snapshot)
    opencv_img = cv.cvtColor(opencv_img, cv.COLOR_RGB2BGR)
    gray = cv.cvtColor(opencv_img, cv.COLOR_BGR2GRAY)
    thresh = 255 - cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    # Blur and perform text extraction
    thresh = cv.GaussianBlur(thresh, (3, 3), 0)
    text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
    # StackOverflow code ends here
    # text = pytesseract.image_to_string(snapshot, config='')
    if text.endswith('\x0c'):
        text = text[:text.rfind('\x0c')]
        if text.endswith('\n'):
            text = text[:text.rfind('\n')]
    preview_text.delete('1.0', 'end')
    preview_text.insert('1.0', text)
    # print(text)
    print(text.split('\n'))
    # snapshot.save(f'temp_dump/{uuid.uuid4().hex}.png')
    snapshot.close()
    # print(final_coords)
    # time.sleep(1)
    global stop_preview
    stop_preview = True
    global text_type
    if widget_type == 'q':
        widget.config(text="Question")
        text_type = 'q'
    elif widget_type == 'a':
        widget.config(text="Answers")
        text_type = 'a'
    else:
        widget.config(text="Extras")
        text_type = 'e'
    # widget.config(disabledforeground="white")
    root_.config(background="green")
    time.sleep(0.4)
    # widget.config(disabledforeground=text_orig_color)
    root_.config(background=orig_color)
    widget['state'] = 'normal'

def previewTarget(selection_preview):
    # Capture the SS
    snapshot = ImageGrab.grab()

    # Get the current position
    position = pyautogui.position()

    # Coordinates to crop, then crop the image and set it on the canvas
    crop_coords = position[0] - 100, position[1] - 100, position[0] + 100, position[1] + 100
    snapshot = snapshot.crop(crop_coords)
    snapshot_1 = ImageDraw.Draw(snapshot)

    # Crosshair's Vertical Line coords
    # coords = (position[0], position[1] - 40, position[0], position[1] + 40)
    snapshot_1.line([(100, 70), (100, 130)], fill="red", width=2)

    # Crosshair's Horizontal Line coords
    # coords = (position[0] - 40, position[1], position[0] + 40, position[1])
    snapshot_1.line([(70, 100), (130, 100)], fill="red", width=2)

    img = ImageTk.PhotoImage(snapshot)
    selection_preview.imgtk = img
    selection_preview.config(image=img)
    if not stop_preview:
        selection_preview.after(10, lambda: previewTarget(selection_preview))

def getQuestionText(event, preview_text, selection_preview, widget_type='', arg=None):
    global stop_preview
    stop_preview = False
    q_btn = event.widget
    q_btn['state'] = 'disabled'
    x = Thread(target=setText,
               kwargs={'widget': q_btn,
                       'preview_text': preview_text,
                       'selection_preview': selection_preview,
                       'widget_type': widget_type})
    x.start()

def getAnswers(event, preview_text, selection_preview, widget_type='', arg=None):
    global stop_preview
    stop_preview = False
    a_btn = event.widget
    a_btn['state'] = 'disabled'
    x = Thread(target=setText,
               kwargs={'widget': a_btn,
                       'preview_text': preview_text,
                       'selection_preview': selection_preview,
                       'widget_type': widget_type})
    x.start()

def getExtras(event, preview_text, selection_preview, widget_type='', arg=None):
    global stop_preview
    stop_preview = False
    e_btn = event.widget
    e_btn['state'] = 'disabled'
    x = Thread(target=setText,
               kwargs={'widget': e_btn,
                       'preview_text': preview_text,
                       'selection_preview': selection_preview,
                       'widget_type': widget_type})
    x.start()

def saveToDB(event, preview_text, q_no):
    question_no = q_no
    global text_type
    with open("questions/mock.json", "r") as db:
        question_db = json.load(db)
        if text_type == 'q':
            question_db[f"q_{question_no}"]["body"] = preview_text.get("1.0", tkinter.END)
        elif text_type == 'a':
            opt = preview_text.get("1.0", tkinter.END).split("\n")
            for _ in opt:
                if _ == "" or not (len(_) > 0):
                    opt.pop(opt.index(_))
            for _ in range(0, 4):
                if len(question_db[f"q_{question_no}"]["options"]) == 4:
                    question_db[f"q_{question_no}"]["options"][_] = opt[_]
                else:
                    question_db[f"q_{question_no}"]["options"].append(opt[_])
        elif text_type == 'e':
            question_db[f"q_{question_no}"]["extras"] = preview_text.get("1.0", tkinter.END)

    with open("questions/mock.json", "w") as db:
        json.dump(question_db, db, indent=4)
    print(preview_text.get("1.0", tkinter.END))
