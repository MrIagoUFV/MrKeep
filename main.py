import flet as ft
from database import Database
from navbar import create_navbar
from menu import create_menu_item, create_side_menu
from addnota import create_note_input, note_colors
from cardnotas import create_note_card
from viewnotas import create_view_notas
from notesections import create_notes_section
from noteoperations import handle_drag_accept, create_note_card_from_data, remove_note_from_sections

def main(page: ft.Page):
    # Inicializa o banco de dados
    db = Database()
    
    # Configurações da página
    page.title = "MrKeep"
    page.window.maximized = True
    page.window.title_bar_hidden = True
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#202124"
    page.padding = 0

    # Estado do menu
    menu_expanded = False

    # Estado do input de notas
    input_expanded = False
    note_color = "#28292C"  # Cor padrão da nota em criação
    is_pinned = False  # Estado de fixação da nota em criação
    note_title = ""  # Estado do título da nota
    note_content = ""  # Estado do conteúdo da nota

    def toggle_menu(e):
        nonlocal menu_expanded
        menu_expanded = not menu_expanded
        menu_button.icon = ft.Icons.CLOSE if menu_expanded else ft.Icons.MENU
        
        # Atualiza o menu lateral com os novos estilos
        side_menu.width = 280 if menu_expanded else 72
        side_menu.content.controls = [
            create_menu_item(ft.Icons.LIGHTBULB_OUTLINE, "Notas", selected=True, menu_expanded=menu_expanded),
            create_menu_item(ft.Icons.ARCHIVE_OUTLINED, "Arquivo", menu_expanded=menu_expanded),
            create_menu_item(ft.Icons.DELETE_OUTLINE, "Lixeira", menu_expanded=menu_expanded),
        ]
        
        side_menu.update()
        page.update()

    def exit_app(e):
        page.window.close()

    def handle_menu_hover(e):
        nonlocal menu_expanded
        # Abre o menu quando o mouse entra
        if e.data == "true":
            menu_expanded = True
        # Fecha o menu quando o mouse sai
        else:
            menu_expanded = False
            
        menu_button.icon = ft.Icons.CLOSE if menu_expanded else ft.Icons.MENU
        side_menu.width = 280 if menu_expanded else 72
        
        # Recria os itens do menu com o estilo apropriado
        side_menu.content.controls = [
            create_menu_item(ft.Icons.LIGHTBULB_OUTLINE, "Notas", selected=True, menu_expanded=menu_expanded),
            create_menu_item(ft.Icons.ARCHIVE_OUTLINED, "Arquivo", menu_expanded=menu_expanded),
            create_menu_item(ft.Icons.DELETE_OUTLINE, "Lixeira", menu_expanded=menu_expanded),
        ]
        
        side_menu.update()
        page.update()

    def toggle_input(e):
        nonlocal input_expanded
        input_expanded = not input_expanded
        update_note_input()
        page.update()

    def close_note(e):
        nonlocal input_expanded, note_color, is_pinned, note_title, note_content
        input_expanded = False
        note_color = "#28292C"  # Reseta para a cor padrão
        is_pinned = False  # Reseta o estado de fixação
        note_title = ""  # Reseta o título
        note_content = ""  # Reseta o conteúdo
        update_note_input()
        page.update()

    def toggle_pin(e):
        nonlocal is_pinned
        is_pinned = not is_pinned
        # Atualiza o ícone do botão que disparou o evento
        e.control.icon = ft.Icons.PUSH_PIN if is_pinned else ft.Icons.PUSH_PIN_OUTLINED
        page.update()

    def change_color(e, color):
        nonlocal note_color
        note_color = color
        # Atualiza a cor do container do input expandido
        # Como o input é recriado a cada mudança, a próxima vez que for
        # renderizado já terá a nova cor
        update_note_input()
        page.update()

    def update_title(e):
        nonlocal note_title
        note_title = e.control.value

    def update_content(e):
        nonlocal note_content
        note_content = e.control.value

    def handle_note_drag_accept(e, target_card):
        handle_drag_accept(
            e, 
            target_card, 
            pinned_notes_section.controls[1].content,
            normal_notes_section.controls[1].content
        )

    def delete_note(e, note_id, card):
        # Exclui a nota do banco de dados
        db.excluir_nota(note_id)
        
        # Remove o card da interface
        remove_note_from_sections(card, pinned_notes_section, normal_notes_section)
        
        # Atualiza o content_area baseado na existência de notas
        update_content_area()
        page.update()

    def change_note_color(e, note_id, card, new_color):
        # Atualiza a cor no banco de dados
        db.atualizar_nota(note_id, corFundo=new_color)
        
        # Atualiza a cor do card na interface
        card.bgcolor = new_color
        
        # Atualiza a página inteira ao invés do card individual
        page.update()

    def archive_note(e, note_id, card):
        # Atualiza a nota como arquivada no banco de dados
        db.atualizar_nota(note_id, arquivada=1)
        
        # Remove o card da interface
        remove_note_from_sections(card, pinned_notes_section, normal_notes_section)
        
        # Atualiza o content_area baseado na existência de notas
        update_content_area()
        page.update()

    def add_note(e):
        nonlocal note_title, note_content, is_pinned, note_color
        if note_title.strip():  # Só cria se tiver título
            # Salva no banco
            nota = db.criar_nota(
                titulo=note_title,
                conteudo=note_content,
                cor_fundo=note_color
            )
            
            if is_pinned:
                db.atualizar_nota(nota['id'], fixada=1)
                nota['fixada'] = 1
            
            # Cria o card
            handlers = {
                'on_color_change': change_note_color,
                'on_archive': archive_note,
                'on_delete': delete_note,
                'on_drag_accept': handle_note_drag_accept
            }
            
            card = create_note_card_from_data([
                nota['id'],
                nota['titulo'],
                nota['conteudo'],
                None, None, None, None,
                nota.get('fixada', 0),
                nota['corFundo']
            ], handlers, page)
            
            # Adiciona na grade apropriada
            if is_pinned:
                pinned_notes_section.controls[1].content.controls.append(card)
            else:
                normal_notes_section.controls[1].content.controls.append(card)
                
            # Fecha o input
            close_note(e)
            
            # Atualiza o content_area
            update_content_area()
            
            # Atualiza a UI
            page.update()

    def update_content_area():
        content_area.content = create_view_notas(
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
            close_note=close_note,
            pinned_notes_section=pinned_notes_section,
            normal_notes_section=normal_notes_section,
        ).content

    def update_note_input():
        update_content_area()
        content_area.update()

    # Ícone do menu hamburguer
    menu_button = ft.IconButton(
        icon=ft.Icons.MENU,
        icon_color="#E2E2E3",
        on_click=toggle_menu,
        icon_size=24,
    )

    # Ícone de sair
    exit_button = ft.IconButton(
        icon=ft.Icons.EXIT_TO_APP,
        icon_color="#E2E2E3",
        on_click=exit_app,
        icon_size=24,
    )

    # Navbar usando o módulo navbar.py
    navbar = create_navbar(menu_button, exit_button)

    # Menu Lateral usando o módulo menu.py
    side_menu = create_side_menu(menu_expanded, handle_menu_hover)

    # Seções de notas usando o módulo notesections.py
    pinned_notes_section = create_notes_section("FIXADAS", True)
    normal_notes_section = create_notes_section("OUTRAS", False)

    # Container da área central atualizado com as grades de notas
    content_area = ft.Container(
        content=create_view_notas(
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
            close_note=close_note,
            pinned_notes_section=pinned_notes_section,
            normal_notes_section=normal_notes_section,
        ).content,
        expand=True,
    )

    # Container principal que vai conter a navbar e o menu lateral
    main_container = ft.Container(
        content=ft.Column(
            [
                navbar,
                ft.Row(
                    [
                        side_menu,
                        content_area,
                    ],
                    expand=True,
                    spacing=0,
                ),
            ],
            spacing=0,
            expand=True,
        ),
        expand=True,
    )

    def load_notes():
        # Carrega todas as notas ativas (não arquivadas e não na lixeira)
        notas = db.listar_notas()
        
        handlers = {
            'on_color_change': change_note_color,
            'on_archive': archive_note,
            'on_delete': delete_note,
            'on_drag_accept': handle_note_drag_accept
        }
        
        for nota in notas:
            # Cria o card
            card = create_note_card_from_data(nota, handlers, page)
            
            # Adiciona na grade apropriada
            if nota[7]:  # fixada
                pinned_notes_section.controls[1].content.controls.append(card)
            else:
                normal_notes_section.controls[1].content.controls.append(card)
        
        # Atualiza o content_area baseado na existência de notas
        update_content_area()
    
    # Carrega as notas existentes
    load_notes()
    
    # Adiciona o container principal à página
    page.add(main_container)
    
    # Atualiza a página com as configurações
    page.update()

# Inicia a aplicação
ft.app(main) 