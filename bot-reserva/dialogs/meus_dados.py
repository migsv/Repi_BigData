from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext

from helpers.formatting import (
    format_currency,
    format_date,
    format_datetime,
    format_status,
)


class MeusDadosDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(MeusDadosDialog, self).__init__("MeusDadosDialog")
        self.user_state = user_state
        self.add_dialog(TextPrompt("cpfPrompt"))
        self.add_dialog(
            WaterfallDialog(
                "MeusDadosDialog",
                [self.pedir_cpf_step, self.mostrar_dados_step]
            )
        )
        self.initial_dialog_id = "MeusDadosDialog"

    async def pedir_cpf_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "cpfPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Informe seu CPF (somente números):"),
                retry_prompt=MessageFactory.text("CPF inválido, tente novamente.")
            )
        )

    async def mostrar_dados_step(self, step_context: WaterfallStepContext):
        cpf = "".join(filter(str.isdigit, str(step_context.result or "")))
        if not cpf:
            await step_context.context.send_activity(MessageFactory.text("CPF inválido."))
            return await step_context.end_dialog()

        from services.backend import (
            get_user_by_cpf,
            get_reservas_voo_by_cpf,
            get_reservas_hotel_by_cpf,
            BackendError
        )

        try:
            user = await get_user_by_cpf(cpf)
        except BackendError as e:
            await step_context.context.send_activity(MessageFactory.text(str(e)))
            return await step_context.end_dialog()

        msg_user = (
            "🧾 Seus dados\n"
            f"Nome: {user.get('nome')}\n"
            f"Email: {user.get('email')}\n"
            f"Telefone: {user.get('telefone')}\n"
            f"CPF: {user.get('cpf')}\n"
        )
        await step_context.context.send_activity(MessageFactory.text(msg_user))

        # Voos
        try:
            reservas_voo = await get_reservas_voo_by_cpf(cpf)
        except BackendError as e:
            await step_context.context.send_activity(MessageFactory.text(f"Erro ao listar voos: {e}"))
            reservas_voo = []

        if reservas_voo:
            await step_context.context.send_activity(
                MessageFactory.text(f"✈️ Reservas de voo ({len(reservas_voo)}):")
            )
            for r in reservas_voo:
                msg = (
                    f"- {r.get('origem')} → {r.get('destino')} ({r.get('companhiaAerea')})\n"
                    f"  Partida: {format_datetime(r.get('dataPartida'))} | "
                    f"Tarifa: {format_currency(r.get('preco'))} | "
                    f"Status: {format_status(r.get('status'))}"
                )
                await step_context.context.send_activity(MessageFactory.text(msg))
        else:
            await step_context.context.send_activity(
                MessageFactory.text("Nenhuma reserva de voo encontrada.")
            )

        # Hotéis
        try:
            reservas_hotel = await get_reservas_hotel_by_cpf(cpf)
        except BackendError as e:
            await step_context.context.send_activity(MessageFactory.text(f"Erro ao listar hotéis: {e}"))
            reservas_hotel = []

        if reservas_hotel:
            await step_context.context.send_activity(
                MessageFactory.text(f"🏨 Reservas de hotel ({len(reservas_hotel)}):")
            )
            for h in reservas_hotel:
                msg = (
                    f"- {h.get('nomeHotel')} ({h.get('localizacao')})\n"
                    f"  {format_date(h.get('dataCheckIn'))} → {format_date(h.get('dataCheckOut'))} | "
                    f"Total: {format_currency(h.get('precoTotal'))} | "
                    f"Status: {format_status(h.get('status'))}"
                )
                await step_context.context.send_activity(MessageFactory.text(msg))
        else:
            await step_context.context.send_activity(
                MessageFactory.text("Nenhuma reserva de hotel encontrada.")
            )

        return await step_context.end_dialog()
