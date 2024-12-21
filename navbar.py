import flet as ft

def create_navbar(menu_button, exit_button):
    # Ícone do Keep
    keep_icon = ft.Image(
        src="https://www.gstatic.com/images/branding/product/1x/keep_2020q4_48dp.png",
        width=40,
        height=40,
        fit=ft.ImageFit.CONTAIN,
    )

    # Título
    title = ft.Text(
        "MrKeep",
        color="#E2E2E3",
        size=20,
        weight=ft.FontWeight.W_500
    )

    # Navbar
    return ft.Container(
        content=ft.Row(
            [
                # Grupo da esquerda
                ft.Row(
                    [menu_button, keep_icon, title],
                    spacing=10,
                ),
                # Grupo da direita
                exit_button,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(left=10, right=10),
        height=64,
        bgcolor="#202124",
        border=ft.border.only(bottom=ft.BorderSide(1, "#525355"))
    ) 