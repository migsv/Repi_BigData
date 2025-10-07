from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice

from dialogs.cadastrar_cliente import CadastrarClienteDialog
from dialogs.reservar_voo import ReservarVooDialog
from dialogs.visualizar_dados import VisualizarDadosDialog  # <-- novo


class MainDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(MainDialog, self).__init__("MainDialog")
        self.user_state = user_state

        # Prompts e diálogos registrados
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(CadastrarClienteDialog(self.user_state))
        self.add_dialog(ReservarVooDialog(self.user_state))
        self.add_dialog(VisualizarDadosDialog(self.user_state))     # <-- novo


        # Fluxo principal
        self.add_dialog(
            WaterfallDialog(
                "MainDialog",
                [ self.prompt_option_step, self.process_option_step, self.restart_step ]
            )
        )
        self.initial_dialog_id = "MainDialog"

    async def prompt_option_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Escolha a opção desejada:"),
                choices=[
                    Choice("Cadastrar Cliente"),
                    Choice("Reservar Voo"),
                    Choice("Meus Dados"),      # <-- novo
                    Choice("Ajuda"),
                ]

            )
        )

    async def process_option_step(self, step_context: WaterfallStepContext):
        option = step_context.result.value

        if option == "Cadastrar Cliente":
            return await step_context.begin_dialog("CadastrarClienteDialog")
        elif option == "Reservar Voo":
            return await step_context.begin_dialog("ReservarVooDialog")
        elif option == "Meus Dados":   # <-- novo
            return await step_context.begin_dialog("VisualizarDadosDialog")
        elif option == "Ajuda":
            await step_context.context.send_activity(
                MessageFactory.text("Opções: Cadastrar Cliente, Reservar Voo, Meus Dados.")
            )
            return await step_context.next(None)


    async def restart_step(self, step_context: WaterfallStepContext):
        return await step_context.replace_dialog("MainDialog")
