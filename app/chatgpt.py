import openai
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define suas credenciais de API
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_context_from_txt(filename="output.txt"):
    """Lê o contexto do arquivo .txt fornecido."""
    with open(filename, "r") as file:
        return file.read()

def ask_gpt(question, context):
    """Faz uma pergunta ao modelo GPT da OpenAI com um contexto específico."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": context},
            {"role": "user", "content": question}
        ],
        max_tokens=400  # Limite a resposta para 400 tokens
    )
    return response.choices[0].message['content'].strip()

def main():
    context = read_context_from_txt()
    while True:
        question = input("Digite sua pergunta (ou 'sair' para terminar): ")
        if question.lower() == 'sair':
            break
        answer = ask_gpt(question, context)
        print(f"Resposta: {answer}\n")

if __name__ == "__main__":
    main()
