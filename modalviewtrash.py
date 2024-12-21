import flet as ft

def handle_view_trash(page, db, note_id, card, trash_section, handlers):
    # Estado do modal de visualização
    view_dialog = None
    note_title = ""
    note_content = ""
    note_color = "#28292C"
    
    # Obtém a nota do banco de dados
    nota = db.obter_nota(note_id)
    
    # Atualiza o estado do modal
    note_title = nota[1]  # título
    note_content = nota[2]  # conteúdo
    note_color = nota[8]  # cor

    def handle_restore_from_modal(e):
        # Chama a função de restaurar original
        handlers['on_restore'](e, note_id, card)
        # Fecha o modal
        close_view_modal(e)

    def handle_delete_forever_from_modal(e):
        # Chama a função de excluir original
        handlers['on_delete_forever'](e, note_id, card)
        # Fecha o modal
        close_view_modal(e)
    
    def close_view_modal(e):
        nonlocal view_dialog
        view_dialog.open = False
        page.update()
    
    # Cria o modal de visualização
    view_dialog = create_view_trash_modal(
        note_id=note_id,
        note_title=note_title,
        note_content=note_content,
        note_color=note_color,
        close_modal=close_view_modal,
        on_restore=handle_restore_from_modal,
        on_delete_forever=handle_delete_forever_from_modal
    )
    
    # Abre o modal
    page.dialog = view_dialog
    view_dialog.open = True
    page.update()

def create_view_trash_modal(
    note_id,
    note_title,
    note_content,
    note_color,
    close_modal,
    on_restore=None,
    on_delete_forever=None,
):
    # Container do modal
    modal_content = ft.Container(
        content=ft.Column([
            # Barra superior com título
            ft.Row([
                ft.Text(
                    value=note_title,
                    size=16,
                    color="#E2E2E3",
                    weight=ft.FontWeight.W_500,
                    width=600,
                ),
            ]),

            # Área de conteúdo
            ft.Text(
                value=note_content,
                size=14,
                color="#E2E2E3",
                opacity=0.8,
                width=600,
                expand=True,
                selectable=True,
            ),

            # Barra inferior com ícones
            ft.Container(
                content=ft.Row([
                    # Grupo de ícones da esquerda
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.RESTORE,
                            icon_color="#E2E2E3",
                            icon_size=20,
                            tooltip="Restaurar nota",
                            on_click=on_restore,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_FOREVER,
                            icon_color="#E2E2E3",
                            icon_size=20,
                            tooltip="Excluir permanentemente",
                            on_click=on_delete_forever,
                        ),
                    ], spacing=0),

                    # Botão de fechar à direita
                    ft.Row([
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