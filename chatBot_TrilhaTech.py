# Importar bibliotecas
import streamlit as st
import fitz
from groq import Groq
from PIL import Image

# Configurar chave da Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Função para extrair texto de PDFs (se quiser usar também com PDFs futuramente)
def extract_files(uploader):
    text = ""
    for pdf in uploader:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text")
    return text

# Função para carregar a base de conhecimento
def carregar_base_conhecimento(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

# Função para interagir com a IA
def chat_with_groq(prompt, context):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "Você é um assistente que responde a perguntas relacionadas a Engenharia de Software."},
            {"role": "user", "content": f"{context}\n\nPergunta: {prompt}"}
        ]
    )
    return response.choices[0].message.content

# Interface
def main():
    # Lado superior com logo
    col1, col2 = st.columns([1, 3])
    with col1:
        image = Image.open("logo_chatbot.jpeg")
        st.image(image, caption="Trilha Tech", use_container_width=True)
    with col2:
        st.markdown("## Chatbot - Carreira em Engenharia de Software 💻🚀")
        st.markdown("Este chatbot foi desenvolvido para responder perguntas com base em uma base de conhecimento especializada em carreira na área de Engenharia de Software.")

    st.divider()

    # Carregar base de conhecimento
    base_conhecimento = carregar_base_conhecimento("base_conhecimento_carreira_eng_software.txt")

    # Caixa de pergunta
    st.markdown("### Faça sua pergunta abaixo:")
    user_input = st.text_area("Ex: Quais áreas de atuação existem na engenharia de software?", height=100)

    if st.button("Enviar pergunta"):
        if user_input.strip() == "":
            st.warning("Digite uma pergunta antes de enviar.")
        else:
            resposta = chat_with_groq(user_input, base_conhecimento)
            st.markdown("### Resposta da IA:")
            st.success(resposta)

    st.divider()
    st.caption("🔹 Desenvolvido com Streamlit + Groq API | Trilha Tech 2025")

if __name__ == "__main__":
    main()
