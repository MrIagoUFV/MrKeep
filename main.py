import flet as ft
from database import Database
from navbar import create_navbar
from menu import create_menu_item, create_side_menu
from addnota import create_note_input, note_colors
from cardnotas import create_note_card
from cardarquivo import create_archive_card
from cardlixeira import create_trash_card
from viewnotas import create_view_notas
from viewarq import create_view_arquivo
from viewtrash import create_view_lixeira
from notesections import create_notes_section
from arquivosections import create_archive_section
from lixeirasections import create_trash_section
from noteoperations import handle_drag_accept, create_note_card_from_data, remove_note_from_sections
from modaleditnotas import handle_edit_note
from modaleditarq import handle_edit_archive

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
    current_page = "notas"  # Estado da página atual

    # Estado do input de notas
    input_expanded = False
    note_color = "#28292C"  # Cor padrão da nota em criação
    is_pinned = False  # Estado de fixação da nota em criação
    note_title = ""  # Estado do título da nota
    note_content = ""  # Estado do conteúdo da nota

    # Estado do modal de edição
    edit_dialog = None
    edit_note_id = None
    edit_note_title = ""
    edit_note_content = ""
    edit_note_color = "#28292C"
    edit_is_pinned = False

    def toggle_menu(e):
        nonlocal menu_expanded
        menu_expanded = not menu_expanded
        menu_button.icon = ft.Icons.CLOSE if menu_expanded else ft.Icons.MENU
        
        # Atualiza o menu lateral com os novos estilos
        side_menu.width = 280 if menu_expanded else 72
        update_side_menu()
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
        
        update_side_menu()
        page.update()

    def handle_page_change(new_page):
        nonlocal current_page
        current_page = new_page
        
        # Carrega as notas apropriadas para cada página
        if new_page == "arquivo":
            load_archived_notes()
        elif new_page == "lixeira":
            load_trash_notes()
        else:  # notas
            load_notes()
        
        update_side_menu()
        update_navbar()
        update_content_area()
        page.update()

    def update_side_menu():
        side_menu.content.controls = [
            create_menu_item(
                ft.Icons.LIGHTBULB_OUTLINE, 
                "Notas", 
                selected=current_page == "notas", 
                menu_expanded=menu_expanded,
                on_click=lambda _: handle_page_change("notas")
            ),
            create_menu_item(
                ft.Icons.ARCHIVE_OUTLINED, 
                "Arquivo", 
                selected=current_page == "arquivo", 
                menu_expanded=menu_expanded,
                on_click=lambda _: handle_page_change("arquivo")
            ),
            create_menu_item(
                ft.Icons.DELETE_OUTLINE, 
                "Lixeira", 
                selected=current_page == "lixeira", 
                menu_expanded=menu_expanded,
                on_click=lambda _: handle_page_change("lixeira")
            ),
        ]
        side_menu.update()

    def update_navbar():
        navbar.content = create_navbar(menu_button, exit_button, current_page).content
        navbar.update()

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
        # Move a nota para a lixeira no banco de dados
        db.atualizar_nota(note_id, lixeira=1)
        
        # Remove o card da interface
        if current_page == "notas":
            remove_note_from_sections(card, pinned_notes_section, normal_notes_section)
        elif current_page == "arquivo":
            for draggable in archive_section.content.controls:
                if draggable.content.content == card:
                    archive_section.content.controls.remove(draggable)
                    break
        
        # Atualiza o content_area baseado na existência de notas
        update_content_area()
        page.update()

    def delete_note_forever(e, note_id, card):
        # Exclui a nota permanentemente do banco de dados
        db.excluir_nota(note_id)
        
        # Remove o card da interface
        for draggable in trash_section.content.controls:
            if draggable.content.content == card:
                trash_section.content.controls.remove(draggable)
                break
        
        # Atualiza o content_area baseado na existência de notas
        update_content_area()
        page.update()

    def restore_note_from_trash(e, note_id, card):
        # Obtém o estado anterior da nota
        nota = db.obter_nota(note_id)
        estava_arquivada = nota[9]  # índice 9 é o campo 'arquivada'
        
        # Restaura a nota no banco de dados
        db.atualizar_nota(note_id, lixeira=0)
        
        # Remove o card da interface da lixeira
        for draggable in trash_section.content.controls:
            if draggable.content.content == card:
                trash_section.content.controls.remove(draggable)
                break
        
        # Se estava arquivada e estamos na página de arquivo, recarrega as notas arquivadas
        if estava_arquivada and current_page == "arquivo":
            load_archived_notes()
        # Se não estava arquivada e estamos na página de notas, recarrega as notas
        elif not estava_arquivada and current_page == "notas":
            load_notes()
        
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

    def restore_note(e, note_id, card):
        # Atualiza a nota como não arquivada no banco de dados
        db.atualizar_nota(note_id, arquivada=0)
        
        # Encontra e remove o Draggable que contém o card
        for draggable in archive_section.content.controls:
            if draggable.content.content == card:
                archive_section.content.controls.remove(draggable)
                break
        
        # Limpa as grades de notas
        pinned_notes_section.controls[1].content.controls.clear()
        normal_notes_section.controls[1].content.controls.clear()
        
        # Recarrega as notas
        load_notes()
        
        # Atualiza o content_area baseado na existência de notas
        update_content_area()
        page.update()

    def load_archived_notes():
        # Carrega todas as notas arquivadas
        notas_arquivadas = db.listar_notas(arquivadas=True)
        
        # Limpa a grade de notas arquivadas
        archive_section.content.controls.clear()
        
        handlers = {
            'on_color_change': change_note_color,
            'on_restore': restore_note,
            'on_delete': delete_note,
            'on_drag_accept': handle_note_drag_accept,
            'on_edit': lambda e, note_id, card: handle_edit_archive(page, db, note_id, card, archive_section, handlers)
        }
        
        for nota in notas_arquivadas:
            # Cria o card
            card = create_archive_card(
                title=nota[1],  # titulo
                content=nota[2],  # conteudo
                bgcolor=nota[8],  # corFundo
                note_id=nota[0],  # id
                on_color_change=handlers['on_color_change'],
                on_restore=handlers['on_restore'],
                on_delete=handlers['on_delete'],
                on_drag_accept=handlers['on_drag_accept'],
                on_edit=handlers['on_edit'],
                page=page
            )
            
            # Adiciona na grade de arquivos
            archive_section.content.controls.append(card)
        
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
                'on_drag_accept': handle_note_drag_accept,
                'on_pin': toggle_pin_note,
                'on_edit': handle_note_edit
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
        if current_page == "notas":
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
        elif current_page == "arquivo":
            content_area.content = create_view_arquivo(archive_section).content
        else:  # lixeira
            content_area.content = create_view_lixeira(trash_section).content

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
    navbar = ft.Container(
        content=create_navbar(menu_button, exit_button, current_page).content,
        padding=ft.padding.only(left=10, right=10),
        height=64,
        bgcolor="#202124",
        border=ft.border.only(bottom=ft.BorderSide(1, "#525355"))
    )

    # Menu Lateral usando o módulo menu.py
    side_menu = create_side_menu(
        menu_expanded=menu_expanded, 
        handle_menu_hover=handle_menu_hover,
        selected_page=current_page,
        on_page_change=handle_page_change,
        page=page
    )

    # Seções de notas usando os módulos apropriados
    pinned_notes_section = create_notes_section("FIXADAS", True)
    normal_notes_section = create_notes_section("OUTRAS", False)
    archive_section = create_archive_section()
    trash_section = create_trash_section()

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

    def toggle_pin_note(e, note_id, card):
        # Obtém a nota atual do banco
        nota = db.obter_nota(note_id)
        novo_estado = not bool(nota[7])  # Inverte o estado atual
        
        # Atualiza no banco de dados
        db.atualizar_nota(note_id, fixada=1 if novo_estado else 0)
        
        # Remove o card da seção atual
        remove_note_from_sections(card, pinned_notes_section, normal_notes_section)
        
        # Cria um novo card com o estado atualizado
        handlers = {
            'on_color_change': change_note_color,
            'on_archive': archive_note,
            'on_delete': delete_note,
            'on_drag_accept': handle_note_drag_accept,
            'on_pin': toggle_pin_note,
            'on_edit': handle_note_edit
        }
        
        novo_card = create_note_card_from_data([
            nota[0],  # id
            nota[1],  # titulo
            nota[2],  # conteudo
            None, None, None, None,
            novo_estado,  # fixada
            nota[8]  # corFundo
        ], handlers, page)
        
        # Adiciona na seção apropriada
        if novo_estado:
            pinned_notes_section.controls[1].content.controls.append(novo_card)
        else:
            normal_notes_section.controls[1].content.controls.append(novo_card)
        
        # Atualiza a UI
        update_content_area()
        page.update()

    def handle_note_edit(e, note_id, card):
        handlers = {
            'on_color_change': change_note_color,
            'on_archive': archive_note,
            'on_delete': delete_note,
            'on_drag_accept': handle_note_drag_accept,
            'on_pin': toggle_pin_note,
            'on_edit': handle_note_edit
        }
        handle_edit_note(page, db, note_id, card, pinned_notes_section, normal_notes_section, handlers)

    def load_notes():
        # Carrega todas as notas ativas (não arquivadas e não na lixeira)
        notas = db.listar_notas()
        
        # Limpa as grades de notas
        pinned_notes_section.controls[1].content.controls.clear()
        normal_notes_section.controls[1].content.controls.clear()
        
        handlers = {
            'on_color_change': change_note_color,
            'on_archive': archive_note,
            'on_delete': delete_note,
            'on_drag_accept': handle_note_drag_accept,
            'on_pin': toggle_pin_note,
            'on_edit': handle_note_edit
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

    def load_trash_notes():
        # Carrega todas as notas da lixeira
        notas_lixeira = db.listar_notas(lixeira=True)
        
        # Limpa a grade de notas da lixeira
        trash_section.content.controls.clear()
        
        handlers = {
            'on_restore': restore_note_from_trash,
            'on_delete_forever': delete_note_forever,
            'on_drag_accept': handle_note_drag_accept
        }
        
        for nota in notas_lixeira:
            # Cria o card
            card = create_trash_card(
                title=nota[1],  # titulo
                content=nota[2],  # conteudo
                bgcolor=nota[8],  # corFundo
                note_id=nota[0],  # id
                on_restore=handlers['on_restore'],
                on_delete_forever=handlers['on_delete_forever'],
                on_drag_accept=handlers['on_drag_accept'],
                page=page
            )
            
            # Adiciona na grade da lixeira
            trash_section.content.controls.append(card)
        
        # Atualiza o content_area baseado na existência de notas
        update_content_area()
        page.update()

# Inicia a aplicação
ft.app(main) 