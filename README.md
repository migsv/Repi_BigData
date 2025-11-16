# Repositorio | BigData
Repositório do projeto da aula de BigData | Ibmec

***

# Chatbot de Reservas (Bot + API)

## 1. Visão Geral

Esta entrega implementa um **chatbot de reservas** (Bot Framework SDK em Python) integrado a um **backend** (Spring Boot + **Azure Cosmos DB**). Não há mais uso de PostgreSQL.

O foco é permitir:

- **Cadastrar Cliente** (Nome, Email, Telefone).
- **Reservar Voo (Promoções)**: o bot exibe **3 ofertas**, o usuário escolhe uma, informa seu **ID** e a reserva é criada.
- **Meus Dados**: consulta por **ID** e exibe dados do usuário e **todas as reservas de voo** dele.

> O menu inicial é exibido automaticamente logo após a saudação.

## 2. Funcionalidades Entregues

- **Bot**
  - Menu principal com **Cadastrar Cliente**, **Reservar Voo**, **Meus Dados** e **Ajuda**.
  - **Cadastrar Cliente** → `POST /usuarios`.
  - **Reservar Voo (Promoções)** → mostra 3 opções; após escolha e ID, envia `POST /reservas-voo`.
  - **Meus Dados** → `GET /usuarios/{id}` e `GET /reservas-voo/usuario/{id}`.
  - > Ao concluir o cadastro, o bot exibe um **ID completo (UUID)**. Guarde esse valor e cole-o sempre que for reservar voos ou consultar “Meus Dados”.

- **Backend**
  - **Usuários**: criação e consulta.
  - **Reservas de Voo**: criação e listagem por usuário.
  - Persistência em **Azure Cosmos DB** (configuração em `ChatBot-API/src/main/resources/application.properties`).

---

## 3. Como Rodar

### 3.1 Backend (Spring Boot + Cosmos DB)

1. Garanta que a conta do **Azure Cosmos DB** esteja ativa e que `application.properties` contenha `uri`, `key` e `database` corretos.
2. Em um terminal na pasta `ChatBot-API`, execute:
   ```powershell
   .\mvnw spring-boot:run
   ```
3. Os endpoints ficarão disponíveis em `http://localhost:8080/api` (por exemplo, `http://localhost:8080/api/usuarios`).

### 3.2 Bot (Python)

1. Vá para a pasta `bot-reserva` e configure o ambiente virtual:
   ```powershell
   py -3.10 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
2. Aponte o bot para o backend (o `.env` já usa o mesmo valor) e execute-o:
   ```powershell
   $env:API_BASE = "http://localhost:8080/api"
   python app.py
   ```
   > Sempre inclua o sufixo `/api`, pois o backend expõe seus recursos nesse contexto.

### 3.3 Bot Framework Emulator

No **Bot Framework Emulator**, conecte-se em:
```
http://localhost:3978/api/messages
```

**Ordem recomendada:** Cosmos DB disponível → backend (`.\mvnw spring-boot:run`) → bot Python (`python app.py`) → Bot Framework Emulator.
