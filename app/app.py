# app.py

import streamlit as st
from get_data import process_term, read_from_txt
from chatgpt import ask_gpt

def main():
    st.title("Fale com a Gupy!")

    # Campo de entrada para o termo de pesquisa
    termo = st.text_input("Digite a vaga que procura: (ex: engenheiro de dados pleno)")

    # Botão para executar webscraping
    if st.button('Raspar URLs'):
        
        success = process_term(termo, limit_hrefs=10)  # Limitando a 2 hrefs válidos para o Streamlit
        
        if not success:
            st.error("Você deve digitar outro termo")
            return

        st.success("Webscraping Finalizado!")

    # Campo de entrada para a pergunta ao modelo GPT-4
    question = st.text_input("Digite sua pergunta a Gupy: (ex: Quais os 5 principais requisitos para a vaga?)")

    # Botão para executar a pergunta ao modelo GPT-4
    if st.button('Perguntar ao GPT-4'):
        context = read_from_txt()
        answer = ask_gpt(question, context)
        st.write(f"Resposta: {answer}")

if __name__ == "__main__":
    main()
