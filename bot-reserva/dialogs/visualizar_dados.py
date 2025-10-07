from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext

class VisualizarDadosDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(VisualizarDadosDialog, self).__init__("VisualizarDadosDialog")
        self.user_state = user_state

        self.add_dialog(TextPrompt("idPrompt"))
        self.add_dialog(
            WaterfallDialog(
                "VisualizarDadosDialog",
                [ self.pedir_id_step, self.mostrar_dados_step ]
            )
        )
        self.initial_dialog_id = "VisualizarDadosDialog"

    async def pedir_id_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "idPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Digite seu ID de usuário (ex.: 1):"),
                retry_prompt=MessageFactory.text("ID inválido. Digite um número inteiro (ex.: 1).")
            )
        )

    async def mostrar_dados_step(self, step_context: WaterfallStepContext):
        raw = str(step_context.result or "").strip()
        try:
            user_id = int(raw)
        except Exception:
            await step_context.context.send_activity(
                MessageFactory.text("ID inválido. Operação cancelada.")
            )
            return await step_context.end_dialog()

        from services.backend import get_user, get_reservas_voo_by_usuario, BackendError

        # Busca usuário
        try:
            user = await get_user(user_id)
        except BackendError as e:
            await step_context.context.send_activity(MessageFactory.text(str(e)))
            return await step_context.end_dialog()
        except Exception as e:
            await step_context.context.send_activity(MessageFactory.text(f"Erro ao buscar usuário: {e}"))
            return await step_context.end_dialog()

        # Busca reservas de voo do usuário
        try:
            reservas = await get_reservas_voo_by_usuario(user_id)
        except BackendError as e:
            await step_context.context.send_activity(MessageFactory.text(str(e)))
            reservas = []
        except Exception as e:
            await step_context.context.send_activity(MessageFactory.text(f"Erro ao listar reservas: {e}"))
            reservas = []

        # Monta resposta
        # depois de obter 'user'
        if not isinstance(user, dict) or not user.get("id"):
            # mostra bruto para debug se vier _raw
            raw = user.get("_raw") if isinstance(user, dict) else None
            msg = "Usuário não encontrado ou resposta inválida do servidor."
            if raw:
                msg += f"\n(raw: {raw[:300]})"
            await step_context.context.send_activity(MessageFactory.text(msg))
            return await step_context.end_dialog()

        msg_user = (
            "🧾 Seus dados\n"
            f"ID: {user.get('id')}\n"
            f"Nome: {user.get('nome') or user.get('name')}\n"
            f"Email: {user.get('email')}\n"
            f"Telefone: {user.get('telefone')}\n"
        )
        await step_context.context.send_activity(MessageFactory.text(msg_user))

        if not reservas:
            await step_context.context.send_activity(MessageFactory.text("Você não possui reservas de voo."))
            return await step_context.end_dialog()

        # lista as reservas (em blocos para não estourar o tamanho da mensagem)
        lines = []
        for r in reservas:
            usuario_ret = r.get("usuarioId") or (r.get("usuario") or {}).get("id")
            lines.append(
                "✈️ Reserva\n"
                f"ID: {r.get('id')}\n"
                f"Usuário: {usuario_ret}\n"
                f"Companhia: {r.get('companhiaAerea')}\n"
                f"Origem/Destino: {r.get('origem')} → {r.get('destino')}\n"
                f"Partida: {r.get('dataPartida')}\n"
                f"Retorno: {r.get('dataRetorno')}\n"
                f"Preço: {r.get('preco')}\n"
                f"Status: {r.get('status')}\n"
            )

        # envia em pedaços de até ~5 reservas por mensagem
        chunk, count = [], 0
        for item in lines:
            chunk.append(item)
            count += 1
            if count % 5 == 0:
                await step_context.context.send_activity(MessageFactory.text("\n".join(chunk)))
                chunk = []
        if chunk:
            await step_context.context.send_activity(MessageFactory.text("\n".join(chunk)))

        return await step_context.end_dialog()
