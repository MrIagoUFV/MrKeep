import flet as ft

def create_empty_state():
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

def create_view_lixeira():
    return ft.Container(
        content=ft.Column(
            [
                # Container com scroll para as notas excluídas ou empty state
                ft.Container(
                    content=create_empty_state(),
                    expand=True,
                ),
            ],
            spacing=0,
        ),
        expand=True,
    ) 