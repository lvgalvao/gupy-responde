# Documentação fale com a Gupy

## Escopo do Projeto

1. Pegar o site da Gupy
2. O usuário pdoe passar o tipo de vaga que ele quer procurar
3. O sistema vai crawlear as 50 primeiras vagas
4. O sistema vai salvar o detlaha das vagas em um banco SQLlite
5. Vamos usar a API do ChatGPT para conversar com as vagas
6. O usuário vai poder conversar com as vagas e o sistema vai responder com as vagas que ele achou
7. Vamos usar o streamlit para ser a interface do usuário


## Fluxo

``` mermaid
sequenceDiagram
  autonumber
  User->>Streamlit: Digita o termo de interesse
  Streamlit->>httpx: Solicita na Gupy as vagas de "Desenvolvedor"
  Request->>BeutiSoup: Extrai os links das vagas
  BeutiSoup->>Request: Retorna os links das vagas
  Request->>httpx: Solicita os detalhes das vagas
  httpx->>BeutiSoup: Extrai os detalhes das vagas
```

## Módulo de request

### ::: app.get_data.url_builder

### Módulo de request do site da Gupy

## Módulo de parser do HTML

## Módulo do OPENAI

## Módulo do frontend