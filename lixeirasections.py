import flet as ft

def create_trash_section():
    """Cria uma seção de notas na lixeira"""
    return ft.Container(
        content=ft.GridView(
            runs_count=0,
            max_extent=250,
            spacing=10,
            run_spacing=10,
            padding=30,
            controls=[],  # Lista vazia de notas
        ),
        expand=True,
    ) 