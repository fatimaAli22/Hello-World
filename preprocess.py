import json
import spacy
import uuid
from tqdm import tqdm
from spacy.tokens import DocBin


nlp = spacy.blank("en")


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


train_data = load_data("./data/json/train.json")["annotations"]
dev_data = load_data("./data/json/dev.json")["annotations"]
annotated_answers = load_data("./data/json/annotated_answers.json")


def create_training(TRAIN_DATA):
    db = DocBin()
    for text, annot in tqdm(TRAIN_DATA):
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print("Skipping entity")
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    return db


def generate_final_answers(annotated_answers):
    answers = []
    for annotation in annotated_answers["annotations"]:
        answer_string, entities_data = annotation

        # Extract unique labels
        unique_labels = set(label for _, _, label in entities_data["entities"])

        answer = {
            "id": str(uuid.uuid4()),
            "body": answer_string,
            "label": list(unique_labels),
        }

        answers.append(answer)

    with open("./data/json/answers.json", "w", encoding="utf-8") as output_file:
        json.dump(answers, output_file, indent=2, ensure_ascii=False)

    print("Conversion completed. Generated answers.json file.")


train_db = create_training(train_data)
dev_db = create_training(dev_data)

train_db.to_disk("./data/train.spacy")
dev_db.to_disk("./data/dev.spacy")

generate_final_answers(annotated_answers)
