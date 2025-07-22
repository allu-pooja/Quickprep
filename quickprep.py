import streamlit as st
import nltk
import nlp
import pymongo
import io
from text_extract import extract_text_from_PDF_files
from summarizer import summarize_text
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from pdf_conversion import create_pdf
from auth import save_user_history
from auth import get_user_history
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI=os.getenv("MONGO_URI")
client=pymongo.MongoClient(MONGO_URI)
db=client["Quickprep"]
history_collection=db["history"]

def quickprep_page():
    st.title("QuickPrep")

    username = st.session_state.get("username", "")

    user_history=[]
    if username:
        user_history=list(history_collection.find({"username":username}))

    upload_file = st.file_uploader("Upload your pdf", type="pdf")
    
    with st.sidebar:
        st.title("Tools")
        word = st.text_input("Search word meaning")

        if word:
            with st.spinner("Searching"):
                lemmatizer = WordNetLemmatizer()
                lemma = lemmatizer.lemmatize(word.lower())
                synsets = wordnet.synsets(lemma)

            if synsets:
                st.subheader(f"Meaning(s) of '{word}':")
                for i, syn in enumerate(synsets[:5], 1):
                    st.write(f"{i}. ({syn.pos()}) {syn.definition()}")
            else:
                st.error("Meaning not found")

        st.text_area("Add notes")

        st.title("Your History")
        if user_history:
            for idx, entry in enumerate(user_history):
                # Make sure entry is a dict
                if isinstance(entry, dict):
                    filename = entry.get("filename", f"Untitled_{idx}.pdf")
                    summary = entry.get("summary", "")
                    images_data = entry.get("images", [])

                    with st.expander(f"{filename}"):
                        pdf_data = create_pdf(summary)
                        st.download_button(
                            label="Download PDF",
                            data=pdf_data,
                            file_name=filename,
                            mime="application/pdf",
                            key=f"sidebar_download_{idx}"
                        )
        else:
            st.write("No history found yet.")

    if "extracted_text" not in st.session_state:
        st.session_state["extracted_text"] = None
    if "summary" not in st.session_state:
        st.session_state["summary"] = None
    if "file_uploaded" not in st.session_state:
        st.session_state["file_uploaded"] = False
    if "history" not in st.session_state:
        st.session_state["history"] = []

    uploaded_filename = upload_file.name if upload_file else "default"
    download_filename = uploaded_filename.replace(".pdf", "_summary.pdf")
    
    if upload_file:
        st.success("File uploaded Successfully")
        st.session_state["file_uploaded"] = True

        if st.button("Summarize"):
            with st.spinner("Text summarizing.... Please wait"):
                extracted_text = extract_text_from_PDF_files(upload_file)
                summary = summarize_text(extracted_text, num_sentences=5)

                upload_file.seek(0)

                history_collection.insert_one({
                    "username": username,
                    "filename": uploaded_filename.replace(".pdf", "_summary.pdf"),
                    "summary": summary,
                })
                
                st.session_state["extracted_text"] = extracted_text
                st.session_state["summary"] = summary

               
   #Extarct text,images
    if st.session_state["extracted_text"] is not None:
        st.header("Extracted Text")
        st.write(st.session_state["extracted_text"][:1000])

        st.header("Summary")
        st.markdown(summarize_text(st.session_state["extracted_text"]),unsafe_allow_html=True)
        st.write(st.session_state["summary"])

     # Download summarized pdf
    if st.session_state["summary"] is not None:
        pdf_data = create_pdf(st.session_state["summary"])
        st.download_button(
            label=("Click here to download"),
            data=pdf_data,
            file_name=download_filename,
            mime="application/pdf"
        )









            
