# Usar a imagem base do AWS Lambda para Python 3.11
FROM python:3.12

# Atualizar o pip
RUN pip3 install --upgrade pip

WORKDIR /telegram_api

# Copiar o arquivo requirements.txt para o contêiner
COPY requirements.txt ./

# Instalar as dependências do Python
RUN pip3 install -r requirements.txt

# Copiar arquivos do código
COPY . .

# Definir o comando padrão para o Lambda
CMD [ "python3", "main.py" ]