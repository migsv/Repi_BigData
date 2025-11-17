from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory, ConversationState
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice

from dialogs.cadastrar_cliente import CadastrarClienteDialog
from dialogs.reservar_voo import ReservarVooDialog
from dialogs.consultar_voo import ConsultarVooDialog
from dialogs.cancelar_voo import CancelarVooDialog
from dialogs.reservar_hotel import ReservarHotelDialog
from dialogs.consultar_hotel import ConsultarHotelDialog
from dialogs.cancelar_hotel import CancelarHotelDialog
from dialogs.dev_tools_dialog import DevToolsDialog
from dialogs.meus_dados import MeusDadosDialog


class MainDialog(ComponentDialog):
    def __init__(self, user_state: UserState, conversation_state: ConversationState):
        super(MainDialog, self).__init__("MainDialog")
        self.user_state = user_state
        self.intent_flag_accessor = conversation_state.create_property("IntentRoutingFlag")

        # Prompts e diálogos registrados
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(CadastrarClienteDialog(self.user_state))
        self.add_dialog(ReservarVooDialog(self.user_state))
        self.add_dialog(ConsultarVooDialog(self.user_state))
        self.add_dialog(CancelarVooDialog(self.user_state))
        self.add_dialog(ReservarHotelDialog(self.user_state))
        self.add_dialog(ConsultarHotelDialog(self.user_state))
        self.add_dialog(CancelarHotelDialog(self.user_state))
        self.add_dialog(MeusDadosDialog(self.user_state))
        self.add_dialog(DevToolsDialog(self.user_state))

        # Fluxo principal
        self.add_dialog(
            WaterfallDialog(
                "MainDialog",
                [ self.prompt_option_step, self.process_option_step, self.restart_step ]
            )
        )
        self.initial_dialog_id = "MainDialog"

    async def prompt_option_step(self, step_context: WaterfallStepContext):
        await self.intent_flag_accessor.set(step_context.context, True)
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Escolha a opção desejada:"),
                choices=[
                    Choice("Cadastrar Cliente"),
                    Choice("Reservar Voo"),
                    Choice("Consultar Voo"),
                    Choice("Cancelar Voo"),
                    Choice("Meus Dados"),
                    Choice("Reservar Hotel"),
                    Choice("Consultar Hotel"),
                    Choice("Cancelar Hotel"),
                    Choice("Ferramentas Dev"),
                    Choice("Ajuda"),
                ]

            )
        )

    async def process_option_step(self, step_context: WaterfallStepContext):
        option = step_context.result.value

        if option != "Ajuda":
            await self.intent_flag_accessor.set(step_context.context, False)

        if option == "Cadastrar Cliente":
            return await step_context.begin_dialog("CadastrarClienteDialog")
        if option == "Reservar Voo":
            return await step_context.begin_dialog("ReservarVooDialog")
        if option == "Consultar Voo":
            return await step_context.begin_dialog("ConsultarVooDialog")
        if option == "Cancelar Voo":
            return await step_context.begin_dialog("CancelarVooDialog")
        if option == "Reservar Hotel":
            return await step_context.begin_dialog("ReservarHotelDialog")
        if option == "Consultar Hotel":
            return await step_context.begin_dialog("ConsultarHotelDialog")
        if option == "Cancelar Hotel":
            return await step_context.begin_dialog("CancelarHotelDialog")
        if option == "Meus Dados":
            return await step_context.begin_dialog("MeusDadosDialog")
        if option == "Ferramentas Dev":
            return await step_context.begin_dialog("DevToolsDialog")
        if option == "Ajuda":
            await step_context.context.send_activity(
                MessageFactory.text(
                    "Use os botões ou digite frases livres como 'quero reservar um voo' ou 'cancelar hotel'."
                )
            )
            return await step_context.next(None)


    async def restart_step(self, step_context: WaterfallStepContext):
        return await step_context.replace_dialog("MainDialog")
