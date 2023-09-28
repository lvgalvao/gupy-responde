import streamlit as st
from app.get_data import url_builder, fetch_page, extract_hrefs, extract_body_text, save_to_txt
from app.chatgpt import read_context_from_txt, ask_gpt

def main():
    st.title("Webscraping e OpenAI Streamlit App")

    # Campo de entrada para o termo de pesquisa
    termo = st.text_input("Digite o termo de busca:")

    # Botão para executar webscraping
    if st.button('Raspar URLs'):
        # Reiniciando o arquivo 'output.txt'
        with open("output.txt", "w"):
            pass
        
        url = url_builder(termo)
        page_content = fetch_page(url)
        hrefs = extract_hrefs(page_content)
        
        if len(hrefs) == 1:
            st.error("Você deve digitar outro termo")
            return

        hrefs = [href for href in hrefs if "://" in href][:2]  # Limitando a 2 hrefs válidos

        for href in hrefs:
            st.write(f"Processando {href}...")
            body_text = extract_body_text(href)
            save_to_txt(body_text)

        st.success("Webscraping Finalizado!")

    # Campo de entrada para a pergunta ao modelo GPT-4
    question = st.text_input("Digite sua pergunta ao GPT-4:")

    # Botão para executar a pergunta ao modelo GPT-4
    if st.button('Perguntar ao GPT-4'):
        context = read_context_from_txt()
        answer = ask_gpt(question, context)
        st.write(f"Resposta: {answer}")

if __name__ == "__main__":
    main()
