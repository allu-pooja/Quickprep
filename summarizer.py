import nltk
import spacy
nltk.data.path.append(r'C:\Users\allup\OneDrive\Desktop\python\QuickPrep\nltk_data')
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

import spacy.cli

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def spacy_sent_tokenize(text):
    doc=nlp(text)
    return [sent.text.strip() for sent in doc.sents]

def summarize_text(text,num_sentences=5):
    sentences=spacy_sent_tokenize(text)
    clean_text=" ".join(sentences)

    parser=PlaintextParser.from_string(clean_text,Tokenizer("english"))
    summarizer=LexRankSummarizer()
    summary=summarizer(parser.document,num_sentences)
    return "\n\n".join(f"• {sentence}" for sentence in summary)