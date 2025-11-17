from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice, ListStyle

from helpers.formatting import format_datetime, format_status


class CancelarVooDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(CancelarVooDialog, self).__init__("CancelarVooDialog")
        self.user_state = user_state
        self.add_dialog(TextPrompt("cpfPrompt"))
        self.add_dialog(ChoicePrompt("reservaPrompt"))
        self.add_dialog(
            WaterfallDialog(
                "CancelarVooDialog",
                [self.pedir_cpf_step, self.selecionar_reserva_step, self.cancelar_step]
            )
        )
        self.initial_dialog_id = "CancelarVooDialog"

    async def pedir_cpf_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "cpfPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Informe o CPF do titular das reservas:"),
                retry_prompt=MessageFactory.text("CPF inválido, tente novamente.")
            )
        )

    async def selecionar_reserva_step(self, step_context: WaterfallStepContext):
        cpf = "".join(filter(str.isdigit, str(step_context.result or "")))
        if not cpf:
            await step_context.context.send_activity(MessageFactory.text("CPF inválido. Operação cancelada."))
            return await step_context.end_dialog()
        step_context.values["cpf"] = cpf

        from services.backend import get_reservas_voo_by_cpf, BackendError
        try:
            reservas = await get_reservas_voo_by_cpf(cpf)
        except BackendError as e:
            await step_context.context.send_activity(MessageFactory.text(str(e)))
            return await step_context.end_dialog()

        reservas_ativas = [
            r for r in reservas if (r.get("status") or "").upper() != "CANCELADA"
        ]
        if not reservas_ativas:
            await step_context.context.send_activity(
                MessageFactory.text("Não encontrei reservas de voo disponíveis para cancelamento.")
            )
            return await step_context.end_dialog()

        step_context.values["reservas"] = reservas_ativas
        linhas = ["Escolha o voo para cancelar:"]
        choices = []
        for idx, r in enumerate(reservas_ativas, start=1):
            linhas.append(
                f"{idx}) {r.get('origem')} → {r.get('destino')} ({r.get('companhiaAerea')})\n"
                f"   Partida: {format_datetime(r.get('dataPartida'))} | Status: {format_status(r.get('status'))}"
            )
            choices.append(Choice(value=str(idx), synonyms=[str(idx), r.get("id")]))

        await step_context.context.send_activity(MessageFactory.text("\n".join(linhas)))
        return await step_context.prompt(
            "reservaPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Selecione a opção que deseja cancelar:"),
                choices=choices,
                style=ListStyle.hero_card,
            ),
        )

    async def cancelar_step(self, step_context: WaterfallStepContext):
        choice = step_context.result
        reservas = step_context.values.get("reservas", [])
        try:
            idx = int(choice.value) - 1
        except (TypeError, ValueError):
            await step_context.context.send_activity(
                MessageFactory.text("Opção inválida. Operação cancelada.")
            )
            return await step_context.end_dialog()

        if idx < 0 or idx >= len(reservas):
            await step_context.context.send_activity(
                MessageFactory.text("Opção inválida. Operação cancelada.")
            )
            return await step_context.end_dialog()

        reserva_id = reservas[idx].get("id")

        from services.backend import cancel_reserva_voo, BackendError
        try:
            await cancel_reserva_voo(reserva_id)
            await step_context.context.send_activity(
                MessageFactory.text("Reserva cancelada com sucesso!")
            )
        except BackendError as e:
            await step_context.context.send_activity(MessageFactory.text(f"Não foi possível cancelar: {e}"))
        except Exception as e:
            await step_context.context.send_activity(MessageFactory.text(f"Erro inesperado: {e}"))

        return await step_context.end_dialog()
