import flet as ft
from models import TotalDiario, Corrida, session
from datetime import datetime

def main(page: ft.Page):
    page.title = "Organizador de Ganhos e Gastos"

    # Função para atualizar a interface ao fechar o DatePicker/TimePicker
    def on_picker_dismissed(e):
        page.update()

    # Função para exibir a data selecionada (Total Diário)
    def on_date_selected(e):
        if date_picker.value:
            selected_date.value = f"Data selecionada: {date_picker.value.strftime('%d-%m-%Y')}"
        else:
            selected_date.value = "Nenhuma data selecionada"
        page.update()

    # Funções para exibir os horários selecionados (Total Diário)
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

    # Função para salvar os dados no banco de dados (Total Diário)
    def salvar_geral(e):
        try:
            if not date_picker.value:
                txt_erro.content.value = "Erro: Por favor, selecione uma data antes de salvar."
                txt_erro.visible = True
                txt_acerto.visible = False
                page.update()
                return

            data = date_picker.value
            horario_saida = horario_saida_picker.value.strftime("%H:%M") if horario_saida_picker.value else "00:00"
            horario_chegada = horario_chegada_picker.value.strftime("%H:%M") if horario_chegada_picker.value else "00:00"
            km_total_dia = float(km_total_input.value.replace(',', '.') or 0)
            ganho_total_dia = float(ganho_total_input.value.replace(',', '.') or 0)
            gasto_total_abastecimento = float(gasto_total_abastecimento_input.value.replace(',', '.') or 0)
            gasto_total_alimentacao = float(gasto_total_alimentacao_input.value.replace(',', '.') or 0)
            qtde_corridas = int(qtde_corridas_input.value or 0)
            classificacao_dia = classificacao_dia_input.value

            novo_registro = TotalDiario(
                data=data,
                horario_saida=horario_saida,
                horario_chegada=horario_chegada,
                km_total_dia=km_total_dia,
                ganho_total_dia=ganho_total_dia,
                gasto_total_abastecimento=gasto_total_abastecimento,
                gasto_total_alimentacao=gasto_total_alimentacao,
                qtde_corridas=qtde_corridas,
                classificacao_dia=classificacao_dia
            )
            session.add(novo_registro)
            session.commit()

            txt_erro.visible = False
            txt_acerto.content.value = "Dados salvos com sucesso!"
            txt_acerto.visible = True
        except Exception as ex:
            txt_erro.content.value = f"Erro ao salvar: {ex}"
            txt_erro.visible = True
            txt_acerto.visible = False
        page.update()

    # Função para exibir a data selecionada para a corrida (Corridas Individuais)
    def on_date_selected_corrida(e):
        if date_picker_corrida.value:
            selected_date_corrida.value = f"Data da corrida: {date_picker_corrida.value.strftime('%d-%m-%Y')}"
        else:
            selected_date_corrida.value = "Nenhuma data selecionada"
        page.update()

    # Função para salvar a corrida (Corridas Individuais)
    def salvar_corrida(e):
        try:
            if not date_picker_corrida.value:
                txt_erro_corrida.content.value = "Erro: Por favor, selecione uma data antes de salvar."
                txt_erro_corrida.visible = True
                txt_acerto_corrida.visible = False
                page.update()
                return

            data = date_picker_corrida.value
            plataforma = plataforma_input.value
            tempo = float(tempo_input.value.replace(',', '.') or 0)
            valor = float(valor_input.value.replace(',', '.') or 0)
            km = float(km_input.value.replace(',', '.') or 0)
            local_saida = local_saida_input.value
            local_destino = local_destino_input.value

            nova_corrida = Corrida(
                data=data,
                plataforma=plataforma,
                tempo=tempo,
                valor=valor,
                km=km,
                local_saida=local_saida,
                local_destino=local_destino
            )
            session.add(nova_corrida)
            session.commit()

            txt_erro_corrida.visible = False
            txt_acerto_corrida.content.value = "Corrida salva com sucesso!"
            txt_acerto_corrida.visible = True
        except Exception as ex:
            txt_erro_corrida.content.value = f"Erro ao salvar: {ex}"
            txt_erro_corrida.visible = True
            txt_acerto_corrida.visible = False
        page.update()

    # Componentes da interface para Total Diário
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
    date_picker = ft.DatePicker(on_change=on_date_selected, on_dismiss=on_picker_dismissed)
    horario_saida_picker = ft.TimePicker(on_change=on_horario_saida_selected, on_dismiss=on_picker_dismissed)
    horario_chegada_picker = ft.TimePicker(on_change=on_horario_chegada_selected, on_dismiss=on_picker_dismissed)
    page.overlay.extend([date_picker, horario_saida_picker, horario_chegada_picker])

    date_button = ft.ElevatedButton("Escolher Data", on_click=lambda _: page.open(date_picker))
    horario_saida_button = ft.ElevatedButton("Selecionar Horário de Saída", on_click=lambda _: page.open(horario_saida_picker))
    horario_chegada_button = ft.ElevatedButton("Selecionar Horário de Chegada", on_click=lambda _: page.open(horario_chegada_picker))
    selected_date = ft.Text("Nenhuma data selecionada")
    horario_saida = ft.Text("Horário de saída não selecionado")
    horario_chegada = ft.Text("Horário de chegada não selecionado")
    km_total_input = ft.TextField(label="Km total do dia", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    ganho_total_input = ft.TextField(label="R$ Ganho total do dia", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    gasto_total_abastecimento_input = ft.TextField(label="R$ Abastecimento total do dia", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    gasto_total_alimentacao_input = ft.TextField(label="R$ Gasto total alimentação dia", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    qtde_corridas_input = ft.TextField(label="Quantidade de corridas", keyboard_type=ft.KeyboardType.NUMBER, width=200)
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
        value="Mediano"
    )
    save_button = ft.ElevatedButton("Salvar", on_click=salvar_geral)

    # Componentes da interface para Corridas Individuais
    txt_erro_corrida = ft.Container(
        content=ft.Text("Erro ao salvar a corrida"),
        visible=False,
        bgcolor=ft.Colors.RED_200,
        padding=10,
        width=300
    )
    txt_acerto_corrida = ft.Container(
        content=ft.Text("Corrida salva com sucesso"),
        visible=False,
        bgcolor=ft.Colors.GREEN_200,
        padding=10,
        width=300
    )
    date_picker_corrida = ft.DatePicker(on_change=on_date_selected_corrida, on_dismiss=on_picker_dismissed)
    page.overlay.append(date_picker_corrida)
    date_button_corrida = ft.ElevatedButton("Escolher Data da Corrida", on_click=lambda _: page.open(date_picker_corrida))
    selected_date_corrida = ft.Text("Nenhuma data selecionada")
    plataforma_input = ft.Dropdown(
        label="Plataforma",
        width=200,
        options=[
            ft.dropdown.Option("Uber"),
            ft.dropdown.Option("99pop"),
            ft.dropdown.Option("Indrive")
        ],
        value="Uber"
    )
    tempo_input = ft.TextField(label="Tempo da corrida (min)", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    valor_input = ft.TextField(label="Valor recebido (R$)", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    km_input = ft.TextField(label="KM rodados", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    local_saida_input = ft.TextField(label="Local de saída", width=200)
    local_destino_input = ft.TextField(label="Local de destino", width=200)
    save_button_corrida = ft.ElevatedButton("Salvar Corrida", on_click=salvar_corrida)

    # Layout das abas
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
                classificacao_dia_input,
                save_button
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )

    aba_corridas_individuais = ft.Tab(
        text="Corridas Individuais",
        content=ft.Column(
            controls=[
                txt_erro_corrida,
                txt_acerto_corrida,
                date_button_corrida,
                selected_date_corrida,
                plataforma_input,
                tempo_input,
                valor_input,
                km_input,
                local_saida_input,
                local_destino_input,
                save_button_corrida
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )

    # Adiciona as abas à interface
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[aba_total_diario, aba_corridas_individuais]
    )
    page.add(tabs)

# Executa o aplicativo
ft.app(target=main)