import flet as ft

def create_notes_section(title, is_pinned=False):
    """Cria uma seção de notas (pinned ou normal)"""
    return ft.Column(
        controls=[
            ft.Container(
                content=ft.Text(
                    title,
                    size=12,
                    weight=ft.FontWeight.W_500,
                    color="#E2E2E3",
                ),
                padding=ft.padding.only(left=30, bottom=10, top=20),
            ),
            ft.Container(
                content=ft.GridView(
                    runs_count=0,
                    max_extent=250,
                    spacing=10,
                    run_spacing=10,
                    padding=30,
                    controls=[],  # Lista vazia de notas
                ),
            ),
        ],
        visible=True,
    ) 