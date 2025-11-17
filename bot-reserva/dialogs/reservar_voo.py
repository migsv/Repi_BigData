from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice

from helpers.formatting import format_currency, format_datetime, format_status


class ReservarVooDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ReservarVooDialog, self).__init__("ReservarVooDialog")
        self.user_state = user_state

        self.add_dialog(ChoicePrompt("promoPrompt"))
        self.add_dialog(TextPrompt("usuarioCpfPrompt"))

        self.add_dialog(
            WaterfallDialog(
                "ReservarVooDialog",
                [
                    self.mostrar_promocoes_step,
                    self.pedir_usuario_step,
                    self.criar_reserva_step,
                ],
            )
        )
        self.initial_dialog_id = "ReservarVooDialog"

        self.promos = [
            {
                "companhiaAerea": "GranAir",
                "origem": "GRU",
                "destino": "LIS",
                "dataPartida": "2025-08-15T22:05:00",
                "preco": "3599.90",
                "descricao": "Inclui 1 bagagem despachada + acesso ao lounge GranClub.",
            },
            {
                "companhiaAerea": "Latam",
                "origem": "SDU",
                "destino": "BSB",
                "dataPartida": "2025-07-03T09:20:00",
                "preco": "799.00",
                "descricao": "Tarifa flexível + upgrade gratuito de assento.",
            },
            {
                "companhiaAerea": "Azul",
                "origem": "VCP",
                "destino": "MIA",
                "dataPartida": "2025-09-21T23:10:00",
                "preco": "4299.00",
                "descricao": "Voos diretos + 10% de cashback em pontos TudoAzul.",
            },
            {
                "companhiaAerea": "GOL",
                "origem": "GRU",
                "destino": "REC",
                "dataPartida": "2025-06-18T11:40:00",
                "preco": "999.90",
                "descricao": "Direto + franquia extra para equipamentos esportivos.",
            },
            {
                "companhiaAerea": "Tap",
                "origem": "GIG",
                "destino": "BCN",
                "dataPartida": "2025-10-02T18:55:00",
                "preco": "3890.00",
                "descricao": "Stopover gratuito em Lisboa e traslado incluído.",
            },
        ]

    async def mostrar_promocoes_step(self, step_context: WaterfallStepContext):
        linhas = ["🔥 Voos promocionais GranVoyage:", ""]
        for idx, promo in enumerate(self.promos, start=1):
            linhas.append(
                f"{idx}) {promo['companhiaAerea']} | {promo['origem']} → {promo['destino']} | "
                f"{format_datetime(promo['dataPartida'])} | {format_currency(promo['preco'])}"
            )
            linhas.append(f"   {promo['descricao']}")
        linhas.append("\nEscolha uma das opções para confirmar imediatamente.")
        texto = "\n".join(linhas)
        return await step_context.prompt(
            "promoPrompt",
            PromptOptions(
                prompt=MessageFactory.text(texto),
                choices=[
                    Choice("Opção 1"),
                    Choice("Opção 2"),
                    Choice("Opção 3"),
                    Choice("Opção 4"),
                    Choice("Opção 5"),
                    Choice("Voltar ao Menu"),
                ],
                retry_prompt=MessageFactory.text(
                    "Por favor, escolha entre Opção 1 a 5 ou Voltar ao Menu."
                ),
            ),
        )

    async def pedir_usuario_step(self, step_context: WaterfallStepContext):
        escolha = step_context.result.value

        if escolha == "Voltar ao Menu":
            await step_context.context.send_activity(
                MessageFactory.text("Voltando ao menu principal.")
            )
            return await step_context.end_dialog()

        idx = {
            "Opção 1": 0,
            "Opção 2": 1,
            "Opção 3": 2,
            "Opção 4": 3,
            "Opção 5": 4,
        }.get(escolha)
        if idx is None:
            await step_context.context.send_activity(
                MessageFactory.text("Opção inválida.")
            )
            return await step_context.end_dialog()

        step_context.values["vooSelecionado"] = self.promos[idx]

        return await step_context.prompt(
            "usuarioCpfPrompt",
            PromptOptions(
                prompt=MessageFactory.text(
                    "Informe o CPF do titular da reserva (somente números)."
                )
            )
        )

    async def criar_reserva_step(self, step_context: WaterfallStepContext):
        usuario_cpf = "".join(filter(str.isdigit, str(step_context.result or "")))
        if not usuario_cpf:
            await step_context.context.send_activity(
                MessageFactory.text("CPF inválido. Operação cancelada.")
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
                usuario_cpf=usuario_cpf,
                origem=voo["origem"],
                destino=voo["destino"],
                data_partida=voo["dataPartida"],
                preco_str=voo["preco"],
                companhia_aerea=voo.get("companhiaAerea"),
                data_retorno=None,
                status="CONFIRMADA",
            )

            usuario_id_ret = reserva.get("usuarioId") or (reserva.get("usuario") or {}).get("id")
            msg = (
                "✈️ Reserva confirmada!\n"
                f"Código: {reserva.get('id')}\n"
                f"Cliente: {usuario_id_ret or 'novo cadastro'}\n"
                f"Voo: {reserva.get('origem')} → {reserva.get('destino')} ({reserva.get('companhiaAerea')})\n"
                f"Partida: {format_datetime(reserva.get('dataPartida'))}\n"
                f"Tarifa: {format_currency(reserva.get('preco'))}\n"
                f"Status: {format_status(reserva.get('status'))}"
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
