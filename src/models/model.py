"""
Model
-----
This module defines AI-dependent functions.
"""
import json
from pathlib import Path
import random
import numpy as np
import torch
from transformers import AutoTokenizer

from src.models.contriever import Contriever

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)

contriever = Contriever.from_pretrained("facebook/contriever")
tokenizer = AutoTokenizer.from_pretrained("facebook/contriever")

with open(Path(__file__).parents[1] / "dataset\English_df.json", "r", encoding="utf-8") as file:
    faq = json.load(file)

questions = [item["question"] for item in faq]


def get_answer(question: str):
    """Return an aswer and a context to the question from the datanase."""
    answer_and_context = [(item["text"], item["context"]) for item in faq if item["question"] == question]
    return answer_and_context


def find_similar_questions(question: str):
    """Return a list of similar questions from the database."""
    query = tokenizer(question, padding=True, truncation=True, return_tensors="pt")
    embeddings_query = contriever(**query)
    questions_toks = tokenizer(questions, padding=True, truncation=True, return_tensors="pt")
    embeddings_question = contriever(**questions_toks)
    dot_product = []
    for idx, _ in enumerate(embeddings_question):
        dot_product.append((embeddings_query @ embeddings_question[idx]).item())
    ids_max_score = sorted(range(len(dot_product)), key=lambda x: dot_product[x], reverse=True)[:3]
    result = []
    for i in ids_max_score:
        result.append(questions[i])
    return result
