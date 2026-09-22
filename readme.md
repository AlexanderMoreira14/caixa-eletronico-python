# Caixa Eletrônico em Python

Sistema bancário desenvolvido em dupla para praticar lógica de programação e fundamentos da linguagem Python.
*(Nota de versão: O projeto iniciou utilizando arquivos JSON para armazenamento e foi recentemente refatorado de forma individual para uma arquitetura relacional robusta com SQLite).*

## Desenvolvedores

- Alexander Moreira — [@AlexanderMoreira14]
- Davi Ramos — [@donnyeram]

## ✨ Funcionalidades e CRUD Completo

- **Gestão de Contas:** Cadastro de novos usuários (INSERT), alteração de senha (UPDATE) e exclusão permanente de conta com limpeza de histórico (DELETE em cascata).
- **Operações Financeiras:** Depósitos, Saques e PIX (transferências entre contas) com validação de saldo em tempo real.
- **Extrato Bancário:** Registro individualizado de cada transação com data e hora na tabela de histórico, lido de forma dinâmica (SELECT).
- **Autenticação e Segurança:** Sistema de login com limite de tentativas para isolar as operações do usuário ativo.
- **Tratamento de Erros:** Prevenção contra entradas inválidas (letras onde deveriam ser números, valores negativos, etc).

## Tecnologias

- Python 3
- SQLite3
- JSON (Armazenamento estático utilizado na versão 1.0)
- Git e GitHub

## Como executar

1. Instale o Python.
2. Clone ou baixe o repositório.
3. Execute: python main.py. No terminal

*(O banco de dados `caixa_eletronico.db` e as tabelas necessárias serão criados automaticamente na primeira execução).*

## 🤖 Nota sobre Aprendizado e IA
Durante a evolução deste projeto (especificamente na migração de armazenamento estático em arquivos para um banco de dados relacional SQLite), utilizei inteligência artificial como tutor de estudos. O objetivo da IA não foi gerar o código por mim, mas sim me guiar passo a passo para entender na prática a lógica de arquitetura, a execução de comandos CRUD (Create, Read, Update, Delete) e como integrar consultas SQL nativas no Python.

