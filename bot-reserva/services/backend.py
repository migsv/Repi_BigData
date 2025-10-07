# services/backend.py
import os
import aiohttp

API_BASE = os.getenv("API_BASE", "http://localhost:8080")

class BackendError(Exception):
    pass

# Função de teste usada para debugar um problema de import
def print_test():
    print("Backend service is reachable at", API_BASE)

async def _post_json(session, url, payload):
    resp = await session.post(url, json=payload)
    txt = await resp.text()
    return resp, txt

async def create_user(nome: str, email: str, documento: str, telefone: str) -> dict:
    url = f"{API_BASE}/usuarios"
    payload = {"nome": nome, "email": email, "documento": documento, "telefone": telefone}

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

def _to_iso_datetime(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return s
    if "T" not in s:
        return f"{s}T00:00:00"
    parts = s.split("T", 1)
    hm = parts[1]
    if len(hm.split(":")) == 2:  # HH:MM -> HH:MM:00
        return s + ":00"
    return s

def _parse_preco(preco_str: str) -> float:
    s = (preco_str or "").strip().replace("R$", "").replace(" ", "")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    return float(s)

async def create_reserva_voo(
    usuario_id: int,
    origem: str,
    destino: str,
    data_partida: str,
    preco_str: str,
    companhia_aerea: str | None = None,
    data_retorno: str | None = None,
    status: str = "PENDENTE",
) -> dict:
    url = f"{API_BASE}/reservas-voo"

    def _to_iso_datetime(s: str) -> str:
        s = (s or "").strip()
        if not s:
            return s
        if "T" not in s:
            return f"{s}T00:00:00"
        if len(s.split("T", 1)[1].split(":")) == 2:  # HH:MM -> HH:MM:00
            return s + ":00"
        return s

    def _parse_preco(preco: str) -> float:
        x = (preco or "").strip().replace("R$", "").replace(" ", "")
        if "," in x and "." in x:
            x = x.replace(".", "").replace(",", ".")
        elif "," in x:
            x = x.replace(",", ".")
        return float(x)

    payload = {
        # 👇 aqui está a mudança crucial:
        "usuario": {"id": int(usuario_id)},
        "origem": origem,
        "destino": destino,
        "dataPartida": _to_iso_datetime(data_partida),
        "preco": _parse_preco(preco_str),
        "status": status,
    }
    if companhia_aerea:
        payload["companhiaAerea"] = companhia_aerea
    if data_retorno:
        payload["dataRetorno"] = _to_iso_datetime(data_retorno)

    import aiohttp, json
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
                raise BackendError("Reserva já existe (409). " + txt)
            raise BackendError(f"Erro {resp.status} ao criar reserva de voo: {txt}")
