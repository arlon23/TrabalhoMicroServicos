# Trabalho de Microsserviços

## Instalação Linux/WSL

Abra um terminal Linux/WSL e execute os seguintes comandos:

```bash
sudo apt-get update
sudo apt install python3
sudo apt install python3-pip
pip install flask
pip install -U Werkzeug
```

Para poder fazer o upload dos documentos é preciso criar as pastas uploads na raiz do projeto, e as pastas images e documents dentro da pasta uploads

```terminal
uploads
    images
    documents
```

## Executar o projeto

Para rodar o projeto basta rodar o comando:

```bash
python3 main.py
```
