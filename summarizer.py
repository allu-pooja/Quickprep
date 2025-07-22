import nltk
import spacy
nltk.download("punkt")
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

nlp=spacy.load("en_core_web_sm")

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