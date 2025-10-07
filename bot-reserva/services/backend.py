# services/backend.py
import os
import aiohttp

API_BASE = os.getenv("API_BASE", "http://localhost:8080")

class BackendError(Exception):
    pass

# Função de teste usada para debugar um problema de import
def print_test():
    print("Backend service is reachable at", API_BASE)

async def create_user(nome: str, email: str, documento: str) -> dict:
    url = f"{API_BASE}/usuarios"
    payload = {"nome": nome, "email": email, "documento": documento}
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, json=payload) as resp:
            txt = await resp.text()
            if resp.status in (200, 201):
                try:
                    import json
                    return json.loads(txt)
                except Exception:
                    return {}
            if resp.status == 409:
                raise BackendError("Usuário já existe (409). " + txt)
            raise BackendError(f"Erro {resp.status} ao criar usuário: {txt}")

# Resolveu um problema pontual
__all__ = ["print_test", "create_user", "BackendError"]
