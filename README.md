# Repositorio | BigData
Repositório do projeto da aula de BigData | Ibmec

***

# Chatbot de Reservas (Bot + API)

## 1. Visão Geral

Esta entrega implementa um **chatbot de reservas** (Bot Framework SDK em Python) integrado a um **backend** (Spring Boot + **Azure Cosmos DB**). Não há mais uso de PostgreSQL.

O foco é permitir que o usuário realize toda a jornada de reserva/consulta/cancelamento usando apenas o **CPF** como identificador principal.
O bot aceita tanto comandos por menu quanto por linguagem natural (intents no Azure AI Language).

## 2. Funcionalidades Entregues

- **Bot**
  - Menu principal com **Cadastrar Cliente**, **Reservar/Consultar/Cancelar Voo**, **Reservar/Consultar/Cancelar Hotel**, **Ferramentas Dev** e **Ajuda**.
  - Integração com **Conversational Language Understanding** (Azure AI Language). Intents suportadas: `ComprarVoo`, `ConsultarVoo`, `CancelarVoo`, `ReservarHotel`, `ConsultarHotel`, `CancelarHotel`.
  - Todo fluxo pede o **CPF** do cliente; IDs internos ficam transparentes.
  - Botão “Ferramentas Dev” lista, dentro do chat, todos os usuários e reservas existentes (voos e hotéis) – útil em testes.
  - O cadastro exige CPF único (o bot alerta se já existir) e cada etapa usa mensagens e botões mais descritivos.

- **Backend**
  - **Usuários**: criação e consulta (por ID ou CPF) com validação de duplicidade.
  - **Reservas de Voo**: criação, listagem geral, listagem por CPF e cancelamento.
  - **Reservas de Hotel**: criação, listagem geral, listagem por CPF e cancelamento.
  - “Seeder” (`DataSeeder`) popula automaticamente usuários e reservas de exemplo ao subir a API (caso esteja vazia).
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
