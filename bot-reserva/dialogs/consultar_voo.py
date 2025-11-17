from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext

from helpers.formatting import format_currency, format_datetime, format_status


class ConsultarVooDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ConsultarVooDialog, self).__init__("ConsultarVooDialog")
        self.user_state = user_state

        self.add_dialog(TextPrompt("cpfPrompt"))
        self.add_dialog(
            WaterfallDialog(
                "ConsultarVooDialog",
                [self.pedir_cpf_step, self.mostrar_dados_step]
            )
        )
        self.initial_dialog_id = "ConsultarVooDialog"

    async def pedir_cpf_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "cpfPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Informe seu CPF (somente números):"),
                retry_prompt=MessageFactory.text("CPF inválido. Digite apenas números.")
            )
        )

    async def mostrar_dados_step(self, step_context: WaterfallStepContext):
        cpf = "".join(filter(str.isdigit, str(step_context.result or "")))
        if not cpf:
            await step_context.context.send_activity(MessageFactory.text("CPF inválido. Operação cancelada."))
            return await step_context.end_dialog()

        from services.backend import (
            get_user_by_cpf,
            get_reservas_voo_by_cpf,
            BackendError
        )

        try:
            user = await get_user_by_cpf(cpf)
        except BackendError as e:
            await step_context.context.send_activity(MessageFactory.text(str(e)))
            return await step_context.end_dialog()

        try:
            reservas = await get_reservas_voo_by_cpf(cpf)
        except BackendError as e:
            await step_context.context.send_activity(MessageFactory.text(str(e)))
            reservas = []

        msg_user = (
            "🧾 Seus dados\n"
            f"Nome: {user.get('nome')}\n"
            f"Email: {user.get('email')}\n"
            f"Telefone: {user.get('telefone')}\n"
            f"CPF: {user.get('cpf')}\n"
        )
        await step_context.context.send_activity(MessageFactory.text(msg_user))

        if not reservas:
            await step_context.context.send_activity(MessageFactory.text("Você não possui reservas de voo."))
            return await step_context.end_dialog()

        for reserva in reservas:
            msg = (
                "✈️ Reserva de Voo\n"
                f"Código: {reserva.get('id')}\n"
                f"Rota: {reserva.get('origem')} → {reserva.get('destino')} ({reserva.get('companhiaAerea')})\n"
                f"Partida: {format_datetime(reserva.get('dataPartida'))}\n"
                f"Tarifa: {format_currency(reserva.get('preco'))}\n"
                f"Status: {format_status(reserva.get('status'))}\n"
            )
            await step_context.context.send_activity(MessageFactory.text(msg))

        return await step_context.end_dialog()
