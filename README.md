# Repositorio | BigData
Repositório do projeto da aula de BigData | Ibmec

***

# Chatbot de Reservas (Bot + API)

## 1. Visão Geral

Esta entrega implementa um **chatbot de reservas** (Bot Framework SDK em Python) integrado a um **backend** (Spring Boot + PostgreSQL).

O foco é permitir:

- **Cadastrar Cliente** (Nome, Email, Telefone).
- **Reservar Voo (Promoções)**: o bot exibe **3 ofertas**, o usuário escolhe uma, informa seu **ID** e a reserva é criada.
- **Meus Dados**: consulta por **ID** e exibe dados do usuário e **todas as reservas de voo** dele.

> O menu inicial é exibido **automaticamente** após a saudação.

## 2. Funcionalidades Entregues

- **Bot**
  - Menu principal com **Cadastrar Cliente**, **Reservar Voo**, **Meus Dados** e **Ajuda**.
  - **Cadastrar Cliente** → `POST /usuarios`.
  - **Reservar Voo (Promoções)** → mostra 3 opções; após escolha e ID, envia `POST /reservas-voo`.
  - **Meus Dados** → `GET /usuarios/{id}` e `GET /reservas-voo/usuario/{id}`.

- **Backend**
  - **Usuários**: criação e consulta.
  - **Reservas de Voo**: criação e listagem por usuário.
  - Persistência em **PostgreSQL** (Docker).

---

## 3. Como Rodar

--------------------------------  
**Parte do Bot:**

Entrar na pasta `bot-reserva`

```powershell
# se ainda não existir a venv:
py -3.10 -m venv .venv

# ativar a venv
.\.venv\Scripts\Activate.ps1

# instalar dependências (use requirements.txt se existir)
python -m pip install --upgrade pip
pip install -r requirements.txt  # se houver esse arquivo
```

Defina a URL do backend e execute o bot:

```powershell
$env:API_BASE="http://localhost:8080"
python app.py
```

No **Bot Framework Emulator**, conectar em:
```
http://localhost:3978/api/messages
```
-----------------------------------

**Parte do Back:**

Inicia Docker Desktop  
No PowerShell:
```powershell
docker run --name pg-bigdata -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=dudumimi21 -e POSTGRES_DB=BigData -p 5432:5432 -d postgres:16
```

Na pasta `ChatBot-API`:
```powershell
.\mvnw spring-boot:run
```
-----------------------
