from botbuilder.core import ActivityHandler, TurnContext, MessageFactory, UserState, ConversationState
from botbuilder.schema import ChannelAccount
from botbuilder.dialogs import Dialog
from helpers.DialogHelper import DialogHelper

from services.language_client import analyze_intent

class MainBot(ActivityHandler):
    MENU_OPTIONS = {"Cadastrar Cliente", "Reservar Voo", "Meus Dados", "Ajuda"}
    INTENT_TO_OPTION = {
        "ComprarVoo": "Reservar Voo",
        "ConsultarVoo": "Meus Dados",
    }
    INFORM_INTENTS = {
        "CancelarVoo": "Ainda não implementamos cancelamento de voos pelo bot. "
                       "Use um atendente ou aguarde as próximas versões.",
        "ReservarHotel": "O fluxo de reserva de hotel será habilitado em breve.",
        "ConsultarHotel": "Consulta de reservas de hotel ainda não está disponível.",
        "CancelarHotel": "Cancelamento de hotel ainda não foi implementado.",
    }
    INTENT_THRESHOLD = 0.65
    
    def __init__(self, 
                 dialog: Dialog,
                 conversation_state: ConversationState,
                 user_state: UserState
                 ):
        self.dialog = dialog
        self.conversation_state = conversation_state
        self.user_state = user_state
        
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
        if not text or text in self.MENU_OPTIONS:
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
