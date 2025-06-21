import io
from fpdf import FPDF

def create_pdf(summary_text):
    def clean_text(text):
        return text.encode("latin-1","replace").decode("latin-1")
    pdf=FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True,margin=15)

    #Summary
    pdf.set_font("Arial",size=12)
    cleaned_summary=clean_text("Summary:\n\n"+summary_text)
    pdf.multi_cell(0,10,txt=cleaned_summary)

    output=io.BytesIO()
    pdf_bytes=pdf.output(dest='S')
    output.write(pdf_bytes)
    output.seek(0)
    return output