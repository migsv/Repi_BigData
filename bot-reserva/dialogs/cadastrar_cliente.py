from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions, TextPrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice

class CadastrarClienteDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(CadastrarClienteDialog, self).__init__("CadastrarClienteDialog")
        self.user_state = user_state
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "CadastrarClienteDialog",
                [ self.prompt_cadastro_step, self.process_cadastro_step ]
            )
        )
        self.initial_dialog_id = "CadastrarClienteDialog"

    async def prompt_cadastro_step(self, step_context: WaterfallStepContext):
        message = MessageFactory.text(
            "Cadastro de Cliente (DEMO)\nInforme: Nome | Email | Documento"
        )
        prompt_option = PromptOptions(
            prompt=message,
            retry_prompt=MessageFactory.text("Formato inválido. Ex.: Ana | ana@email.com | 123.456.789-00")
        )
        return await step_context.prompt(TextPrompt.__name__, prompt_option)

    async def process_cadastro_step(self, step_context: WaterfallStepContext):
        bruto = str(step_context.result or "")
        partes = [p.strip() for p in bruto.split("|")]
        nome = partes[0] if len(partes) > 0 else ""
        email = partes[1] if len(partes) > 1 else ""
        doc = partes[2] if len(partes) > 2 else ""
        await step_context.context.send_activity(
            MessageFactory.text(f"Cliente cadastrado (DEMO)\nNome: {nome}\nEmail: {email}\nDocumento: {doc}")
        )
        return await step_context.end_dialog()
