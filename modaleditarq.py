import flet as ft
from addnota import note_colors
from noteoperations import create_note_card_from_data, remove_note_from_sections
from cardarquivo import create_archive_card

def handle_edit_archive(page, db, note_id, card, archive_section, handlers):
    # Estado do modal de edição
    edit_dialog = None
    edit_note_title = ""
    edit_note_content = ""
    edit_note_color = "#28292C"
    
    # Obtém a nota do banco de dados
    nota = db.obter_nota(note_id)
    
    # Atualiza o estado do modal
    edit_note_title = nota[1]  # título
    edit_note_content = nota[2]  # conteúdo
    edit_note_color = nota[8]  # cor

    def handle_restore_from_modal(e):
        # Chama a função de restaurar original
        handlers['on_restore'](e, note_id, card)
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
    
    def change_edit_color(e, color):
        nonlocal edit_note_color, edit_dialog
        edit_note_color = color
        # Atualiza a cor do container do modal
        edit_dialog.content.bgcolor = color
        page.update()
    
    def save_edited_note(e, note_id, handlers):
        # Atualiza a nota no banco de dados
        db.atualizar_nota(
            note_id,
            titulo=edit_note_title,
            conteudo=edit_note_content,
            corFundo=edit_note_color
        )
        
        # Remove o card antigo da seção de arquivo
        for draggable in archive_section.content.controls:
            if draggable.content.content == card:
                archive_section.content.controls.remove(draggable)
                break
        
        # Cria um novo card com os dados atualizados
        novo_card = create_archive_card(
            title=edit_note_title,
            content=edit_note_content,
            bgcolor=edit_note_color,
            note_id=note_id,
            on_color_change=handlers['on_color_change'],
            on_restore=handlers['on_restore'],
            on_delete=handlers['on_delete'],
            on_drag_accept=handlers['on_drag_accept'],
            on_edit=handlers['on_edit'],
            page=page
        )
        
        # Adiciona o novo card na seção de arquivo
        archive_section.content.controls.append(novo_card)
        
        # Fecha o modal
        close_edit_modal(e)
        
        # Atualiza a UI
        page.update()
    
    def close_edit_modal(e):
        nonlocal edit_dialog
        edit_dialog.open = False
        page.update()
    
    # Cria o modal de edição
    edit_dialog = create_edit_archive_modal(
        note_id=note_id,
        note_title=edit_note_title,
        note_content=edit_note_content,
        note_color=edit_note_color,
        change_color=change_edit_color,
        update_title=update_edit_title,
        update_content=update_edit_content,
        save_note=lambda e, id: save_edited_note(e, id, handlers),
        close_modal=close_edit_modal,
        on_restore=handle_restore_from_modal,
        on_delete=handle_delete_from_modal
    )
    
    # Abre o modal
    page.dialog = edit_dialog
    edit_dialog.open = True
    page.update()

def create_edit_archive_modal(
    note_id,
    note_title,
    note_content,
    note_color,
    change_color,
    update_title,
    update_content,
    save_note,
    close_modal,
    on_restore=None,
    on_delete=None,
):
    # Container do modal
    modal_content = ft.Container(
        content=ft.Column([
            # Barra superior com título
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
                    width=600,
                    height=40,
                    on_change=update_title,
                ),
            ]),

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
                            icon=ft.Icons.RESTORE,
                            icon_color="#E2E2E3",
                            icon_size=20,
                            tooltip="Restaurar nota",
                            on_click=on_restore,
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