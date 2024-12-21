import flet as ft
from addnota import note_colors

def create_archive_card(title, content, bgcolor=None, note_id=None, 
                       on_color_change=None, on_restore=None, on_delete=None, 
                       on_drag_accept=None, on_edit=None, page=None, db=None,
                       archive_section=None):
    """Cria um card de nota arquivada"""
    
    # Variável para rastrear o último card com hover
    last_hover_card = None
    
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
                    icon=ft.Icons.EDIT_OUTLINED,
                    icon_color="#E2E2E3",
                    icon_size=20,
                    tooltip="Editar nota",
                    on_click=lambda e: on_edit(e, note_id, card) if on_edit else None,
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

    def on_drag_start(e):
        if db:
            # Armazena o ID e ordem do card sendo arrastado
            nota = db.obter_nota(note_id)
            if nota:
                # Armazena os dados no Draggable
                e.control.data = {
                    "id": note_id,
                    "ordem": nota[-1] if len(nota) > 11 else 0  # último índice é ordem
                }
                # Armazena os dados no DragTarget também
                e.control.content.data = e.control.data

    def on_will_accept(e):
        nonlocal last_hover_card
        # Armazena o card que está recebendo o hover
        last_hover_card = e.control.content
        # Visual feedback
        card.elevation = 20
        card.border = ft.border.all(2, "#1E6F50")
        page.update()

    def on_leave(e):
        nonlocal last_hover_card
        # Limpa o último card com hover
        last_hover_card = None
        # Remove visual feedback
        card.elevation = 1
        card.border = None
        page.update()

    def on_accept(e):
        if not db:
            return

        # Obtém o ID da nota de origem do Draggable
        src = page.get_control(e.src_id)
        if not src or not src.data or "id" not in src.data:
            return
        source_id = src.data["id"]

        # Inicializa nova_ordem com um valor padrão
        nova_ordem = 0

        # Se tiver um card com hover, usa sua ordem
        if last_hover_card and last_hover_card.data:
            target_id = last_hover_card.data.get("id")
            if target_id:
                target_nota = db.obter_nota(target_id)
                if target_nota:
                    # Obtém a grid do arquivo
                    grid = archive_section.content

                    if grid and hasattr(grid, "controls"):
                        next_nota = None
                        target_ordem = target_nota[-1] if len(target_nota) > 11 else 0
                        
                        # Procura o próximo card após o target
                        for i, draggable in enumerate(grid.controls):
                            current_id = draggable.content.content.data.get("id")
                            if current_id == target_id:  # Encontrou o card alvo
                                if i < len(grid.controls) - 1:
                                    next_id = grid.controls[i+1].content.content.data.get("id")
                                    if next_id:
                                        next_nota = db.obter_nota(next_id)
                                break
                        
                        # Calcula nova ordem
                        if next_nota and len(next_nota) > 11:
                            # Se tem próximo card, coloca na média entre os dois
                            next_ordem = next_nota[-1]
                            nova_ordem = target_ordem + ((next_ordem - target_ordem) / 2)
                        else:
                            # Se é o último, adiciona 1000 à ordem do target
                            nova_ordem = target_ordem + 1000
        
        # Se não tiver hover ou se algo deu errado, coloca no final
        if nova_ordem == 0:
            ultima_ordem = db.obter_ultima_ordem(arquivada=True)
            nova_ordem = ultima_ordem + 1000
        
        # Atualiza a ordem no banco
        db.atualizar_ordem(source_id, nova_ordem)

        # Remove visual feedback
        card.elevation = 1
        card.border = None

        # Recarrega as notas
        if archive_section:
            # Limpa a seção
            archive_section.content.controls.clear()
            
            # Recarrega as notas do banco
            notas = db.listar_notas(arquivadas=True)
            
            # Recria os cards com os mesmos handlers
            handlers = {
                'on_color_change': on_color_change,
                'on_restore': on_restore,
                'on_delete': on_delete,
                'on_drag_accept': on_drag_accept,
                'on_edit': on_edit
            }
            
            for nota in notas:
                novo_card = create_archive_card(
                    title=nota[1],  # titulo
                    content=nota[2],  # conteudo
                    bgcolor=nota[8],  # corFundo
                    note_id=nota[0],  # id
                    on_color_change=handlers['on_color_change'],
                    on_restore=handlers['on_restore'],
                    on_delete=handlers['on_delete'],
                    on_drag_accept=handlers['on_drag_accept'],
                    on_edit=handlers['on_edit'],
                    page=page,
                    db=db,
                    archive_section=archive_section
                )
                
                # Adiciona na seção de arquivo
                archive_section.content.controls.append(novo_card)

        page.update()

        # Chama o callback original se existir
        if on_drag_accept:
            on_drag_accept(e, card)

    # Cria o DragTarget que vai envolver o card
    drag_target = ft.DragTarget(
        group="notes",
        content=card,
        on_accept=on_accept,
        on_will_accept=on_will_accept,
        on_leave=on_leave,
        data={"id": note_id}  # Armazena o ID no DragTarget também
    )

    # Retorna o Draggable com todas as propriedades necessárias
    return ft.Draggable(
        group="notes",
        content=drag_target,
        content_when_dragging=placeholder,
        content_feedback=feedback_card,
        on_drag_start=on_drag_start,
        data={"id": note_id}  # Armazena o ID no Draggable também
    ) 