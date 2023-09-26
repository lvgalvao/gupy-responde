import asyncio

import httpx
from bs4 import BeautifulSoup
from icecream import ic


def url_builder(termo: str) -> str:
    """
    Define a URL base e o termo de busca.

    args:
        termo (str): termo de busca
    """
    url_base = "https://portal.gupy.io/job-search/term="
    return f"{url_base}{termo}"


# Função assíncrona para obter conteúdo da página
async def fetch_page(url: str):
    """
    Obtém o conteúdo da página.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.content


# Função para extrair todos os hrefs
def extract_hrefs(page_content):
    """
    Extrai todos os hrefs da página.
    """
    soup = BeautifulSoup(page_content, "html.parser")
    links = soup.find_all("a")
    hrefs = [link.get("href") for link in links if link.get("href") is not None]
    return hrefs


# Função principal
def main():
    termo = input("Digite o termo de busca: ")
    url = url_builder(termo)
    page_content = asyncio.run(fetch_page(url))
    hrefs = extract_hrefs(page_content)
    if len(hrefs) == 1:
        print("Você deve digitar outro termo")
    else:
        for href in hrefs:
            print(href)


if __name__ == "__main__":
    main()
