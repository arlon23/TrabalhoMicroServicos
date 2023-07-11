# Trabalho de Microsserviços

## Instalação Linux/WSL

* Abra um terminal Linux/WSL e execute os seguintes comandos:

```bash
sudo apt-get update
sudo apt install python3
sudo apt install python3-pip
pip install -r requirements.txt
```

* Para poder fazer o upload dos documentos é preciso criar as pastas uploads na raiz do projeto, e as pastas images e documents dentro da pasta uploads.

```terminal
uploads
    images
    documents
```

## Executar o projeto

Vá para o diretório raiz do projeto e execute o comando:

```bash
python3 main.py
```

## Documentação da API

A documentação e definição da API se encontra em `templates/File_API.yml` na raiz do projeto.
