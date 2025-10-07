from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext

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
            "Cadastro de Cliente\nInforme: Nome | Email | Documento | Telefone"
        )
        prompt_option = PromptOptions(
            prompt=message,
            retry_prompt=MessageFactory.text("Formato inválido. Ex.: Ana | ana@email.com | 123.456.789-00 | (11) 91234-5678")
        )
        return await step_context.prompt(TextPrompt.__name__, prompt_option)

    async def process_cadastro_step(self, step_context: WaterfallStepContext):
        bruto = str(step_context.result or "")
        partes = [p.strip() for p in bruto.split("|")]
        nome = partes[0] if len(partes) > 0 else ""
        email = partes[1] if len(partes) > 1 else ""
        doc = partes[2] if len(partes) > 2 else ""
        tel = partes[3] if len(partes) > 3 else ""

        if not (nome and email and doc and tel):
            await step_context.context.send_activity(
                MessageFactory.text("Formato inválido. Tente: Nome | Email | Documento | Telefone")
            )
            return await step_context.end_dialog()

        # Integra com o backend
        # import tardio (evita qualquer ordem de import chata)
        from services.backend import create_user, BackendError
        try:
            user = await create_user(nome, email, doc, tel)
            msg = (
                "Cliente cadastrado com sucesso!\n"
                f"ID: {user.get('id')}\n"
                f"Nome: {user.get('nome') or user.get('name')}\n"
                f"Email: {user.get('email')}\n"
                f"Documento: {user.get('documento') or user.get('document')}\n"
                f"Telefone: {user.get('telefone') or user.get('phone')}"
            )
            await step_context.context.send_activity(MessageFactory.text(msg))
        except BackendError as e:
            await step_context.context.send_activity(
                MessageFactory.text(f"Não foi possível cadastrar: {e}")
            )
        except Exception as e:
            await step_context.context.send_activity(
                MessageFactory.text(f"Erro inesperado ao cadastrar: {e}")
            )

        return await step_context.end_dialog()
