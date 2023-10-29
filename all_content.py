from tkinter import *
from tkinter import font as tkFont
from tkinter.scrolledtext import ScrolledText
import json
import pyperclip
import urllib.parse as url
import subprocess

v = 0
# New Window Showing the complete content
class AllContent:
    def __init__(self, *args, **kwargs):
        self.window = Toplevel()
        self.initiate()

    def refresh(self, *args, **kwargs):
        self.initiate()

    def initiate(self):
        with open("questions/mock.json", "r") as db:
            question_db = json.load(db)
            self.window.title("All Content")
            self.window.config(bg="#0c082b")
            self.window.geometry(f"{self.window.winfo_screenwidth() - 100}x{self.window.winfo_screenheight() - 100}+0+0")
            self.window.state('normal')
            self.window.configure(pady=10)
            self.window.columnconfigure(0, weight=1)
            self.window.rowconfigure(0, weight=1)

            main_frame = Frame(self.window,
                               bg="#0c082b")
            main_frame.grid(row=0, column=0, sticky="nsew")
            main_frame.columnconfigure(0, weight=6)
            main_frame.columnconfigure(1, weight=3)
            main_frame.rowconfigure(0, weight=1)

            # From Here Starts connecting with the backend
            # This frame shows the question's text, answers and any extra details
            question_detail_frame = Frame(main_frame,
                                          bd=2,
                                          bg="#0c082b",
                                          padx=10,
                                          pady=10,
                                          highlightthickness=1)
            question_detail_frame.config(highlightbackground="white", highlightcolor="white")
            question_detail_frame.grid(row=0, column=0, sticky="nsew", padx=10)
            question_detail_frame.rowconfigure(0, weight=0)
            question_detail_frame.rowconfigure(1, weight=0)
            question_detail_frame.rowconfigure(2, weight=0)
            question_detail_frame.rowconfigure(3, weight=0)
            q_font = tkFont.Font(family='Bitstream Vera Sans Mono', size=15, weight='normal')
            q_no_frame = Frame(question_detail_frame,
                               pady=10,
                               bg="#0c082b",)
            q_no_frame.grid(row=0, column=0, sticky=NW)
            question_ = Label(q_no_frame,
                              text="Question No.",)
            question_no = Label(q_no_frame,
                                text="01",
                                foreground="#FF0000")
            question_['font'] = question_no['font'] = q_font
            question_.pack(side=LEFT)
            question_no.pack(side=LEFT, padx=10)

            # Question Text Label and config
            s = "# This frame has all the questions as buttons for navigation to a specific question " * 6
            self.window.update()
            question_text = Label(question_detail_frame,
                                  wraplength=question_detail_frame.winfo_width() - 10,
                                  justify=LEFT,
                                  font=("Bitstream Vera Sans Mono", 14))
            if question_db["q_1"]["body"] == "":
                question_text.config(text=s)
            else:
                question_text.config(text=question_db["q_1"]["body"])
            question_text.grid(row=1, column=0, columnspan=2, ipady=10, ipadx=15, sticky=NW)

            # Handles resizing of Question Text
            def q_frame_resizer(e):
                # self.window.update()
                e.widget.update()
                # question_text.config(wraplength=question_detail_frame.winfo_width() - 20)
                question_text.config(wraplength=e.width - 20)
                # print(question_text['text'])
            # self.window.bind('<Configure>', q_frame_resizer)
            question_detail_frame.bind('<Configure>', q_frame_resizer)

            # Buttons Related to Questions
            q_related_btn = Frame(question_detail_frame,
                                  pady=10,
                                  bg="#0c082b",)
            q_related_btn.columnconfigure(0, weight=1)
            q_related_btn.columnconfigure(1, weight=1)
            q_related_btn.columnconfigure(2, weight=1)
            q_related_btn.grid(row=2, column=0, columnspan=2, sticky=NW, pady=10)
            copy_btn = Button(q_related_btn,
                              text="Copy",
                              font=("Microsoft Sans Serif", 13))
            extra_btn = Button(q_related_btn,
                               text="Extras",
                               font=("Microsoft Sans Serif", 13))
            save_btn = Button(q_related_btn,
                              text="Save",
                              font=("Microsoft Sans Serif", 13))
            copy_btn.grid(row=0, column=0)
            extra_btn.grid(row=0, column=2)
            save_btn.grid(row=0, column=3, padx=10)
            save_btn.bind("<ButtonPress-1>", self.refresh)
            chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome --incognito"
            search_query = f"{chrome_path} \"{question_text['text']}\""
            copy_btn.bind("<ButtonPress-1>", lambda e: pyperclip.copy(question_text['text']))

            # Answers for a Question Section, all RadioButtons
            # String Var , kinda acts as the RadioGroup
            q_ans_frame = Frame(question_detail_frame,
                                pady=0,
                                bg="#0c082b",)
            q_ans_frame.grid(row=3, column=0, columnspan=2, sticky=NW)

            # Saves the answer choice
            # def selectedAnswer(opt_no):
            #     q_no = question_no['text']
            #     with open("questions/mock.json", "w") as db_:
            #         update_answer = json.load(db_)
            #         if q_no[0] == "0":
            #             update_answer[f"q_{q_no[1]}"]["selected"] = opt_no
            #         else:
            #             update_answer[f"q_{q_no}"]["selected"] = opt_no
            #         json.dump(update_answer, db_, indent=4)
            #     self.refresh()
            global v
            v = StringVar(q_ans_frame, "answer")
            opt_1 = Radiobutton(q_ans_frame,
                                text="Option 1",
                                value="0",
                                bg="#0d5e0b",
                                selectcolor="#0d5e0b",
                                fg="white",
                                font=("Bitstream Vera Sans Mono", 14),
                                variable=v,)
            opt_2 = Radiobutton(q_ans_frame,
                                text="Option 2",
                                value="1",
                                bg="#0d5e0b",
                                selectcolor="#0d5e0b",
                                fg="white",
                                font=("Bitstream Vera Sans Mono", 14),
                                variable=v,)
            opt_3 = Radiobutton(q_ans_frame,
                                text="Option 3",
                                value="2",
                                bg="#0d5e0b",
                                selectcolor="#0d5e0b",
                                fg="white",
                                font=("Bitstream Vera Sans Mono", 14),
                                variable=v,)
            opt_4 = Radiobutton(q_ans_frame,
                                text="Option 4",
                                value="3",
                                bg="#0d5e0b",
                                selectcolor="#0d5e0b",
                                fg="white",
                                font=("Bitstream Vera Sans Mono", 14),
                                variable=v,)
            opt_1.pack(side=LEFT, )
            opt_2.pack(side=LEFT, padx=10)
            opt_3.pack(side=LEFT, )
            opt_4.pack(side=LEFT, padx=10)
            options = (opt_1, opt_2, opt_3, opt_4)
            if len(question_db["q_1"]["options"]) == 4:
                for _ in range(0, 4):
                    options[_].config(text=question_db["q_1"]["options"][_])

            # This frame has all the questions as buttons for navigation to a specific question
            question_navigator_frame = Frame(main_frame,
                                             bd=2,
                                             bg="#0c082b",
                                             padx=10,
                                             pady=10,
                                             highlightthickness=1)
            question_navigator_frame.config(highlightbackground="white", highlightcolor="white")

            # padx was 10 in the following
            question_navigator_frame.grid(row=0, column=1, sticky="nsew", padx=0)
            question_navigator_frame.columnconfigure(0, weight=1)
            question_navigator_frame.rowconfigure(0, weight=6)
            question_navigator_frame.rowconfigure(1, weight=3)
            # Frame for containing all Buttons
            question_btn_frame = Frame(question_navigator_frame,
                                       bg="#0c082b",
                                       bd=2,
                                       padx=0,
                                       highlightthickness=1)
            question_btn_frame.config(highlightbackground="white", highlightcolor="white")
            question_btn_frame.grid(row=0, column=0, sticky=NSEW)
            question_btns = []
            helv14 = tkFont.Font(family='Helvetica', size=14, weight='bold')
            for _ in range(0, 5):
                question_btn_frame.columnconfigure(_, weight=1)
            for _ in range(0, 8):
                question_btn_frame.rowconfigure(_, weight=1)
            num = 1

            # Handling of Displaying Question Details on Button Press
            def showQuestionDetails(event):
                q_no = event.widget['text']
                question_no.config(text=q_no)
                if q_no[0] == "0":
                    question_text.config(text=question_db[f"q_{q_no[1]}"]["body"])
                    if len(question_db[f"q_{q_no[1]}"]["options"]) == 4:
                        for _ in range(0, 4):
                            options[_].config(text=question_db[f"q_{q_no[1]}"]["options"][_])
                    else:
                        pass
                else:
                    if len(question_db[f"q_{q_no}"]["options"]) == 4:
                        for _ in range(0, 4):
                            options[_].config(text=question_db[f"q_{q_no}"]["options"][_])
                    else:
                        pass
                    question_text.config(text=question_db[f"q_{q_no}"]["body"])

            for row_n in range(0, 8):
                for col_n in range(0, 5):
                    if num < 10:
                        q_btn = Button(question_btn_frame,
                                       text=f"0{num}",
                                       padx=2,
                                       pady=2)
                    else:
                        q_btn = Button(question_btn_frame,
                                       text=f"{num}",
                                       padx=2,
                                       pady=2)
                    question_btns.append(q_btn)
                    q_btn['font'] = helv14
                    q_btn.grid(row=row_n, column=col_n, padx=0, pady=0)
                    if question_db[f"q_{num}"]["body"] == "":
                        q_btn['state'] = 'disabled'
                    if not num == 1:
                        q_btn.bind("<ButtonPress-1>", showQuestionDetails)
                    num += 1

