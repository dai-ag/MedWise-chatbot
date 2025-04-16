from fpdf import FPDF
import base64

def generate_pdf(chat_history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for msg in chat_history:
        role = "You" if msg["role"] == "user" else "MedWise Bot"
        content = msg["content"]
        pdf.multi_cell(0, 10, f"{role}: {content}\n")

    pdf_path = "/tmp/medwise_chat.pdf"
    pdf.output(pdf_path)
    return pdf_path

if st.sidebar.button("⬇️ Export Chat to PDF"):
    pdf_file_path = generate_pdf(st.session_state.messages)
    with open(pdf_file_path, "rb") as file:
        btn = st.download_button(
            label="Download PDF",
            data=file,
            file_name="medwise_chat.pdf",
            mime="application/pdf"
        )
