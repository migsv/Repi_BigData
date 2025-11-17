# services/backend.py
import os
import aiohttp
import json

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

def _normalize_cpf(cpf: str) -> str:
    return "".join(filter(str.isdigit, (cpf or "")))

async def create_user(nome: str, email: str, telefone: str, cpf: str) -> dict:
    url = f"{API_BASE}/usuarios"
    payload = {"nome": nome, "email": email, "telefone": telefone, "cpf": _normalize_cpf(cpf)}

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
    usuario_cpf: str,
    origem: str,
    destino: str,
    data_partida: str,
    preco_str: str,
    companhia_aerea: str | None = None,
    data_retorno: str | None = None,
    status: str = "CONFIRMADA",
) -> dict:
    url = f"{API_BASE}/reservas-voo"

    payload = {
        "usuarioCpf": _normalize_cpf(usuario_cpf),
        "origem": origem,
        "destino": destino,
        "dataPartida": _to_iso_datetime(data_partida),
        "preco": _parse_preco(preco_str),
        "status": status or "CONFIRMADA",
    }
    if companhia_aerea:
        payload["companhiaAerea"] = companhia_aerea
    if data_retorno:
        payload["dataRetorno"] = _to_iso_datetime(data_retorno)

    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, json=payload) as resp:
            txt = await resp.text()
            if resp.status in (200, 201):
                try:
                    return json.loads(txt)
                except Exception:
                    return {}
            if resp.status == 409:
                raise BackendError("Reserva já existe (409). " + txt)
            raise BackendError(f"Erro {resp.status} ao criar reserva de voo: {txt}")

async def _safe_json(resp: aiohttp.ClientResponse):
    """
    Lê o corpo como texto e tenta converter para JSON puro.
    Evita retornar objetos com campos None quando o servidor envia strings.
    """
    txt = await resp.text()
    if not txt:
        return {}
    try:
        return json.loads(txt)
    except Exception:
        return {"_raw": txt}

async def get_user(user_id: str) -> dict:
    user_id = str(user_id).strip()
    url = f"{API_BASE}/usuarios/{user_id}"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await _safe_json(resp)
                if not data:
                    raise BackendError("Usuário não encontrado (resposta vazia).")
                return data
            if resp.status == 404:
                raise BackendError("Usuário não encontrado (404).")
            txt = await resp.text()
            raise BackendError(f"Erro {resp.status} ao buscar usuário: {txt}")

async def get_user_by_cpf(cpf: str) -> dict:
    cpf = _normalize_cpf(cpf)
    url = f"{API_BASE}/usuarios/cpf/{cpf}"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await _safe_json(resp)
                if not data:
                    raise BackendError("Usuário não encontrado (resposta vazia).")
                return data
            if resp.status == 404:
                raise BackendError("Usuário não encontrado (404).")
            txt = await resp.text()
            raise BackendError(f"Erro {resp.status} ao buscar usuário: {txt}")

async def get_reservas_voo_by_usuario(user_id: str) -> list[dict]:
    user_id = str(user_id).strip()
    url = f"{API_BASE}/reservas-voo/usuario/{user_id}"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await _safe_json(resp)
                if isinstance(data, dict):
                    return [data]
                return data or []
            if resp.status == 404:
                return []
            txt = await resp.text()
            raise BackendError(f"Erro {resp.status} ao listar reservas: {txt}")

async def get_reservas_voo_by_cpf(cpf: str) -> list[dict]:
    cpf = _normalize_cpf(cpf)
    url = f"{API_BASE}/reservas-voo/cpf/{cpf}"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await _safe_json(resp)
                if isinstance(data, dict):
                    return [data]
                return data or []
            if resp.status == 404:
                return []
            txt = await resp.text()
            raise BackendError(f"Erro {resp.status} ao listar reservas: {txt}")

async def cancel_reserva_voo(reserva_id: str) -> dict:
    url = f"{API_BASE}/reservas-voo/{reserva_id}/cancelar"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.patch(url) as resp:
            if resp.status in (200, 204):
                return await _safe_json(resp)
            txt = await resp.text()
            raise BackendError(f"Erro {resp.status} ao cancelar reserva: {txt}")

# --------- Hotel helpers ---------

async def create_reserva_hotel(
    usuario_cpf: str,
    nome_hotel: str,
    localizacao: str,
    data_checkin: str,
    data_checkout: str,
    preco_total: str | None = None,
    status: str = "CONFIRMADA",
) -> dict:
    url = f"{API_BASE}/reservas-hotel"
    payload = {
        "usuarioCpf": _normalize_cpf(usuario_cpf),
        "nomeHotel": nome_hotel,
        "localizacao": localizacao,
        "dataCheckIn": data_checkin,
        "dataCheckOut": data_checkout,
        "precoTotal": _parse_preco(preco_total) if preco_total else 0,
        "status": status or "CONFIRMADA",
    }
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, json=payload) as resp:
            txt = await resp.text()
            if resp.status in (200, 201):
                try:
                    return json.loads(txt)
                except Exception:
                    return {}
            raise BackendError(f"Erro {resp.status} ao criar reserva de hotel: {txt}")

async def get_reservas_hotel_by_cpf(cpf: str) -> list[dict]:
    cpf = _normalize_cpf(cpf)
    url = f"{API_BASE}/reservas-hotel/cpf/{cpf}"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await _safe_json(resp)
                if isinstance(data, dict):
                    return [data]
                return data or []
            if resp.status == 404:
                return []
            txt = await resp.text()
            raise BackendError(f"Erro {resp.status} ao listar reservas de hotel: {txt}")

async def cancel_reserva_hotel(reserva_id: str) -> dict:
    url = f"{API_BASE}/reservas-hotel/{reserva_id}/cancelar"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.patch(url) as resp:
            if resp.status in (200, 204):
                return await _safe_json(resp)
            txt = await resp.text()
            raise BackendError(f"Erro {resp.status} ao cancelar reserva de hotel: {txt}")

# --------- Developer helpers ---------

async def list_usuarios() -> list[dict]:
    url = f"{API_BASE}/usuarios"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await _safe_json(resp)
                if isinstance(data, dict):
                    return [data]
                return data or []
            txt = await resp.text()
            raise BackendError(f"Erro {resp.status} ao listar usuários: {txt}")

async def list_reservas_voo() -> list[dict]:
    url = f"{API_BASE}/reservas-voo"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await _safe_json(resp)
                if isinstance(data, dict):
                    return [data]
                return data or []
            txt = await resp.text()
            raise BackendError(f"Erro {resp.status} ao listar reservas de voo: {txt}")

async def list_reservas_hotel() -> list[dict]:
    url = f"{API_BASE}/reservas-hotel"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await _safe_json(resp)
                if isinstance(data, dict):
                    return [data]
                return data or []
            txt = await resp.text()
            raise BackendError(f"Erro {resp.status} ao listar reservas de hotel: {txt}")
