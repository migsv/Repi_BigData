import os
import asyncio
from typing import Any, Dict, List, Optional, Tuple

from azure.ai.language.conversations import ConversationAnalysisClient
from azure.core.credentials import AzureKeyCredential


LANGUAGE_ENDPOINT = os.getenv("LANGUAGE_ENDPOINT")
LANGUAGE_KEY = os.getenv("LANGUAGE_KEY")
LANGUAGE_PROJECT = os.getenv("LANGUAGE_PROJECT")
LANGUAGE_DEPLOYMENT = os.getenv("LANGUAGE_DEPLOYMENT")

_CLIENT: Optional[ConversationAnalysisClient] = None


def _get_client() -> ConversationAnalysisClient:
    global _CLIENT
    if _CLIENT is None:
        if not all([LANGUAGE_ENDPOINT, LANGUAGE_KEY, LANGUAGE_PROJECT, LANGUAGE_DEPLOYMENT]):
            raise RuntimeError(
                "Configuração do Azure Language incompleta. "
                "Verifique LANGUAGE_ENDPOINT, LANGUAGE_KEY, LANGUAGE_PROJECT e LANGUAGE_DEPLOYMENT."
            )
        _CLIENT = ConversationAnalysisClient(
            LANGUAGE_ENDPOINT,
            AzureKeyCredential(LANGUAGE_KEY)
        )
    return _CLIENT


async def analyze_intent(
    text: str
) -> Tuple[str, float, List[Dict[str, Any]]]:
    """
    Analisa o texto informado no modelo de Conversational Language Understanding
    e devolve (intent, pontuação, entidades).
    """
    client = _get_client()
    body = {
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "participantId": "user",
                "id": "1",
                "text": text
            }
        },
        "parameters": {
            "projectName": LANGUAGE_PROJECT,
            "deploymentName": LANGUAGE_DEPLOYMENT,
            "stringIndexType": "Utf16CodeUnit",
        }
    }

    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, client.analyze_conversation, body)
    prediction = result["result"]["prediction"]
    top_intent = prediction.get("topIntent", "")
    intents = {item["category"]: item["confidenceScore"] for item in prediction.get("intents", [])}
    entities = prediction.get("entities", [])
    return top_intent, intents.get(top_intent, 0.0), entities
