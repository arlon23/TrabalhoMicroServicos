Procedimentos Linux/WSL

Verificar se possui python3 instalado

instalar python pip: sudo apt install python3-pip

instalar flask: pip install flask

instalar pacote Werkzeug: pip install -U Werkzeug


Para poder fazer o upload dos documento é preciso criar as pastas uploads na raiz do projeto, e as pastas images e documents dentro da pasta uploads

uploads
    images
    documents


Para rodar o projeto basta rodar o comando: python3 main.py