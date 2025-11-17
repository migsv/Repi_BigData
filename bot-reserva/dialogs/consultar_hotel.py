from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext

from helpers.formatting import format_currency, format_date, format_status


class ConsultarHotelDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ConsultarHotelDialog, self).__init__("ConsultarHotelDialog")
        self.user_state = user_state
        self.add_dialog(TextPrompt("cpfPrompt"))
        self.add_dialog(
            WaterfallDialog(
                "ConsultarHotelDialog",
                [self.pedir_cpf_step, self.mostrar_reservas_step]
            )
        )
        self.initial_dialog_id = "ConsultarHotelDialog"

    async def pedir_cpf_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "cpfPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Informe o CPF para consultar as reservas de hotel:"),
                retry_prompt=MessageFactory.text("CPF inválido, tente novamente.")
            )
        )

    async def mostrar_reservas_step(self, step_context: WaterfallStepContext):
        cpf = "".join(filter(str.isdigit, str(step_context.result or "")))
        if not cpf:
            await step_context.context.send_activity(MessageFactory.text("CPF inválido."))
            return await step_context.end_dialog()

        from services.backend import get_reservas_hotel_by_cpf, BackendError
        try:
            reservas = await get_reservas_hotel_by_cpf(cpf)
        except BackendError as e:
            await step_context.context.send_activity(MessageFactory.text(str(e)))
            return await step_context.end_dialog()

        if not reservas:
            await step_context.context.send_activity(
                MessageFactory.text("Nenhuma reserva de hotel encontrada para este CPF.")
            )
            return await step_context.end_dialog()

        for reserva in reservas:
            msg = (
                "🏨 Reserva de Hotel\n"
                f"Código: {reserva.get('id')}\n"
                f"Hotel: {reserva.get('nomeHotel')} ({reserva.get('localizacao')})\n"
                f"Período: {format_date(reserva.get('dataCheckIn'))} → {format_date(reserva.get('dataCheckOut'))}\n"
                f"Total: {format_currency(reserva.get('precoTotal'))}\n"
                f"Status: {format_status(reserva.get('status'))}\n"
            )
            await step_context.context.send_activity(MessageFactory.text(msg))

        return await step_context.end_dialog()
