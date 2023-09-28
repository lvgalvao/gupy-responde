import streamlit as st

def main():
    st.title("Aplicação Streamlit")

    # Dois campos de entrada de texto
    input1 = st.text_input("Digite o primeiro valor:")
    input2 = st.text_input("Digite o segundo valor:")

    # Suponha que a "resposta" seja a concatenação dos dois inputs (modifique esta lógica conforme necessário)
    resposta = input1 + " " + input2

    # Mostrando a resposta
    if st.button('Gerar Resposta'):
        st.write("Resposta:", resposta)

if __name__ == "__main__":
    main()
