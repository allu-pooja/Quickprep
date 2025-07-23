import nltk
import os
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
import pickle
import spacy.cli
from nltk.tokenize.punkt import PunktSentenceTokenizer

nltk_path = os.path.join(os.path.dirname(__file__), "nltk_data")
punkt_path = os.path.join(nltk_path, "tokenizers", "punkt", "english.pickle")
nltk.data.path.append(nltk_path)

with open(punkt_path, "rb") as f:
    punkt_tokenizer = PunktSentenceTokenizer(pickle.load(f))

    
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def spacy_sent_tokenize(text):
    doc=nlp(text)
    return [sent.text.strip() for sent in doc.sents]

# Custom tokenizer using Punkt
class CustomSumyTokenizer:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    def to_sentences(self, text):
        return self.tokenizer.tokenize(text)

def summarize_text(text,num_sentences=5):
    sentences=spacy_sent_tokenize(text)
    clean_text=" ".join(sentences)

    parser = PlaintextParser.from_string(clean_text, CustomSumyTokenizer(punkt_tokenizer))
    summarizer=LexRankSummarizer()
    summary=summarizer(parser.document,num_sentences)
    return "\n\n".join(f"• {sentence}" for sentence in summary)