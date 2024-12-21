import flet as ft

# Lista de cores para as notas
note_colors = [
    "#28292C",  # Cinza padrão
    "#1E6F50",  # Verde
    "#614A19",  # Marrom
    "#4B443A",  # Bege escuro
    "#662E1E",  # Vermelho escuro
    "#3C3F43",  # Cinza escuro
    "#1A237E",  # Azul escuro
    "#4A148C",  # Roxo escuro
]

def create_note_input(
    input_expanded,
    note_color,
    is_pinned,
    note_title,
    note_content,
    toggle_input,
    toggle_pin,
    change_color,
    update_title,
    update_content,
    add_note,
    close_note
):
    def create_collapsed_input():
        return ft.Container(
            content=ft.TextField(
                border_color="transparent",
                bgcolor="#28292C",
                text_size=16,
                color="#E2E2E3",
                cursor_color="#E2E2E3",
                hint_text="Criar uma nota...",
                hint_style=ft.TextStyle(
                    color="#E2E2E3",
                    size=16,
                ),
                width=600,
                height=50,
                border_radius=10,
                on_focus=toggle_input,
            ),
            alignment=ft.alignment.center,
        )

    def create_expanded_input():
        # Container do input expandido
        input_container = ft.Container(
            content=ft.Column([
                # Barra superior com título e ícone de fixar
                ft.Row([
                    ft.TextField(
                        value=note_title,  # Usa o valor atual do título
                        border_color="transparent",
                        bgcolor="transparent",
                        text_size=16,
                        color="#E2E2E3",
                        cursor_color="#E2E2E3",
                        hint_text="Título",
                        hint_style=ft.TextStyle(
                            color="#E2E2E3",
                            size=16,
                        ),
                        width=540,
                        height=40,
                        on_change=update_title,  # Atualiza o estado do título
                    ),
                    ft.IconButton(
                        icon=ft.Icons.PUSH_PIN if is_pinned else ft.Icons.PUSH_PIN_OUTLINED,
                        icon_color="#E2E2E3",
                        icon_size=20,
                        on_click=toggle_pin,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                # Área de conteúdo
                ft.TextField(
                    value=note_content,  # Usa o valor atual do conteúdo
                    border_color="transparent",
                    bgcolor="transparent",
                    text_size=14,
                    color="#E2E2E3",
                    cursor_color="#E2E2E3",
                    hint_text="Criar uma nota...",
                    hint_style=ft.TextStyle(
                        color="#E2E2E3",
                        size=14,
                    ),
                    width=600,
                    height=120,
                    multiline=True,
                    on_change=update_content,  # Atualiza o estado do conteúdo
                ),

                # Barra inferior com ícones
                ft.Row([
                    ft.PopupMenuButton(
                        icon=ft.Icons.PALETTE_OUTLINED,
                        icon_color="#E2E2E3",
                        icon_size=20,
                        items=[
                            ft.PopupMenuItem(
                                content=ft.Row([
                                    ft.Container(
                                        bgcolor=color,
                                        width=24,
                                        height=24,
                                        border_radius=50,
                                    ),
                                    ft.Text(name, color="#E2E2E3", size=14),
                                ], spacing=10),
                                on_click=lambda e, c=color: change_color(e, c)
                            ) for color, name in zip(note_colors, [
                                "Cinza padrão", "Verde", "Marrom", "Bege escuro",
                                "Vermelho escuro", "Cinza escuro", "Azul escuro", "Roxo escuro"
                            ])
                        ],
                    ),
                    ft.Row([
                        ft.ElevatedButton(
                            "Criar",
                            icon=ft.Icons.ADD,
                            on_click=add_note,
                            style=ft.ButtonStyle(
                                color="#E2E2E3",
                                bgcolor="#1E6F50"  # Cor verde para destacar ação principal
                            ),
                        ),
                        ft.TextButton(
                            text="Fechar",
                            style=ft.ButtonStyle(
                                color="#E2E2E3",
                            ),
                            on_click=close_note,
                        ),
                    ], spacing=10),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ]),
            bgcolor=note_color,  # Usa a cor atual da nota
            padding=10,
            border_radius=10,
            width=600,
        )

        return ft.Container(
            content=input_container,
            alignment=ft.alignment.center,
        )

    return ft.Container(
        content=create_expanded_input() if input_expanded else create_collapsed_input(),
    ) 