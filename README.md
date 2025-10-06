# Repositorio | BigData
Repositório do projeto da aula de BigData | Ibmec

***

# Chatbot Inteligente de Reservas de Viagens (Hotéis e Voos)

## 1. Visão Geral do Projeto

Este projeto consiste no desenvolvimento de um **chatbot inteligente** cujo objetivo principal é permitir que os usuários pesquisem e **realizem reservas de hotéis e passagens aéreas**. A interação ocorre por meio de **mensagens naturais**, utilizando o Azure Bot Framework e o Processamento de Linguagem Natural (NLP) para interpretar as solicitações do usuário.

O chatbot é projetado para:

*   Entender as intenções do usuário.
*   Consultar hotéis e voos em APIs externas públicas/gratuitas.
*   Analisar o sentimento da conversa (satisfação ou frustração).
*   Armazenar métricas de uso e histórico de conversas.

## 2. Funcionalidades Chave (Escopo do Sistema)

O sistema possui as seguintes funcionalidades principais:

*   **Interação com o Usuário:** Disponível via Chat (WebChat, Teams, e Telegram opcional).
*   **Processamento de Linguagem Natural (NLP):** Utiliza **LUIS** (parte do Azure Cognitive Services) para processar linguagem, identificar intenções e extrair entidades. O chatbot deve entender pelo menos 5 intenções principais para ser aceito.
*   **Análise de Sentimento:** Utiliza **Text Analytics** (Azure Cognitive Services) para avaliar o sentimento do usuário.
*   **Consulta Externa:** Integração com APIs de Hotéis (como Hotelbeds ou Amadeus) e APIs de Voos (como Skyscanner ou Kiwi Tequila) para busca de disponibilidade. O critério de aceite exige integração com pelo menos 1 API de hotel e 1 de voo.
*   **Armazenamento de Dados:** Armazenamento do histórico de conversas e sentimentos analisados em **Azure Cosmos DB** ou **SQL Database**.

## 3. Arquitetura e Tecnologias

O sistema é construído majoritariamente sobre a plataforma Azure, garantindo escalabilidade e robustez.

| Componente | Tecnologia / Serviço |
| :--- | :--- |
| **Framework Principal** | **Azure Bot Service + Bot Framework SDK** |
| **NLP e Sentimento** | Azure Cognitive Services (LUIS e Text Analytics) |
| **Hospedagem / Backend** | Azure Functions (Serverless, essencial para lidar com picos de escalabilidade) |
| **Banco de Dados** | Azure Cosmos DB ou SQL Database |
| **Linguagens Suportadas** | C#, Java, Node.js, Python (para o Bot Framework) |
| **Relatórios (Opcional)** | Power BI (ou Power BI Embedded) para métricas |

O **fluxo de mensagem** padrão envolve o Bot Framework enviando a mensagem do usuário para o LUIS, que retorna a intenção e entidades. Em seguida, o Text Analytics avalia o sentimento. Uma **Azure Function** consulta a API apropriada e retorna as opções ao usuário, armazenando o histórico da conversa.

## 4. Requisitos de Qualidade (Não Funcionais)

O projeto possui requisitos de disponibilidade de **99,5%**, sendo suportado por uma arquitetura *Serverless* (Azure Functions) para garantir a **escalabilidade** necessária para lidar com picos de uso.
