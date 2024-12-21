import flet as ft
from addnota import create_note_input

def create_empty_state():
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(
                    name=ft.Icons.LIGHTBULB_OUTLINE,
                    size=120,
                    color="#37383A",
                ),
                ft.Text(
                    "As notas adicionadas são exibidas aqui",
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

def create_view_notas(
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
    close_note,
    pinned_notes_section,
    normal_notes_section,
):
    # Container do input de notas (inicialmente colapsado)
    note_input = ft.Container(
        content=create_note_input(
            input_expanded=input_expanded,
            note_color=note_color,
            is_pinned=is_pinned,
            note_title=note_title,
            note_content=note_content,
            toggle_input=toggle_input,
            toggle_pin=toggle_pin,
            change_color=change_color,
            update_title=update_title,
            update_content=update_content,
            add_note=add_note,
            close_note=close_note
        )
    )

    # Container da área central atualizado com as grades de notas
    return ft.Container(
        content=ft.Column(
            [
                # Container fixo para o input
                ft.Container(
                    content=note_input,
                    padding=ft.padding.only(top=25, left=25, right=25),
                    bgcolor="#202124",
                ),
                # Container com scroll para as notas ou empty state
                ft.Container(
                    content=create_empty_state() if len(pinned_notes_section.controls[1].content.controls) == 0 
                        and len(normal_notes_section.controls[1].content.controls) == 0
                    else ft.Column(
                        [
                            pinned_notes_section,
                            normal_notes_section,
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    expand=True,
                ),
            ],
            spacing=0,
        ),
        expand=True,
    ) 