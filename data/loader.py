import os
import re

def clean_text(text):

    text = re.sub(r"^.*?\n\n", "", text, flags=re.DOTALL)
    text = re.sub(r">.*\n", "", text)
    text = re.sub(r"--.*", "", text)

    text = text.lower()

    text = re.sub(r"http\S+|www\S+", "", text)

    text = re.sub(r"[^a-z\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def load_dataset(dataset_path):

    documents = []
    labels = []

    for category in os.listdir(dataset_path):

        category_path = os.path.join(dataset_path, category)

        if os.path.isdir(category_path):

            for file in os.listdir(category_path):

                file_path = os.path.join(category_path, file)

                try:
                    with open(file_path, "r", encoding="latin1") as f:

                        text = f.read()

                        cleaned_text = clean_text(text)

                        if len(cleaned_text) > 20:
                            documents.append(cleaned_text)
                            labels.append(category)

                except:
                    continue

    return documents, labels