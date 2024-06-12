## Ambiente de desenvolvimento

1. Para criar o ambiente, digite no terminal: ```python -m venv venv```
2. Para ativar o ambiente, digite no terminal: ```source venv/bin/activate```
3. Para instalar as dependências, digite no terminal: ```pip install -r requirements.txt```
4. Para desativar o ambiente, digite no terminal: ```deactivate```

- Caso instale uma nova dependência, digite no terminal: ```pip freeze > requirements.txt```

## Como executar

1. Na pasta raiz do projeto, execute o comando: ```docker compose up -d``` para subir os containers dos dois bancos de dados, um contendo todo o conteúdo e outro vazio, à ser preenchido na segunda parte da aplicação.
2. Execute o script da primeira parte da aplicação, digitando o seguinte comando na pasta raiz da aplicação: ```python first_step/script.py```
3. Execute o script da segunda parte da aplicação, digitando o seguinte comando na pasta raiz da aplicação: ```python second_step/script.py``` 