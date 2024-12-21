import flet as ft

def get_page_info(page_name):
    pages = {
        "notas": {
            "icon": "https://www.gstatic.com/images/branding/product/1x/keep_2020q4_48dp.png",
            "title": "MrKeep"
        },
        "arquivo": {
            "icon": ft.icons.ARCHIVE_OUTLINED,
            "title": "Arquivo"
        },
        "lixeira": {
            "icon": ft.icons.DELETE_OUTLINE,
            "title": "Lixeira"
        }
    }
    return pages.get(page_name, pages["notas"])

def create_navbar(menu_button, exit_button, current_page="notas"):
    page_info = get_page_info(current_page)
    
    # Ícone da página
    page_icon = (
        ft.Image(
            src=page_info["icon"],
            width=40,
            height=40,
            fit=ft.ImageFit.CONTAIN,
        ) if current_page == "notas" else
        ft.Icon(
            name=page_info["icon"],
            size=40,
            color="#E2E2E3",
        )
    )

    # Título
    title = ft.Text(
        page_info["title"],
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
                    [menu_button, page_icon, title],
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