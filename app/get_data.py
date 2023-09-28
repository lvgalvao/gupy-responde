import requests
from bs4 import BeautifulSoup

def url_builder(termo: str) -> str:
    """
    Define a URL base e o termo de busca.
    """
    url_base = "https://portal.gupy.io/job-search/term="
    return f"{url_base}{termo}"

def fetch_page(url: str):
    """
    Obtém o conteúdo da página usando 'requests'.
    """
    response = requests.get(url)
    return response.content

def extract_hrefs(page_content):
    """
    Extrai todos os hrefs da página.
    """
    soup = BeautifulSoup(page_content, "html.parser")
    links = soup.find_all("a")
    hrefs = [link.get("href") for link in links if link.get("href") is not None]
    return hrefs

def extract_body_text(url: str) -> str:
    """
    Extrai o texto do corpo da página de um URL.
    """
    page_content = fetch_page(url)
    soup = BeautifulSoup(page_content, "html.parser")
    
    # Encontre o h2 com o atributo data-testid específico
    h2_tag = soup.find("h2", {"data-testid": "section-Requisitos e qualificações-title"})
    
    if h2_tag:
        # Obter o próximo elemento div após o h2 encontrado
        div_tag = h2_tag.find_next("div")
        if div_tag:
            # Removendo todos os scripts e styles do conteúdo
            for script in div_tag(["script", "style"]):
                script.extract()
            
            # Retornar o texto da div
            return div_tag.get_text().strip()
    return ""


def save_to_txt(text: str, filename="output.txt"):
    """
    Anexa o texto fornecido a um arquivo .txt.
    """
    with open(filename, "a") as file:
        file.write(text + "\n\n")

def read_from_txt(filename="output.txt") -> str:
    """
    Lê o conteúdo do arquivo fornecido.
    """
    with open(filename, "r") as file:
        return file.read()

def process_term(termo: str, limit_hrefs: int = 10):
    """Processa o termo de busca e salva o conteúdo em output.txt."""
    
    # Reiniciando o arquivo 'output.txt'
    with open("output.txt", "w"):
        pass

    url = url_builder(termo)
    page_content = fetch_page(url)
    hrefs = extract_hrefs(page_content)
    
    if len(hrefs) <= 1:
        return False  # Indica que o termo de busca não retornou resultados suficientes

    hrefs = [href for href in hrefs if "://" in href][:limit_hrefs]

    for href in hrefs:
        body_text = extract_body_text(href)
        save_to_txt(body_text)
    
    return True  # Indica sucesso no processamento

def main():
    termo = input("Digite o termo de busca: ")
    
    if not process_term(termo):
        print("Você deve digitar outro termo")
        return

    print("Finalizado!")

if __name__ == "__main__":
    main()
