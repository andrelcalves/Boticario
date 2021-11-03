# O Boticario

<p align="center">Aplicação para o processo seletivo para o grupo boticario 🚀</p>

<p align="center">
<img src="https://img.shields.io/static/v1?label=License&message=MIT&color=7159c1&plastic"/>
<img src="https://img.shields.io/static/v1?label=Version&message=0.0.0&color=7159c1&plastic"/>
</p>

## Tabela de conteúdos

<!--ts-->
- [O Boticario](#o-boticario)
- [Tabela de conteúdos](#tabela-de-conteúdos)
- [Instalação](#instalação)
- [Pré-requisitos](#pré-requisitos)
- [Deploy](#deploy)
- [🎲 Rodando a aplicação](#-rodando-a-aplicação)
- [🎲 Contribuindo com o projeto](#-contribuindo-com-o-projeto)
- [Testes](#testes)
- [Melhorias](#melhorias)
<!--te-->

## Instalação

### Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:

- [Git](https://git-scm.com)
- [Python](https://www.python.org/) * Versão 3.9 ou superior
- [Poetry](https://python-poetry.org/docs/cli/)
- [Docker](https://www.docker.com/)

## Deploy

### 🎲 Rodando a aplicação

```bash
# Clone este repositório
$ git clone <https://github.com/uesleicarvalhoo/boticario>

# Acesse a pasta do projeto no terminal/cmd
$ cd Boticario

# Execute o comando para iniciar a aplicação
$ make compose

# O servidor inciará na porta:5000 * acesse <http://localhost:5000/>
# O servidor já conta com documentação integrada, disponível no endpoint /docs
```

### 🎲 Contribuindo com o projeto

```bash
# Clone este repositório
$ git clone <https://github.com/uesleicarvalhoo/boticario>

# Acesse a pasta do projeto no terminal/cmd
$ cd Boticario

# A aplicação está configurada para rodar com o PostgreSQL, você pode subir uma instancia com o Docker com o comando
$ docker-compose up database -d

# Instale as dependências
$ poetry install

# Inicie o pre-commit, ele vai rodar alguns testes e validações antes de realizar o commit para garantir a qualidade do código
$ pre-commit install

# Copie o arquivo .env.example para .env e altere as configurações das variaveis para as suas configurações
$ cp .env.example .env

# Faça suas alterações

# Formate o código
$ make format

# Garanta que os testes estão passando
$ make test

# Abra uma pull request e ela será analisada

# Dica: Você pode utilizar o comando abaixo para iniciar o servidor com o hot reload
$ make run

# O servidor inciará na porta:5000 * acesse <http://localhost:5000/>
```

### Testes

A aplicação possui testes automatizados, para roda-los é bem simples, apenas execute o comando

```bash
# Executa os testes
$ make test
```

E caso queira um reporte dos testes, você pode rodar o comando

```bash
# Gera o report sobre os testes
$ make coverage
```

### Melhorias

Alguns extras que podems ser adicionados na aplicação

- Escopos de autenticação para o Token JWT

- Rota para atualizar o Token

- Cache nos endpoints mais utilizados

- Pipeline para Deploy
