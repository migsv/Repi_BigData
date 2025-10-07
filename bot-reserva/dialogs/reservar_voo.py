from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice

# O objetivo inicial é criar apenas uma seção de voos com 3 promoções fixas para demonstrar a gravação em DB.

class ReservarVooDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ReservarVooDialog, self).__init__("ReservarVooDialog")
        self.user_state = user_state

        # Prompts
        self.add_dialog(ChoicePrompt("promoPrompt"))
        self.add_dialog(TextPrompt("usuarioIdPrompt"))

        # Waterfall
        self.add_dialog(
            WaterfallDialog(
                "ReservarVooDialog",
                [
                    self.mostrar_promocoes_step,
                    self.pedir_usuario_step,
                    self.criar_reserva_step
                ]
            )
        )
        self.initial_dialog_id = "ReservarVooDialog"

        # 3 promoções fixas (DEMO) – ajuste se quiser
        self.promos = [
            {
                "label": "1) GOL - GRU → REC | 2025-12-15 09:30 | R$ 899,90",
                "companhiaAerea": "GOL",
                "origem": "GRU",
                "destino": "REC",
                "dataPartida": "2025-12-15T09:30:00",
                "preco": "899,90",
            },
            {
                "label": "2) AZUL - SDU → CNF | 2025-11-20 07:00 | R$ 499,00",
                "companhiaAerea": "AZUL",
                "origem": "SDU",
                "destino": "CNF",
                "dataPartida": "2025-11-20T07:00:00",
                "preco": "499,00",
            },
            {
                "label": "3) LATAM - GRU → POA | 2025-10-25 20:15 | R$ 399,90",
                "companhiaAerea": "LATAM",
                "origem": "GRU",
                "destino": "POA",
                "dataPartida": "2025-10-25T20:15:00",
                "preco": "399,90",
            },
        ]

    async def mostrar_promocoes_step(self, step_context: WaterfallStepContext):
        texto = "Promoções de Voo (escolha uma opção ou 'Voltar ao Menu'):\n\n"
        for p in self.promos:
            texto += f"- {p['label']}\n"
        return await step_context.prompt(
            "promoPrompt",
            PromptOptions(
                prompt=MessageFactory.text(texto),
                choices=[
                    Choice("Opção 1"),
                    Choice("Opção 2"),
                    Choice("Opção 3"),
                    Choice("Voltar ao Menu"),
                ],
                retry_prompt=MessageFactory.text("Escolha: Opção 1, Opção 2, Opção 3 ou Voltar ao Menu.")
            )
        )

    async def pedir_usuario_step(self, step_context: WaterfallStepContext):
        escolha = step_context.result.value

        if escolha == "Voltar ao Menu":
            await step_context.context.send_activity(
                MessageFactory.text("Voltando ao menu principal.")
            )
            return await step_context.end_dialog()

        # Mapear escolha -> índice
        idx = {"Opção 1": 0, "Opção 2": 1, "Opção 3": 2}.get(escolha)
        if idx is None:
            await step_context.context.send_activity(
                MessageFactory.text("Opção inválida.")
            )
            return await step_context.end_dialog()

        step_context.values["vooSelecionado"] = self.promos[idx]

        return await step_context.prompt(
            "usuarioIdPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Informe seu ID de usuário para confirmar a reserva (ex.: 1):"),
                retry_prompt=MessageFactory.text("ID inválido. Digite um número inteiro (ex.: 1).")
            )
        )

    async def criar_reserva_step(self, step_context: WaterfallStepContext):
        usuario_id_raw = str(step_context.result or "").strip()
        try:
            usuario_id = int(usuario_id_raw)
        except Exception:
            await step_context.context.send_activity(
                MessageFactory.text("ID inválido. Operação cancelada.")
            )
            return await step_context.end_dialog()

        voo = step_context.values.get("vooSelecionado", {})
        if not voo:
            await step_context.context.send_activity(
                MessageFactory.text("Não foi possível recuperar a opção selecionada.")
            )
            return await step_context.end_dialog()

        from services.backend import create_reserva_voo, BackendError
        try:
            reserva = await create_reserva_voo(
                usuario_id=usuario_id,
                origem=voo["origem"],
                destino=voo["destino"],
                data_partida=voo["dataPartida"],
                preco_str=voo["preco"],
                companhia_aerea=voo.get("companhiaAerea"),
                data_retorno=None,
                status="PENDENTE",
            )

            usuario_id_ret = reserva.get("usuarioId") or (reserva.get("usuario") or {}).get("id")
            msg = (
                "Reserva criada com sucesso!\n"
                f"ID: {reserva.get('id')}\n"
                f"Usuário: {usuario_id_ret}\n"
                f"Companhia: {reserva.get('companhiaAerea')}\n"
                f"Origem: {reserva.get('origem')}\n"
                f"Destino: {reserva.get('destino')}\n"
                f"Partida: {reserva.get('dataPartida')}\n"
                f"Preço: {reserva.get('preco')}\n"
                f"Status: {reserva.get('status')}"
            )
            await step_context.context.send_activity(MessageFactory.text(msg))
        except BackendError as e:
            await step_context.context.send_activity(
                MessageFactory.text(f"Não foi possível criar a reserva: {e}")
            )
        except Exception as e:
            await step_context.context.send_activity(
                MessageFactory.text(f"Erro inesperado ao criar a reserva: {e}")
            )

        return await step_context.end_dialog()
