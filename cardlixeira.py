import flet as ft

def create_trash_card(title, content, bgcolor=None, note_id=None, 
                     on_restore=None, on_delete_forever=None, 
                     on_drag_accept=None, page=None):
    """Cria um card de nota na lixeira"""
    
    # Função para criar o conteúdo do card
    def create_card_content():
        # Cria os botões de ação
        action_buttons = ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.RESTORE,
                    icon_color="#E2E2E3",
                    icon_size=20,
                    tooltip="Restaurar nota",
                    on_click=lambda e: on_restore(e, note_id, card) if on_restore else None,
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_FOREVER,
                    icon_color="#E2E2E3",
                    icon_size=20,
                    tooltip="Excluir permanentemente",
                    on_click=lambda e: on_delete_forever(e, note_id, card) if on_delete_forever else None,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            opacity=0,
            animate_opacity=300,
        )

        return ft.Container(
            content=ft.Column([
                # Título
                ft.Text(
                    title,
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color="#E2E2E3",
                    expand=True,
                ),
                # Conteúdo
                ft.Text(
                    content,
                    size=14,
                    color="#E2E2E3",
                    opacity=0.8,
                ),
                # Espaçador flexível
                ft.Container(expand=True),
                # Barra inferior com ícones de ação
                action_buttons,
            ], spacing=10),
            width=240,
            height=240,
            padding=15,
            border_radius=10,
            bgcolor=bgcolor if bgcolor else "#28292C",
            data={"id": note_id, "title": title},  # Armazena o ID e título da nota
        )

    # Cria o card principal
    card = create_card_content()

    def on_hover(e):
        is_hovering = e.data == "true"
        card.content.controls[-1].opacity = 1 if is_hovering else 0  # action_buttons
        page.update()

    card.on_hover = on_hover

    # Container invisível para mostrar durante o drag
    placeholder = ft.Container(
        width=240,
        height=260,
        opacity=0,
    )

    # Cria uma cópia do card para o feedback do drag, sem os botões de ação
    feedback_card = ft.Container(
        content=ft.Column([
            # Título
            ft.Text(
                title,
                size=16,
                weight=ft.FontWeight.W_500,
                color="#E2E2E3",
                expand=True,
            ),
            # Conteúdo
            ft.Text(
                content,
                size=14,
                color="#E2E2E3",
                opacity=0.8,
            ),
        ]),
        width=240,
        height=240,
        padding=15,
        border_radius=10,
        bgcolor=bgcolor if bgcolor else "#28292C",
        margin=ft.margin.only(bottom=20),
    )

    # Cria o DragTarget que vai envolver o card
    drag_target = ft.DragTarget(
        group="notes",
        content=card,
        on_accept=lambda e: on_drag_accept(e, card) if on_drag_accept else None,
    )

    # Retorna o Draggable com todas as propriedades necessárias
    return ft.Draggable(
        group="notes",
        content=drag_target,
        content_when_dragging=placeholder,
        content_feedback=feedback_card,
    ) 