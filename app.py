import tkinter
from tkinter import *

import pyautogui
from all_content import AllContent
from logic import getQuestionText, getAnswers, getExtras, saveToDB
from tkinter.scrolledtext import ScrolledText
import pyperclip

# Other Definitions

# Padding for Buttons
btn_padx = 15
btn_pady = 15

root = Tk()

# Root Window Definitions
root_width = 650
root_height = 980
root_bg = "#0c082b"
root.geometry(f"{root_width}x{root_height}+{int(root.winfo_screenwidth()-root_width)}+0")
root.configure(bg=root_bg)
root.configure(pady=10)
root.configure(padx=10)
root.columnconfigure(0, weight=1)

# Frame for containing all buttons
btn_frame = Frame(
    root,
    bg=root_bg,
    bd=2,
    padx=10,
    pady=10,
    highlightthickness=1
)
btn_frame.config(highlightbackground="white", highlightcolor="white")
btn_frame.grid(row=0, column=0, sticky="nsew")
btn_frame.columnconfigure(0, weight=1)
btn_frame.columnconfigure(1, weight=1)
btn_frame.columnconfigure(2, weight=1)

# All Buttons
question_btn = Button(
                btn_frame,
                text="Question",
                font=("Microsoft Sans Serif", 12))
question_btn.grid(row=0, column=0, padx=15)
question_btn.bind("<ButtonPress-1>", lambda event: getQuestionText(event, preview_text, selection_preview, widget_type='q'))

answer_btn = Button(
                btn_frame,
                text="Answers",
                font=("Microsoft Sans Serif", 12)
                )
answer_btn.grid(row=0, column=1, padx=15)
answer_btn.bind("<ButtonPress-1>", lambda event: getAnswers(event, preview_text, selection_preview, widget_type='a'))

extras_btn = Button(
                btn_frame,
                text="Extras",
                font=("Microsoft Sans Serif", 12)
                )
extras_btn.grid(row=0, column=2, padx=15)
extras_btn.bind("<ButtonPress-1>", lambda event: getExtras(event, preview_text, selection_preview, widget_type=''))

# Frame For Preview and confirm
preview_frame = Frame(
                    root,
                    bg=root_bg,
                    bd=2,
                    padx=5,
                    pady=5,
                    highlightthickness=1
                    )
preview_frame.config(highlightbackground="white", highlightcolor="white")
preview_frame.columnconfigure(0, weight=1)
preview_frame.columnconfigure(1, weight=1)
preview_frame.columnconfigure(2, weight=1)
preview_frame.grid(row=1, column=0, pady=10)

# Frame Components
preview_text = ScrolledText(preview_frame,
                            height=16,
                            width=44,
                            font=('Dejavu Sans Mono', 14))
preview_text.grid(row=0, column=0, columnspan=3)
# preview_text.tag_config('justified', justify='center')


q_no_len = StringVar()
q_no = Entry(preview_frame,
             width=2,
             justify=CENTER,
             font=("Microsoft Sans Serif", 14),
             textvariable=q_no_len)

def qNoLimit(q_no_len):
    if len(q_no_len.get()) > 0:
        q_no_len.set(q_no_len.get()[:2])


q_no_len.trace("w", lambda *args: qNoLimit(q_no_len))

q_no.grid(row=1, column=0, pady=10, ipadx=10, ipady=10)

copy_btn = Button(preview_frame,
                  text="Copy",
                  font=("Microsoft Sans Serif", 12))
copy_btn.grid(row=1, column=1, pady=10)
def test(e, pt):
    text = pt.get("1.0", tkinter.END)
    if text.endswith('\n'):
        text = text[:text.rfind('\n')]
    pyperclip.copy(text)
    print(text)
    print(text.split("\n"))
    # print(text.split())
    # print(list(text))


copy_btn.bind("<ButtonPress-1>", lambda e: test(e, preview_text))
# copy_btn.bind("<ButtonPress-1>", lambda e: pyperclip.copy(preview_text.get("1.0", tkinter.END)))
confirm_btn = Button(preview_frame,
                     text="Confirm",
                     font=("Microsoft Sans Serif", 12))

confirm_btn.grid(row=1, column=2, pady=10)
confirm_btn.bind("<ButtonPress-1>", lambda event: saveToDB(event, preview_text, q_no.get()))

# Preview of the Selection Image
# selection_preview = Canvas(root, width=126, height=126)
selection_preview = Label(root)
selection_preview.grid(row=2, column=0, pady=10)

content_btn = Button(root,
                     text="All Content",
                     font=("Microsoft Sans Serif", 12))
content_btn.grid(row=3, column=0)
content_btn.bind("<ButtonPress-1>", AllContent)


root.mainloop()
