import flet as ft
from models import TotalDiario, session
from datetime import datetime

def main(page: ft.Page):
    page.title = "Organizador de Ganhos e Gastos"

    # Função para atualizar a interface ao fechar o DatePicker
    def on_date_picker_dismissed(e):
        page.update()

    # Função para exibir a data selecionada
    def on_date_selected(e):
        if date_picker.value:
            selected_date.value = f"Data selecionada: {date_picker.value.strftime('%d-%m-%Y')}"
        else:
            selected_date.value = "Nenhuma data selecionada"
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
            km_total_dia = float(km_total_input.value or 0)
            ganho_total_dia = float(ganho_total_input.value or 0)
            gasto_total_dia = float(gasto_total_input.value or 0)

            # Cria uma nova instância de TotalDiario
            novo_registro = TotalDiario(
                data=data,
                km_total_dia=km_total_dia,
                ganho_total_dia=ganho_total_dia,
                gasto_total_dia=gasto_total_dia
            )

            # Salva no banco de dados
            session.add(novo_registro)
            session.commit()

            # Mensagem de sucesso
            txt_erro.visible = False
            txt_acerto.content.value = "Dados salvos com sucesso!"
            txt_acerto.visible = True
            print(f"Salvou: Data={data.strftime('%d-%m-%Y')}, KM={km_total_dia}, Ganho={ganho_total_dia}, Gasto={gasto_total_dia}")

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
        on_change=on_date_selected,  # Atualiza a interface quando uma data é selecionada
        on_dismiss=on_date_picker_dismissed  # Atualiza ao fechar o DatePicker
    )

    page.overlay.append(date_picker)  # Adiciona o DatePicker à página

    date_button = ft.ElevatedButton(
        "Escolher Data",
        on_click=lambda _: page.open(date_picker)  # Abre o DatePicker corretamente
    )

    selected_date = ft.Text("Nenhuma data selecionada")
    km_total_input = ft.TextField(label="Km total do dia", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    ganho_total_input = ft.TextField(label="Ganho total do dia", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    gasto_total_input = ft.TextField(label="Gasto total do dia", keyboard_type=ft.KeyboardType.NUMBER, width=200)
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
                km_total_input,
                ganho_total_input,
                gasto_total_input,
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