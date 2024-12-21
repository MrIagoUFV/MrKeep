import flet as ft
from addnota import note_colors

def create_archive_card(title, content, bgcolor=None, note_id=None, 
                       on_color_change=None, on_restore=None, on_delete=None, 
                       on_drag_accept=None, page=None):
    """Cria um card de nota arquivada"""
    
    # Função para criar o conteúdo do card
    def create_card_content():
        # Cria os botões de ação
        action_buttons = ft.Row(
            [
                ft.PopupMenuButton(
                    icon=ft.Icons.PALETTE_OUTLINED,
                    icon_color="#E2E2E3",
                    icon_size=20,
                    tooltip="Mudar cor de fundo",
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
                            on_click=lambda e, c=color: on_color_change(e, note_id, card, c) if on_color_change else None
                        ) for color, name in zip(note_colors, [
                            "Cinza padrão", "Verde", "Marrom", "Bege escuro",
                            "Vermelho escuro", "Cinza escuro", "Azul escuro", "Roxo escuro"
                        ])
                    ],
                ),
                ft.IconButton(
                    icon=ft.Icons.VISIBILITY_OUTLINED,
                    icon_color="#E2E2E3",
                    icon_size=20,
                    tooltip="Visualizar nota",
                ),
                ft.IconButton(
                    icon=ft.Icons.EDIT_OUTLINED,
                    icon_color="#E2E2E3",
                    icon_size=20,
                    tooltip="Editar nota",
                ),
                ft.IconButton(
                    icon=ft.Icons.RESTORE,
                    icon_color="#E2E2E3",
                    icon_size=20,
                    tooltip="Restaurar nota",
                    on_click=lambda e: on_restore(e, note_id, card) if on_restore else None,
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color="#E2E2E3",
                    icon_size=20,
                    tooltip="Excluir nota",
                    on_click=lambda e: on_delete(e, note_id, card) if on_delete else None,
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
                    max_lines=4,  # Limita a 4 linhas
                    overflow=ft.TextOverflow.ELLIPSIS,  # Adiciona ... no final
                    text_align=ft.TextAlign.LEFT,  # Mantém alinhamento à esquerda
                    expand=False,  # Importante para não expandir e empurrar os botões
                    height=80,  # Altura fixa para 4 linhas (~20px por linha)
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
                max_lines=4,  # Limita a 4 linhas
                overflow=ft.TextOverflow.ELLIPSIS,  # Adiciona ... no final
                text_align=ft.TextAlign.LEFT,  # Mantém alinhamento à esquerda
                expand=False,  # Importante para não expandir e empurrar os botões
                height=80,  # Altura fixa para 4 linhas (~20px por linha)
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