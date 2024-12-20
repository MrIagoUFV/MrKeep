import flet as ft

def main(page: ft.Page):
    # Configurações da página
    page.title = "MrKeep"
    page.window.maximized = True
    page.window.title_bar_hidden = True
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#202124"
    page.padding = 0

    # Estado do menu
    menu_expanded = False

    def toggle_menu(e):
        nonlocal menu_expanded
        menu_expanded = not menu_expanded
        menu_button.icon = ft.Icons.CLOSE if menu_expanded else ft.Icons.MENU
        
        # Atualiza a largura do menu lateral e visibilidade dos textos
        side_menu.width = 280 if menu_expanded else 72
        for item in side_menu.content.controls:  # Agora itera sobre todos os itens
            item.content.controls[1].opacity = 1 if menu_expanded else 0
        
        side_menu.update()
        page.update()

    def exit_app(e):
        page.window.close()

    def handle_menu_hover(e):
        nonlocal menu_expanded
        # Abre o menu quando o mouse entra
        if e.data == "true":
            menu_expanded = True
        # Fecha o menu quando o mouse sai
        else:
            menu_expanded = False
            
        menu_button.icon = ft.Icons.CLOSE if menu_expanded else ft.Icons.MENU
        side_menu.width = 280 if menu_expanded else 72
        
        # Atualiza a visibilidade dos textos
        for item in side_menu.content.controls:
            item.content.controls[1].opacity = 1 if menu_expanded else 0
        
        side_menu.update()
        page.update()

    # Ícone do menu hamburguer
    menu_button = ft.IconButton(
        icon=ft.Icons.MENU,
        icon_color="#E2E2E3",
        on_click=toggle_menu,
        icon_size=24,
    )

    # Ícone de sair
    exit_button = ft.IconButton(
        icon=ft.Icons.EXIT_TO_APP,
        icon_color="#E2E2E3",
        on_click=exit_app,
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

    # Menu Items
    def create_menu_item(icon, text, selected=False):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        name=icon,
                        size=24,
                        color="#E2E2E3",
                    ),
                    ft.Text(
                        text,
                        color="#E2E2E3",
                        size=16,
                        opacity=1 if menu_expanded else 0,
                        animate_opacity=300,
                    )
                ],
                spacing=16,
            ),
            bgcolor="#41331C" if selected else None,
            padding=ft.padding.all(16),
            border_radius=ft.border_radius.all(24),
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
        )

    # Menu Lateral atualizado
    side_menu = ft.Container(
        width=72 if not menu_expanded else 280,
        bgcolor="#202124",
        border=ft.border.only(right=ft.BorderSide(1, "#525355")),
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
        padding=ft.padding.only(top=8, left=8, right=8),
        content=ft.Column(
            [
                create_menu_item(ft.Icons.LIGHTBULB_OUTLINE, "Notas", selected=True),
                create_menu_item(ft.Icons.ARCHIVE_OUTLINED, "Arquivo"),
                create_menu_item(ft.Icons.DELETE_OUTLINE, "Lixeira"),
            ],
            spacing=4,
        ),
        on_hover=handle_menu_hover,
    )

    # Container principal que vai conter a navbar e o menu lateral
    main_container = ft.Container(
        content=ft.Column(
            [
                navbar,
                ft.Row(
                    [
                        side_menu,
                        ft.Container(expand=True),  # Área do conteúdo principal
                    ],
                    expand=True,  # Faz a Row ocupar todo espaço vertical restante
                    spacing=0,
                ),
            ],
            spacing=0,
            expand=True,
        ),
        expand=True,
    )

    # Adiciona o container principal à página (ao invés de apenas a navbar)
    page.add(main_container)
    
    # Atualiza a página com as configurações
    page.update()

# Inicia a aplicação
ft.app(main) 