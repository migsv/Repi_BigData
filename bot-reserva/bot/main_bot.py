import re

from botbuilder.core import ActivityHandler, TurnContext, MessageFactory, UserState, ConversationState
from botbuilder.schema import ChannelAccount
from botbuilder.dialogs import Dialog
from helpers.DialogHelper import DialogHelper

from services.language_client import analyze_intent

class MainBot(ActivityHandler):
    MENU_OPTIONS = {
        "Cadastrar Cliente",
        "Reservar Voo",
        "Consultar Voo",
        "Cancelar Voo",
        "Meus Dados",
        "Reservar Hotel",
        "Consultar Hotel",
        "Cancelar Hotel",
        "Ferramentas Dev",
        "Ajuda",
    }
    INTENT_TO_OPTION = {
        "ComprarVoo": "Reservar Voo",
        "ConsultarVoo": "Consultar Voo",
        "CancelarVoo": "Cancelar Voo",
        "ReservarHotel": "Reservar Hotel",
        "ConsultarHotel": "Consultar Hotel",
        "CancelarHotel": "Cancelar Hotel",
    }
    INFORM_INTENTS = {}
    PROMPT_IGNORE = {
        "Opção 1",
        "Opção 2",
        "Opção 3",
        "Opção 4",
        "Opção 5",
        "Voltar ao Menu",
        "Voltar",
        "1",
        "2",
        "3",
        "4",
        "5",
    }
    UUID_REGEX = re.compile(r"^[0-9a-fA-F-]{32,36}$")
    NUMERIC_REGEX = re.compile(r"^\d+$")
    PIPE_PATTERN = re.compile(r"\|")
    INTENT_THRESHOLD = 0.65
    
    def __init__(self, 
                 dialog: Dialog,
                 conversation_state: ConversationState,
                 user_state: UserState
                 ):
        self.dialog = dialog
        self.conversation_state = conversation_state
        self.user_state = user_state
        self.intent_flag_accessor = self.conversation_state.create_property("IntentRoutingFlag")
        
    async def on_turn(self, turn_context):
        await super().on_turn(turn_context)
        
        #Save any state changes on conversation
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)
     
        
    async def on_message_activity(self, turn_context: TurnContext):
        await self._maybe_route_by_intent(turn_context)
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("MainDialogState")
        )

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Seja bem vindo(a) ao bot de atendimento da GranVoyage! Ajudaremos você a marcar a viagem dos seus sonhos.\n"
                    )
                )
                await DialogHelper.run_dialog(
                    self.dialog,
                    turn_context,
                    self.conversation_state.create_property("MainDialogState")
                )

    async def _maybe_route_by_intent(self, turn_context: TurnContext):
        text = (turn_context.activity.text or "").strip()
        allow_intents = await self.intent_flag_accessor.get(turn_context, True)
        if (not text
                or not allow_intents
                or text in self.MENU_OPTIONS
                or text in self.PROMPT_IGNORE
                or self.UUID_REGEX.match(text)
                or self.NUMERIC_REGEX.match(text)
                or self.PIPE_PATTERN.search(text)):
            return

        try:
            top_intent, score, entities = await analyze_intent(text)
        except Exception as exc:
            # Log localmente e segue com o fluxo padrão
            print(f"[LanguageService] Falha ao analisar texto: {exc}")
            return

        if score < self.INTENT_THRESHOLD:
            return

        mapped_option = self.INTENT_TO_OPTION.get(top_intent)
        if mapped_option:
            await turn_context.send_activity(
                MessageFactory.text(
                    f"Entendi que você deseja '{mapped_option}' (intent {top_intent}, {score:.0%})."
                )
            )
            turn_context.activity.text = mapped_option
            return

        extra_message = self.INFORM_INTENTS.get(top_intent)
        if extra_message:
            await turn_context.send_activity(
                MessageFactory.text(
                    f"Detectei a intenção '{top_intent}' ({score:.0%}). {extra_message}"
                )
            )
