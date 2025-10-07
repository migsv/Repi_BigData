from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions, TextPrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice

class ReservarHotelDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ReservarHotelDialog, self).__init__("ReservarHotelDialog")
        self.user_state = user_state
        self.add_dialog(TextPrompt("matriculaPrompt"))   # agora Cidade
        self.add_dialog(TextPrompt("disciplinaPrompt"))  # agora Datas
        self.add_dialog(ChoicePrompt("horarioPrompt"))   # agora Tipo de Quarto
        self.add_dialog(
            WaterfallDialog(
                "ReservarHotelDialog",
                [
                    self.prompt_cidade_step,
                    self.prompt_datas_step,
                    self.prompt_quarto_step,
                    self.process_reserva_step
                ]
            )
        )
        self.initial_dialog_id = "ReservarHotelDialog"

    async def prompt_cidade_step(self, step_context: WaterfallStepContext):
        message = MessageFactory.text("Reservar Hotel (DEMO)\nInforme a cidade:")
        return await step_context.prompt("matriculaPrompt",
            PromptOptions(prompt=message, retry_prompt=MessageFactory.text("Informe a cidade:")))

    async def prompt_datas_step(self, step_context: WaterfallStepContext):
        step_context.values["cidade"] = str(step_context.result or "").strip()
        return await step_context.prompt("disciplinaPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Check-in | Check-out (dd/mm | dd/mm)"),
                retry_prompt=MessageFactory.text("Ex.: 10/11 | 12/11")
            ))

    async def prompt_quarto_step(self, step_context: WaterfallStepContext):
        step_context.values["datas"] = str(step_context.result or "").strip()
        return await step_context.prompt(
            "horarioPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Tipo de quarto:"),
                choices=[Choice("Standard"), Choice("Luxo"), Choice("Suíte")]
            )
        )

    async def process_reserva_step(self, step_context: WaterfallStepContext):
        cidade = step_context.values.get("cidade", "")
        datas  = step_context.values.get("datas", "")
        quarto = getattr(step_context.result, "value", step_context.result)
        msg = (
            "Reserva criada (DEMO)\n"
            f"Cidade: {cidade}\nDatas: {datas}\nQuarto: {quarto}\n"
            "Localizador: H-ABC123"
        )
        await step_context.context.send_activity(MessageFactory.text(msg))
        return await step_context.end_dialog()
