import flet as ft
from arquivosections import create_archive_section

def create_empty_state():
    """Cria o estado vazio da visualização de arquivos"""
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(
                    name=ft.Icons.ARCHIVE_OUTLINED,
                    size=120,
                    color="#37383A",
                ),
                ft.Text(
                    "Suas notas arquivadas aparecem aqui",
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

def create_view_arquivo(archive_section=None):
    """Cria a visualização de arquivos"""
    # Se não foi fornecida uma seção de arquivos, cria uma nova
    if archive_section is None:
        archive_section = create_archive_section()

    # Container da área central atualizado com a grade de notas arquivadas
    return ft.Container(
        content=ft.Column(
            [
                # Container com scroll para as notas ou empty state
                ft.Container(
                    content=create_empty_state() if len(archive_section.content.controls) == 0
                    else archive_section,
                    expand=True,
                ),
            ],
            spacing=0,
        ),
        expand=True,
    ) 