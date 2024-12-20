import flet as ft

def main(page: ft.Page):
    # Configurações da página
    page.title = "MrKeep"
    page.window_maximized = True
    page.window_title_bar_hidden = True
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#202124"
    page.padding = 0

    # Estado do menu
    menu_expanded = False

    def toggle_menu(e):
        nonlocal menu_expanded
        menu_expanded = not menu_expanded
        menu_button.icon = ft.icons.CLOSE if menu_expanded else ft.icons.MENU
        page.update()

    # Ícone do menu hamburguer
    menu_button = ft.IconButton(
        icon=ft.icons.MENU,
        icon_color="#E2E2E3",
        on_click=toggle_menu,
        icon_size=24,
    )

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
    navbar = ft.Container(
        content=ft.Row(
            [
                menu_button,
                keep_icon,
                title,
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.only(left=10, right=10),
        height=64,
        bgcolor="#202124",
        border=ft.border.only(bottom=ft.BorderSide(1, "#525355"))
    )

    # Adiciona a navbar à página
    page.add(navbar)
    
    # Atualiza a página com as configurações
    page.update()

# Inicia a aplicação
ft.app(main) 