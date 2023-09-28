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
    # Removendo todos os scripts e styles do conteúdo
    for script in soup(["script", "style"]):
        script.extract()
    # Pegando o texto do corpo da página
    return soup.get_text()

def save_to_txt(text: str, filename="output.txt"):
    """
    Anexa o texto fornecido a um arquivo .txt.
    """
    with open(filename, "a") as file:
        file.write(text + "\n\n")

def main():
    # Reiniciando o arquivo 'output.txt'
    with open("output.txt", "w"):
        pass

    termo = input("Digite o termo de busca: ")
    url = url_builder(termo)
    page_content = fetch_page(url)
    hrefs = extract_hrefs(page_content)
    
    if len(hrefs) == 1:
        print("Você deve digitar outro termo")
        return

    hrefs = [href for href in hrefs if "://" in href][:2]  # Limitando a 5 hrefs válidos

    for href in hrefs:
        print(f"Processando {href}...")
        body_text = extract_body_text(href)
        save_to_txt(body_text)

    print("Finalizado!")

if __name__ == "__main__":
    main()
