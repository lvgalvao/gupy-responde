import requests
from bs4 import BeautifulSoup
import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define suas credenciais de API
openai.api_key = os.getenv("OPENAI_API_KEY")

def url_builder(termo: str) -> str:
    url_base = "https://portal.gupy.io/job-search/term="
    return f"{url_base}{termo}"

def fetch_page(url: str):
    response = requests.get(url)
    return response.content

def extract_hrefs(page_content):
    soup = BeautifulSoup(page_content, "html.parser")
    links = soup.find_all("a")
    hrefs = [link.get("href") for link in links if link.get("href") is not None]
    return hrefs

def extract_body_text(url: str) -> str:
    page_content = fetch_page(url)
    soup = BeautifulSoup(page_content, "html.parser")
    
    h2_tag = soup.find("h2", {"data-testid": "section-Requisitos e qualificações-title"})
    
    if h2_tag:
        div_tag = h2_tag.find_next("div")
        if div_tag:
            for script in div_tag(["script", "style"]):
                script.extract()
            return div_tag.get_text().strip()
    return ""

def process_term(termo: str, limit_hrefs: int = 10):
    url = url_builder(termo)
    page_content = fetch_page(url)
    hrefs = extract_hrefs(page_content)
    
    if len(hrefs) <= 1:
        return False, []  # Indica que o termo de busca não retornou resultados suficientes

    hrefs = [href for href in hrefs if "://" in href][:limit_hrefs]
    results = []
    for href in hrefs:
        body_text = extract_body_text(href)
        results.append(body_text)
    return True, results

def ask_gpt(question, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": context},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message['content'].strip()

def main():
    st.title("Fale com a Gupy!")
    termo = st.text_input("Digite a vaga que procura: (ex: desenvolvedor)")

    if st.button('Raspar URLs'):
        success, results = process_term(termo)
        if not success:
            st.error("Você deve digitar outro termo")
        else:
            st.session_state['results'] = results
            st.success("Webscraping Finalizado!")

    if 'results' in st.session_state:
        context = "\n".join(st.session_state['results'])
        question = st.text_input("Digite sua pergunta a Gupy: (ex: Quais requisitos para a vaga?)")
        if st.button('Perguntar ao GPT-3.5'):
            answer = ask_gpt(question, context)
            st.write(f"Resposta: {answer}")

if __name__ == "__main__":
    main()
