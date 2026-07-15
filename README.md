# Projeto de PSI - Sistema de Lembretes e Anotações

---

## Equipe

- Andresa dos Santos Dantas
- Michel Jackson dos Santos Bezerra de Medeiros
- Rafael Fernandes Martins
- Valessia Juliany de Medeiros Linhares

---

## Proposta

- O projeto consiste no desenvolvimento de uma aplicação web utilizando o Flask, com o objetivo de auxiliar usuários na organização de suas tarefas diárias por meio de um sistema de lembretes e anotações.
- A aplicação permitirá que os usuários realizem cadastro e login, criando um ambiente onde poderão registrar, visualizar, editar e excluir lembretes de forma simples e rápida, como uma agenda.
- O sistema será acessado por meio de páginas web interativas.
- O principal foco da aplicação é oferecer uma solução prática para o gerenciamento de informações pessoais, evitando que tarefas importantes sejam esquecidas no dia a dia.

---

## Problema

- No dia a dia, é comum esquecer tarefas, compromissos ou até ideias importantes. Muitas vezes isso acontece por falta de organização ou por não ter um lugar simples para anotar essas coisas rapidamente. Além disso, nem todo mundo usa aplicativos mais complexos de produtividade, o que acaba dificultando ainda mais o controle das atividades.

---

## Justificativa

- Além de resolver o problema proposto, o projeto também permite aplicar conceitos importantes do desenvolvimento web, como autenticação de usuários, proteção de rotas, integração com banco de dados utilizando SQLAlchemy e organização da aplicação por meio do framework Flask.

---

## Funcionalidades

- Cadastro de usuários  
- Login  
- Logout
- Autenticação de usuários com flask-login
- Criar lembretes  
- Listar lembretes  
- Editar lembretes  
- Excluir lembretes  
- Filtro de lembretes

## Banco de Dados

- Banco de dados SQLite
- Utilização do SQLAlchemy como ORM
- Modelos de Usuário e Lembretes
- Relacionamentos utilizando chaves estrangeiras
- Operações CRUD

---

## Tecnologias

- Python
- Flask
- Flask-Login
- SQLAlchemy
- SQLite
- HTML
- CSS
- JavaScript

---

## Estrutura

A aplicação terá:

- Rotas para cada página
- Templates HTML utilizando um template base
- Arquivos estáticos (CSS, JavaScript e imagens)
- Formulários para cadastro, login e gerenciamento de lembretes
- Métodos GET e POST
- Rotas parametrizadas
- Filtros utilizando query string
- Autenticação com Flask-Login
- Proteção de rotas
- SQLAlchemy

---

## Como rodar

- Instale a pasta correspondente à aplicação e descompacte ela
- Inicie um ambiente virtual antes de rodar a aplicação
- Pegue o localhost e se redirecione de acordo com as rotas (comece com a /cadastro)
