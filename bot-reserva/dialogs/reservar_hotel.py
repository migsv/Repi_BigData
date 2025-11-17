from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice

from helpers.formatting import format_currency, format_date, format_status


class ReservarHotelDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ReservarHotelDialog, self).__init__("ReservarHotelDialog")
        self.user_state = user_state
        self.add_dialog(ChoicePrompt("promoPrompt"))
        self.add_dialog(TextPrompt("cpfPrompt"))
        self.add_dialog(
            WaterfallDialog(
                "ReservarHotelDialog",
                [
                    self.mostrar_promocoes_step,
                    self.pedir_cpf_step,
                    self.process_reserva_step,
                ],
            )
        )
        self.initial_dialog_id = "ReservarHotelDialog"

        self.promos = [
            {
                "nomeHotel": "Gran Resort Lisboa",
                "localizacao": "Lisboa",
                "dataCheckIn": "2025-08-02",
                "dataCheckOut": "2025-08-09",
                "precoTotal": "5290.00",
                "descricao": "7 noites com café da manhã + traslado aeroporto/hotel.",
            },
            {
                "nomeHotel": "Solar do Vale Boutique",
                "localizacao": "Gramado",
                "dataCheckIn": "2025-07-12",
                "dataCheckOut": "2025-07-16",
                "precoTotal": "1890.00",
                "descricao": "Festival de inverno + fondue incluso.",
            },
            {
                "nomeHotel": "Costa Caribe All Inclusive",
                "localizacao": "Cancún",
                "dataCheckIn": "2025-09-01",
                "dataCheckOut": "2025-09-06",
                "precoTotal": "6120.00",
                "descricao": "All inclusive premium + crédito em spa.",
            },
            {
                "nomeHotel": "Urban Sky São Paulo",
                "localizacao": "São Paulo",
                "dataCheckIn": "2025-06-20",
                "dataCheckOut": "2025-06-23",
                "precoTotal": "960.00",
                "descricao": "Fim de semana gastronômico + late checkout.",
            },
            {
                "nomeHotel": "Blue Lagoon Retreat",
                "localizacao": "Maldivas",
                "dataCheckIn": "2025-11-05",
                "dataCheckOut": "2025-11-10",
                "precoTotal": "11250.00",
                "descricao": "Bangâlo sobre a água + jantar privativo incluso.",
            },
        ]

    async def mostrar_promocoes_step(self, step_context: WaterfallStepContext):
        linhas = ["🏨 Seleção de hotéis em promoção:", ""]
        for idx, hotel in enumerate(self.promos, start=1):
            linhas.append(
                f"{idx}) {hotel['nomeHotel']} - {hotel['localizacao']} | "
                f"{format_date(hotel['dataCheckIn'])} → {format_date(hotel['dataCheckOut'])} | "
                f"{format_currency(hotel['precoTotal'])}"
            )
            linhas.append(f"   {hotel['descricao']}")
        linhas.append("\nEscolha uma opção para confirmar imediatamente.")
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
                    "Informe uma das opções 1 a 5 ou Voltar ao Menu."
                ),
            ),
        )

    async def pedir_cpf_step(self, step_context: WaterfallStepContext):
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
            await step_context.context.send_activity(MessageFactory.text("Opção inválida."))
            return await step_context.end_dialog()

        step_context.values["hotelSelecionado"] = self.promos[idx]
        return await step_context.prompt(
            "cpfPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Informe o CPF do titular (somente números):"),
                retry_prompt=MessageFactory.text("CPF inválido. Digite apenas números."),
            ),
        )

    async def process_reserva_step(self, step_context: WaterfallStepContext):
        cpf = "".join(filter(str.isdigit, str(step_context.result or "")))
        if not cpf:
            await step_context.context.send_activity(
                MessageFactory.text("CPF inválido. Operação cancelada.")
            )
            return await step_context.end_dialog()

        hotel = step_context.values.get("hotelSelecionado", {})
        if not hotel:
            await step_context.context.send_activity(
                MessageFactory.text("Não foi possível recuperar a opção selecionada.")
            )
            return await step_context.end_dialog()

        from services.backend import create_reserva_hotel, BackendError

        try:
            reserva = await create_reserva_hotel(
                usuario_cpf=cpf,
                nome_hotel=hotel["nomeHotel"],
                localizacao=hotel["localizacao"],
                data_checkin=hotel["dataCheckIn"],
                data_checkout=hotel["dataCheckOut"],
                preco_total=hotel["precoTotal"],
                status="CONFIRMADA",
            )
            msg = (
                "🏨 Reserva confirmada!\n"
                f"Código: {reserva.get('id')}\n"
                f"Hotel: {reserva.get('nomeHotel')} ({reserva.get('localizacao')})\n"
                f"Período: {format_date(reserva.get('dataCheckIn'))} → {format_date(reserva.get('dataCheckOut'))}\n"
                f"Total: {format_currency(reserva.get('precoTotal'))}\n"
                f"Status: {format_status(reserva.get('status'))}"
            )
            await step_context.context.send_activity(MessageFactory.text(msg))
        except BackendError as e:
            await step_context.context.send_activity(
                MessageFactory.text(f"Não foi possível criar a reserva: {e}")
            )
        except Exception as e:
            await step_context.context.send_activity(
                MessageFactory.text(f"Erro inesperado ao criar reserva: {e}")
            )

        return await step_context.end_dialog()
