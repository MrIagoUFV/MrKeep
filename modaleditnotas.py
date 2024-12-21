import flet as ft
from addnota import note_colors
from noteoperations import create_note_card_from_data, remove_note_from_sections

def handle_edit_note(page, db, note_id, card, pinned_section, normal_section, handlers):
    # Estado do modal de edição
    edit_dialog = None
    edit_note_title = ""
    edit_note_content = ""
    edit_note_color = "#28292C"
    edit_is_pinned = False
    
    # Obtém a nota do banco de dados
    nota = db.obter_nota(note_id)
    
    # Atualiza o estado do modal
    edit_note_title = nota[1]  # título
    edit_note_content = nota[2]  # conteúdo
    edit_note_color = nota[8]  # cor
    edit_is_pinned = bool(nota[7])  # fixada
    
    def handle_archive_from_modal(e):
        # Chama a função de arquivar original
        handlers['on_archive'](e, note_id, card)
        # Fecha o modal
        close_edit_modal(e)

    def handle_delete_from_modal(e):
        # Chama a função de excluir original
        handlers['on_delete'](e, note_id, card)
        # Fecha o modal
        close_edit_modal(e)
    
    # Funções específicas para o modal de edição
    def update_edit_title(e):
        nonlocal edit_note_title
        edit_note_title = e.control.value
    
    def update_edit_content(e):
        nonlocal edit_note_content
        edit_note_content = e.control.value
    
    def toggle_edit_pin(e):
        nonlocal edit_is_pinned
        edit_is_pinned = not edit_is_pinned
        # Atualiza o ícone do botão que disparou o evento
        e.control.icon = ft.Icons.PUSH_PIN if edit_is_pinned else ft.Icons.PUSH_PIN_OUTLINED
        page.update()
    
    def change_edit_color(e, color):
        nonlocal edit_note_color, edit_dialog
        edit_note_color = color
        # Atualiza a cor do container do modal
        edit_dialog.content.bgcolor = color
        page.update()
    
    def save_edited_note(e, note_id, handlers):
        # Obtém a nota atual para preservar a ordem
        nota_atual = db.obter_nota(note_id)
        ordem_atual = nota_atual[-1] if len(nota_atual) > 11 else 0
        
        # Atualiza a nota no banco de dados
        db.atualizar_nota(
            note_id,
            titulo=edit_note_title,
            conteudo=edit_note_content,
            corFundo=edit_note_color,
            fixada=1 if edit_is_pinned else 0,
            ordem=ordem_atual  # Mantém a ordem original
        )
        
        # Encontra a posição atual do card
        index = None
        section = None
        
        # Procura nas notas fixadas
        for i, note in enumerate(pinned_section.controls[1].content.controls):
            if note.content.content == card:
                index = i
                section = pinned_section.controls[1].content
                break
        
        # Se não encontrou nas fixadas, procura nas normais
        if index is None:
            for i, note in enumerate(normal_section.controls[1].content.controls):
                if note.content.content == card:
                    index = i
                    section = normal_section.controls[1].content
                    break
        
        # Remove o card antigo
        remove_note_from_sections(card, pinned_section, normal_section)
        
        # Cria um novo card com os dados atualizados
        novo_card = create_note_card_from_data([
            note_id,
            edit_note_title,
            edit_note_content,
            None, None, None, None,
            edit_is_pinned,
            edit_note_color
        ], handlers, page)
        
        # Adiciona o novo card na seção apropriada mantendo a posição
        target_section = pinned_section.controls[1].content if edit_is_pinned else normal_section.controls[1].content
        
        if section == target_section:
            # Se continua na mesma seção, mantém a posição
            target_section.controls.insert(index, novo_card)
        else:
            # Se mudou de seção, adiciona no final
            target_section.controls.append(novo_card)
        
        # Fecha o modal
        close_edit_modal(e)
        
        # Atualiza a UI
        page.update()
    
    def close_edit_modal(e):
        nonlocal edit_dialog
        edit_dialog.open = False
        page.update()
    
    # Cria o modal de edição
    edit_dialog = create_edit_modal(
        note_id=note_id,
        note_title=edit_note_title,
        note_content=edit_note_content,
        note_color=edit_note_color,
        is_pinned=edit_is_pinned,
        toggle_pin=toggle_edit_pin,
        change_color=change_edit_color,
        update_title=update_edit_title,
        update_content=update_edit_content,
        save_note=lambda e, id: save_edited_note(e, id, handlers),
        close_modal=close_edit_modal,
        on_archive=handle_archive_from_modal,
        on_delete=handle_delete_from_modal
    )
    
    # Abre o modal
    page.dialog = edit_dialog
    edit_dialog.open = True
    page.update()

def create_edit_modal(
    note_id,
    note_title,
    note_content,
    note_color,
    is_pinned,
    toggle_pin,
    change_color,
    update_title,
    update_content,
    save_note,
    close_modal,
    on_archive=None,
    on_delete=None,
):
    # Container do modal
    modal_content = ft.Container(
        content=ft.Column([
            # Barra superior com título e ícone de fixar
            ft.Row([
                ft.TextField(
                    value=note_title,
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
                    on_change=update_title,
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
                value=note_content,
                border_color="transparent",
                bgcolor="transparent",
                text_size=14,
                color="#E2E2E3",
                cursor_color="#E2E2E3",
                hint_text="Digite uma nota...",
                hint_style=ft.TextStyle(
                    color="#E2E2E3",
                    size=14,
                ),
                width=600,
                expand=True,
                multiline=True,
                min_lines=1,
                max_lines=None,
                on_change=update_content,
            ),

            # Barra inferior com ícones
            ft.Container(
                content=ft.Row([
                    # Grupo de ícones da esquerda
                    ft.Row([
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
                                    on_click=lambda e, c=color: change_color(e, c)
                                ) for color, name in zip(note_colors, [
                                    "Cinza padrão", "Verde", "Marrom", "Bege escuro",
                                    "Vermelho escuro", "Cinza escuro", "Azul escuro", "Roxo escuro"
                                ])
                            ],
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ARCHIVE_OUTLINED,
                            icon_color="#E2E2E3",
                            icon_size=20,
                            tooltip="Arquivar nota",
                            on_click=on_archive,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color="#E2E2E3",
                            icon_size=20,
                            tooltip="Excluir nota",
                            on_click=on_delete,
                        ),
                    ], spacing=0),

                    # Grupo de botões da direita
                    ft.Row([
                        ft.ElevatedButton(
                            "Salvar",
                            icon=ft.Icons.SAVE,
                            on_click=lambda e: save_note(e, note_id),
                            style=ft.ButtonStyle(
                                color="#E2E2E3",
                                bgcolor="#1E6F50"
                            ),
                        ),
                        ft.TextButton(
                            text="Fechar",
                            style=ft.ButtonStyle(
                                color="#E2E2E3",
                            ),
                            on_click=close_modal,
                        ),
                    ], spacing=10),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.only(top=10),
            ),
        ], spacing=0),
        bgcolor=note_color,
        padding=10,
        border_radius=10,
        width=600,
        height=500,
    )

    # Cria o AlertDialog
    return ft.AlertDialog(
        modal=True,
        content=modal_content,
        inset_padding=20,
        actions_padding=0,
        actions_alignment=ft.MainAxisAlignment.END,
    ) 