import flet as ft
from models import TotalDiario, session
from datetime import datetime

def main(page: ft.Page):
    page.title = "Organizador de Ganhos e Gastos"

    # Função para atualizar a interface ao fechar o DatePicker/TimePicker
    def on_picker_dismissed(e):
        page.update()

    # Função para exibir a data selecionada
    def on_date_selected(e):
        if date_picker.value:
            selected_date.value = f"Data selecionada: {date_picker.value.strftime('%d-%m-%Y')}"
        else:
            selected_date.value = "Nenhuma data selecionada"
        page.update()

    # Funções para exibir os horários selecionados
    def on_horario_saida_selected(e):
        if horario_saida_picker.value:
            horario_saida.value = f"Horário de saída selecionado: {horario_saida_picker.value.strftime('%H:%M')}"
        else:
            horario_saida.value = "Horário de saída não selecionado"
        page.update()

    def on_horario_chegada_selected(e):
        if horario_chegada_picker.value:
            horario_chegada.value = f"Horário de chegada selecionado: {horario_chegada_picker.value.strftime('%H:%M')}"
        else:
            horario_chegada.value = "Horário de chegada não selecionado"
        page.update()

    # Função para salvar os dados no banco de dados
    def salvar_geral(e):
        try:
            # Verifica se a data foi selecionada
            if not date_picker.value:
                txt_erro.content.value = "Erro: Por favor, selecione uma data antes de salvar."
                txt_erro.visible = True
                txt_acerto.visible = False
                page.update()
                return

            # Coleta os dados da interface
            data = date_picker.value  # Mantém como datetime.date
            horario_saida = horario_saida_picker.value.strftime("%H:%M") if horario_saida_picker.value else "00:00"
            horario_chegada = horario_chegada_picker.value.strftime("%H:%M") if horario_chegada_picker.value else "00:00"
            km_total_dia = float(km_total_input.value.replace(',', '.') or 0)
            ganho_total_dia = float(ganho_total_input.value.replace(',', '.') or 0)
            gasto_total_abastecimento = float(gasto_total_abastecimento_input.value.replace(',', '.') or 0)
            gasto_total_alimentacao = float(gasto_total_alimentacao_input.value.replace(',', '.') or 0)
            qtde_corridas = int(qtde_corridas_input.value or 0)
            classificacao_dia = classificacao_dia_input.value  # Obtém a classificação selecionada

            # Cria uma nova instância de TotalDiario
            novo_registro = TotalDiario(
                data=data,
                horario_saida=horario_saida,
                horario_chegada=horario_chegada,
                km_total_dia=km_total_dia,
                ganho_total_dia=ganho_total_dia,
                gasto_total_abastecimento=gasto_total_abastecimento,
                gasto_total_alimentacao=gasto_total_alimentacao,
                qtde_corridas=qtde_corridas,
                classificacao_dia=classificacao_dia  # Adiciona a classificação
            )

            # Salva no banco de dados
            session.add(novo_registro)
            session.commit()

            # Mensagem de sucesso
            txt_erro.visible = False
            txt_acerto.content.value = "Dados salvos com sucesso!"
            txt_acerto.visible = True
            print(f"Salvou: Data={data.strftime('%d-%m-%Y')}, Saída={horario_saida}, Chegada={horario_chegada}, KM={km_total_dia}, Ganho={ganho_total_dia}, Gasto Abastecimento={gasto_total_abastecimento}, Gasto Alimentação={gasto_total_alimentacao}, Corridas={qtde_corridas}, Classificação={classificacao_dia}")

        except Exception as ex:
            # Mensagem de erro
            txt_erro.content.value = f"Erro ao salvar: {ex}"
            txt_erro.visible = True
            txt_acerto.visible = False
            print(f"Erro: {ex}")
        page.update()

    # Elementos da interface
    txt_erro = ft.Container(
        content=ft.Text("Erro ao salvar os dados"),
        visible=False,
        bgcolor=ft.Colors.RED_200,
        padding=10,
        width=300
    )
    txt_acerto = ft.Container(
        content=ft.Text("Dados salvos com sucesso"),
        visible=False,
        bgcolor=ft.Colors.GREEN_200,
        padding=10,
        width=300
    )

    # Configuração do DatePicker
    date_picker = ft.DatePicker(
        on_change=on_date_selected,
        on_dismiss=on_picker_dismissed
    )

    # Configuração dos TimePickers
    horario_saida_picker = ft.TimePicker(
        on_change=on_horario_saida_selected,
        on_dismiss=on_picker_dismissed
    )
    horario_chegada_picker = ft.TimePicker(
        on_change=on_horario_chegada_selected,
        on_dismiss=on_picker_dismissed
    )

    page.overlay.extend([date_picker, horario_saida_picker, horario_chegada_picker])

    date_button = ft.ElevatedButton(
        "Escolher Data",
        on_click=lambda _: page.open(date_picker)
    )
    horario_saida_button = ft.ElevatedButton(
        "Selecionar Horário de Saída",
        on_click=lambda _: page.open(horario_saida_picker)
    )
    horario_chegada_button = ft.ElevatedButton(
        "Selecionar Horário de Chegada",
        on_click=lambda _: page.open(horario_chegada_picker)
    )

    # Configuração do Dropdown para classificar o dia
    classificacao_dia_input = ft.Dropdown(
        label="Classificação do dia",
        width=200,
        options=[
            ft.dropdown.Option("Péssimo"),
            ft.dropdown.Option("Ruim"),
            ft.dropdown.Option("Mediano"),
            ft.dropdown.Option("Bom"),
            ft.dropdown.Option("Ótimo")
        ],
        value="Mediano"  # Valor padrão
    )

    selected_date = ft.Text("Nenhuma data selecionada")
    horario_saida = ft.Text("Horário de saída não selecionado")
    horario_chegada = ft.Text("Horário de chegada não selecionado")
    km_total_input = ft.TextField(label="Km total do dia", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    ganho_total_input = ft.TextField(label="R$ Ganho total do dia", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    gasto_total_abastecimento_input = ft.TextField(label="R$ Abastecimento total do dia", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    gasto_total_alimentacao_input = ft.TextField(label="R$ Gasto total alimentação dia", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    qtde_corridas_input = ft.TextField(label="Quantidade de corridas", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    save_button = ft.ElevatedButton("Salvar", on_click=salvar_geral)

    # Layout da aba "Total Diário"
    aba_total_diario = ft.Tab(
        text="Total Diário",
        content=ft.Column(
            controls=[
                txt_erro,
                txt_acerto,
                date_button,
                selected_date,
                horario_saida_button,
                horario_saida,
                horario_chegada_button,
                horario_chegada,
                km_total_input,
                ganho_total_input,
                gasto_total_abastecimento_input,
                gasto_total_alimentacao_input,
                qtde_corridas_input,
                classificacao_dia_input,  # Adiciona o Dropdown no final
                save_button
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )

    # Aba "Corridas Individuais" (placeholder)
    aba_corridas_individuais = ft.Tab(
        text="Corridas Individuais",
        content=ft.Text("Em desenvolvimento...")
    )

    # Componente de abas
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[aba_total_diario, aba_corridas_individuais]
    )

    # Adiciona as abas à página
    page.add(tabs)

# Executa o aplicativo
ft.app(target=main)