import flet as ft
from lixeirasections import create_trash_section

def create_empty_state():
    """Cria o estado vazio da visualização de lixeira"""
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(
                    name=ft.Icons.DELETE_OUTLINE,
                    size=120,
                    color="#37383A",
                ),
                ft.Text(
                    "Não há notas na lixeira",
                    size=16,
                    color="#9AA0A6",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        expand=True,
        alignment=ft.alignment.center,
    )

def create_view_lixeira(trash_section=None):
    """Cria a visualização de lixeira"""
    # Se não foi fornecida uma seção de lixeira, cria uma nova
    if trash_section is None:
        trash_section = create_trash_section()

    # Container da área central atualizado com a grade de notas da lixeira
    return ft.Container(
        content=ft.Column(
            [
                # Container com scroll para as notas ou empty state
                ft.Container(
                    content=create_empty_state() if len(trash_section.content.controls) == 0
                    else trash_section,
                    expand=True,
                ),
            ],
            spacing=0,
        ),
        expand=True,
    ) 