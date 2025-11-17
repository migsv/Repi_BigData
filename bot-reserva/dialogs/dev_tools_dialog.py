import asyncio
import json

from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext

from helpers.formatting import (
    format_currency,
    format_date,
    format_datetime,
    format_status,
)


class DevToolsDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(DevToolsDialog, self).__init__("DevToolsDialog")
        self.user_state = user_state
        self.add_dialog(
            WaterfallDialog(
                "DevToolsDialog",
                [self.exibir_info_step]
            )
        )
        self.initial_dialog_id = "DevToolsDialog"

    async def exibir_info_step(self, step_context: WaterfallStepContext):
        from services.backend import (
            list_usuarios,
            list_reservas_voo,
            list_reservas_hotel,
            BackendError
        )

        try:
            usuarios, reservas_voo, reservas_hotel = await asyncio.gather(
                list_usuarios(),
                list_reservas_voo(),
                list_reservas_hotel()
            )
        except BackendError as e:
            await step_context.context.send_activity(MessageFactory.text(f"Erro ao consultar backend: {e}"))
            return await step_context.end_dialog()
        except Exception as e:
            await step_context.context.send_activity(MessageFactory.text(f"Erro inesperado: {e}"))
            return await step_context.end_dialog()

        usuarios = self._sanitize_list(usuarios)
        reservas_voo = self._sanitize_list(reservas_voo)
        reservas_hotel = self._sanitize_list(reservas_hotel)

        await step_context.context.send_activity(
            MessageFactory.text(f"👥 Usuários cadastrados ({len(usuarios)}):")
        )
        for u in usuarios:
            msg = (
                f"- Nome: {u.get('nome')} | Email: {u.get('email')} | Telefone: {u.get('telefone')} | CPF: {u.get('cpf')}"
            )
            await step_context.context.send_activity(MessageFactory.text(msg))

        await step_context.context.send_activity(
            MessageFactory.text(f"✈️ Reservas de voo ({len(reservas_voo)}):")
        )
        for r in reservas_voo:
            msg = (
                f"- {r.get('origem')} → {r.get('destino')} ({r.get('companhiaAerea')}) | "
                f"CPF: {r.get('usuarioCpf')} | "
                f"Partida: {format_datetime(r.get('dataPartida'))} | "
                f"Valor: {format_currency(r.get('preco'))} | "
                f"Status: {format_status(r.get('status'))}"
            )
            await step_context.context.send_activity(MessageFactory.text(msg))

        await step_context.context.send_activity(
            MessageFactory.text(f"🏨 Reservas de hotel ({len(reservas_hotel)}):")
        )
        for h in reservas_hotel:
            msg = (
                f"- {h.get('nomeHotel')} ({h.get('localizacao')}) | CPF: {h.get('usuarioCpf')} | "
                f"Período: {format_date(h.get('dataCheckIn'))} → {format_date(h.get('dataCheckOut'))} | "
                f"Total: {format_currency(h.get('precoTotal'))} | "
                f"Status: {format_status(h.get('status'))}"
            )
            await step_context.context.send_activity(MessageFactory.text(msg))

        return await step_context.end_dialog()

    def _sanitize_list(self, data):
        cleaned = []
        for item in data or []:
            if isinstance(item, dict) and "_raw" in item:
                try:
                    cleaned.append(json.loads(item["_raw"]))
                except Exception:
                    continue
            else:
                cleaned.append(item)
        return cleaned
