import spacy
import json

with open("./data/json/answers.json", "r", encoding="utf-8") as f:
    answers = json.load(f)

nlp = spacy.load("./output/model-last")

question = """
How do I find out which process is listening on a TCP or UDP port on Windows?
"""

doc = nlp(question)

results = []

for ent in doc.ents:
    print(ent.text, ent.label_)
    for answer in answers:
        if "id" in answer and any(res.get("id") == answer["id"] for res in results):
            continue

        if ent.text.lower() in answer["body"].lower() or ent.label_ in answer["label"]:
            results.append(answer)
            break


for res in results:
    print(res["id"])

#How do I find out which process is listening on a TCP or UDP port on Windows?
#What is the difference between a port and a socket?
#How can I connect to Android with ADB over TCP?
#What is the quickest way to HTTP GET in Python?
#Finding local IP addresses using Python's stdlib