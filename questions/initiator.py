import json

questions = {}
for _ in range(1, 41):
    questions[f"q_{_}"] = {
        "body": "",
        "options": [],
        "answer": "0",
        "extras": ""
    }
with open("mock.json", "w") as db:
    json.dump(questions, db, indent=4)

answers = {}
for _ in range(1, 41):
    answers[f"q_{_}"] = ""

with open("answers.json", "w") as ans:
    json.dump(answers, ans, indent=4)