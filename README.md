# Geração de arquivo json a partir de um BD

O presente script, escrito utilizando a linguagem de programação Python, foi criado com o intuito de extrair dados de um determinado 
Banco de Dados e escrevê-los em um arquivo json.

---

### Ferramentas

[![Generic badge](https://img.shields.io/badge/Python-3.8.5-blue.svg)](https://www.python.org/downloads/)
[![Generic badge](https://img.shields.io/badge/Oracle-18c%20XE-orange.svg)](https://www.oracle.com/br/database/technologies/appdev/xe.html)
[![Generic badge](https://img.shields.io/badge/Pycharm-2020.2%20Community%20Edition-green.svg)](https://www.jetbrains.com/pt-br/pycharm/download/)
[![Generic badge](https://img.shields.io/badge/json-JavaScript%20Object%20Notation-red.svg)](https://www.json.org/json-pt.html)

### Módulos/Bibliotecas Python
[![Generic badge](https://img.shields.io/badge/cx_Oracle-8.0.1-orange.svg)](https://cx-oracle.readthedocs.io/en/latest/index.html) Para criar a conexão com o Banco de Dados  
[![Generic badge](https://img.shields.io/badge/json-12.0.2-red.svg)](https://docs.python.org/3/library/json.html) Para converter os dicionários em objetos json

### Schema
[![Generic badge](https://img.shields.io/badge/Schema-HR-orange.svg)](https://docs.oracle.com/cd/B13789_01/server.101/b10771/scripts003.htm)  
Para a criação deste script, foi utilizado o HR schema, esquema de uma aplicação de Recursos Humanos criado pela Oracle, que tem como objetivo principal armazenar os 
registros de empregados de uma organização. Este esquema é bastante utilizado para demonstrar exemplos, exercícios de cursos e sites da internet.

**Instruções de como desbloquear o HR schema:** [Installing Sample Schemas](https://docs.oracle.com/database/121/COMSC/installation.htm#COMSC001)

---

### Arquivos no repositório
- **script.py -** Script Python onde contém toda a execução
- **estrutura.json -** Contém a estrutura do arquivo que deverá ser gerado
- **dados.json -** Arquivo gerado após a execucação do script.py
