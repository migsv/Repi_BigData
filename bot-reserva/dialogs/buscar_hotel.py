from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions, TextPrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice

class BuscarHotelDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(BuscarHotelDialog, self).__init__("BuscarHotelDialog")
        self.user_state = user_state
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "BuscarHotelDialog",
                [ self.prompt_busca_step, self.process_busca_step ]
            )
        )
        self.initial_dialog_id = "BuscarHotelDialog"

    async def prompt_busca_step(self, step_context: WaterfallStepContext):
        message = MessageFactory.text(
            "Buscar Hotel (DEMO)\nCidade | Check-in dd/mm | Check-out dd/mm | Hóspedes"
        )
        prompt_option = PromptOptions(
            prompt=message,
            retry_prompt=MessageFactory.text("Ex.: Rio de Janeiro | 10/11 | 12/11 | 2")
        )
        return await step_context.prompt(TextPrompt.__name__, prompt_option)

    async def process_busca_step(self, step_context: WaterfallStepContext):
        bruto = str(step_context.result or "")
        partes = [p.strip() for p in bruto.split("|")]
        cidade  = partes[0] if len(partes) > 0 else ""
        checkin = partes[1] if len(partes) > 1 else ""
        checkout= partes[2] if len(partes) > 2 else ""
        hosp   = partes[3] if len(partes) > 3 else ""
        lista = (
            f"Resultados em {cidade} ({checkin}→{checkout}, {hosp} hósp.):\n"
            "1) Hotel Atlântico ★★★★ R$ 420/noite\n"
            "2) Copacabana Plaza ★★★★ R$ 480/noite\n"
            "3) Rio Sun Suites ★★★ R$ 310/noite\n"
            "Use 'Reservar Hotel' no menu para simular a reserva."
        )
        await step_context.context.send_activity(MessageFactory.text(lista))
        return await step_context.end_dialog()
