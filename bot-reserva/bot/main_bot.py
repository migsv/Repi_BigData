from botbuilder.core import ActivityHandler, TurnContext, MessageFactory, UserState, ConversationState
from botbuilder.schema import ChannelAccount
from botbuilder.dialogs import Dialog
from helpers.DialogHelper import DialogHelper


class MainBot(ActivityHandler):
    
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
                        f"Seja bem vindo(a) ao bot de atendimento do IBMEC EVENTOS "
                        f"Digite uma mensagem para iniciar o atendimento"
                    )
                )