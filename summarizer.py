import nltk
nltk.download("punkt")
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def summarize_text(text,num_sentences=5):
    parser=PlaintextParser.from_string(text,Tokenizer("english"))
    summarizer=LexRankSummarizer()
    summary=summarizer(parser.document,num_sentences)
    return "\n\n".join(f"• {sentence}" for sentence in summary)