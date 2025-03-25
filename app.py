import flet as ft
from sqlalchemy import create_engine
from models import dados, session

def main(page: ft.Page):
    page.title = 'Organizador de ganhos e gastos'

    def on_date_picker_dismissed(e):
        page.update()

    def on_date_selected(e):
        if date_picker.value:
            selected_date.value = f"Data selecionada: {date_picker.value.strftime('%Y-%m-%d')}"
        else:
            selected_date.value = "Nenhuma data selecionada"
        page.update()

    def salvar_geral(e):
        try:
            data = date_picker.value.strftime("%Y-%m-%d") if date_picker.value else "N/A"
            km_total_dia = float(km_total_input.value or 0)
            ganho_total_dia = float(ganho_total_input.value or 0)
            gasto_total_dia = float(gasto_total_input.value or 0)

            novo_dado = dados(
                data=data,
                km_total_dia=km_total_dia,
                ganho_total_dia=ganho_total_dia,
                gasto_total_dia=gasto_total_dia
            )

            session.add(novo_dado)
            session.commit()

            print(f"Salvando: Data={data}, KM={km_total_dia}, Ganho={ganho_total_dia}, Gasto={gasto_total_dia}")

            txt_erro.visible = False
            txt_acerto.visible = True
        except Exception as ex:
            txt_erro.visible = True
            txt_acerto.visible = False
            print(f"Erro ao cadastrar: {ex}")
        page.update()

    txt_erro = ft.Text("Erro ao salvar os dados", visible=False, bgcolor=ft.Colors.RED)
    txt_acerto = ft.Text("Dados salvos com sucesso", visible=False, bgcolor=ft.Colors.GREEN)

    date_picker = ft.DatePicker(
        on_change=on_date_selected,
        on_dismiss=on_date_picker_dismissed
    )
    page.overlay.append(date_picker)

    date_button = ft.ElevatedButton(
        "Escolher Data",
        on_click=lambda _: page.open(date_picker)
    )

    selected_date = ft.Text("Nenhuma data selecionada")
    km_total_input = ft.TextField(label="Km total do dia", keyboard_type=ft.KeyboardType.NUMBER)
    ganho_total_input = ft.TextField(label="Ganho total do dia", keyboard_type=ft.KeyboardType.NUMBER)
    gasto_total_input = ft.TextField(label="Gasto total do dia", keyboard_type=ft.KeyboardType.NUMBER)
    save_button = ft.ElevatedButton("Salvar", on_click=salvar_geral)

    page.add(
        ft.Column([
            txt_erro,
            txt_acerto,
            date_button,
            selected_date,
            km_total_input,
            ganho_total_input,
            gasto_total_input,
            save_button
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
    )

ft.app(target=main)