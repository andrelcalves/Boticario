# O Boticario

<p align="center">Aplicação para o processo seletivo para o grupo boticario 🚀</p>

<p align="center">
<img src="https://img.shields.io/static/v1?label=License&message=MIT&color=7159c1&plastic"/>
<img src="https://img.shields.io/static/v1?label=Version&message=0.0.0&color=7159c1&plastic"/>
</p>

## Tabela de conteúdos

<!--ts-->
* [Instalação](#instalação)
* [Rodando a aplicação](#iniciando)
* [Testes](#testes)
* [TODO's](#todo's)

<!--te-->

## Instalação

### Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:

* [Git](https://git-scm.com)
* [Python](https://www.python.org/) * Versão 3.9 ou superior
* [Poetry](https://python-poetry.org/docs/cli/)
* [Docker](https://www.docker.com/)

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

### 🎲 Rodando a aplicação - Ambiente de Desenvolvimento

```bash
# Clone este repositório
$ git clone <https://github.com/uesleicarvalhoo/boticario>

# Acesse a pasta do projeto no terminal/cmd
$ cd Boticario

# Caso queira iniciar o servidor de desenvolvimento, você precisa primeiro iniciar o banco de dados
$ docker-compose up database -d

# Instale as dependências
$ poetry install

# Copie o arquivo .env.example para .env e altere as configurações das variaveis para as suas configurações
$ cp .env.example .env

# Execute a aplicação em modo de desenvolvimento
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
$ make coverage
```
