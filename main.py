import flet as ft
from database import Database
from navbar import create_navbar
from menu import create_menu_item, create_side_menu
from addnota import create_note_input, note_colors

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
            card = create_note_card(
                title=nota['titulo'],
                content=nota['conteudo'],
                is_pinned=is_pinned,
                bgcolor=nota['corFundo'],
                note_id=nota['id']  # Passa o ID da nota
            )
            
            # Adiciona na grade apropriada
            if is_pinned:
                pinned_notes_section.controls[1].content.controls.append(card)
            else:
                normal_notes_section.controls[1].content.controls.append(card)
                
            # Fecha o input
            close_note(e)
            
            # Atualiza o content_area para mostrar as notas ao invés do empty state
            content_area.content.controls[1].content = ft.Column(
                [
                    pinned_notes_section,
                    normal_notes_section,
                ],
                scroll=ft.ScrollMode.AUTO,
            )
            
            # Atualiza a UI
            page.update()

    def update_note_input():
        note_input.content = create_note_input(
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
        note_input.update()

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

    def create_note_card(title, content, is_pinned=False, bgcolor=None, note_id=None):
        # Cria o botão de fixar
        pin_button = ft.IconButton(
            icon=ft.Icons.PUSH_PIN if is_pinned else ft.Icons.PUSH_PIN_OUTLINED,
            icon_color="#E2E2E3",
            icon_size=20,
            opacity=1 if is_pinned else 0,
            visible=True,
        )

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
                                on_click=lambda e, c=color: change_note_color(e, note_id, card, c) if note_id else None
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
                        on_click=lambda e: archive_note(e, note_id, card) if note_id else None,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color="#E2E2E3",
                        icon_size=20,
                        tooltip="Excluir nota",
                        on_click=lambda e: delete_note(e, note_id, card) if note_id else None,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
                opacity=0,
                animate_opacity=300,
            )

            return ft.Container(
                content=ft.Column([
                    # Barra superior com título e ícone de fixar
                    ft.Row([
                        ft.Text(
                            title,
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color="#E2E2E3",
                            expand=True,
                        ),
                        pin_button,
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
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
                bgcolor=bgcolor if bgcolor else ("#1E6F50" if is_pinned else "#28292C"),
                data={"id": note_id, "title": title},  # Armazena o ID e título da nota
            )

        # Cria o card principal
        card = create_card_content()

        def on_hover(e):
            is_hovering = e.data == "true"
            if is_hovering:
                pin_button.opacity = 1
                card.content.controls[-1].opacity = 1  # action_buttons
            else:
                pin_button.opacity = 0
                card.content.controls[-1].opacity = 0  # action_buttons
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
                # Barra superior com título e ícone de fixar
                ft.Row([
                    ft.Text(
                        title,
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color="#E2E2E3",
                        expand=True,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.PUSH_PIN if is_pinned else ft.Icons.PUSH_PIN_OUTLINED,
                        icon_color="#E2E2E3",
                        icon_size=20,
                        opacity=1 if is_pinned else 0,
                        visible=True,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
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
            bgcolor=bgcolor if bgcolor else ("#1E6F50" if is_pinned else "#28292C"),
            margin=ft.margin.only(bottom=20),
        )

        # Cria o DragTarget que vai envolver o card
        drag_target = ft.DragTarget(
            group="notes",
            content=card,
            on_accept=lambda e: handle_drag_accept(e, card),
        )

        # Retorna o Draggable com todas as propriedades necessárias
        return ft.Draggable(
            group="notes",
            content=drag_target,
            content_when_dragging=placeholder,
            content_feedback=feedback_card,
        )

    def handle_drag_accept(e, target_card):
        # Obtém o card de origem e destino
        source_card = e.control.content
        target_content = target_card

        # Obtém as listas de notas
        pinned_grid = pinned_notes_section.controls[1].content
        normal_grid = normal_notes_section.controls[1].content

        # Encontra os índices dos cards
        source_index = -1
        target_index = -1
        grid = None

        # Procura nas notas fixadas
        for i, note in enumerate(pinned_grid.controls):
            if note.content.content == source_card:
                source_index = i
                grid = pinned_grid
                break
            if note.content.content == target_content:
                target_index = i
                grid = pinned_grid
                break

        # Se não encontrou nas fixadas, procura nas normais
        if source_index == -1 and target_index == -1:
            for i, note in enumerate(normal_grid.controls):
                if note.content.content == source_card:
                    source_index = i
                    grid = normal_grid
                    break
                if note.content.content == target_content:
                    target_index = i
                    grid = normal_grid
                    break

        # Se encontrou os dois cards na mesma grade, faz a troca
        if grid and source_index != -1 and target_index != -1:
            grid.controls[source_index], grid.controls[target_index] = \
                grid.controls[target_index], grid.controls[source_index]
            grid.update()

    def delete_note(e, note_id, card):
        # Exclui a nota do banco de dados
        db.excluir_nota(note_id)
        
        # Remove o card da interface
        # Procura nas notas fixadas
        for note in pinned_notes_section.controls[1].content.controls:
            if note.content.content == card:
                pinned_notes_section.controls[1].content.controls.remove(note)
                break
        
        # Se não encontrou nas fixadas, procura nas normais
        for note in normal_notes_section.controls[1].content.controls:
            if note.content.content == card:
                normal_notes_section.controls[1].content.controls.remove(note)
                break
        
        # Verifica se precisa mostrar o empty state
        if len(pinned_notes_section.controls[1].content.controls) == 0 and len(normal_notes_section.controls[1].content.controls) == 0:
            content_area.content.controls[1].content = create_empty_state()
        
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
        # Procura nas notas fixadas
        for note in pinned_notes_section.controls[1].content.controls:
            if note.content.content == card:
                pinned_notes_section.controls[1].content.controls.remove(note)
                break
        
        # Se não encontrou nas fixadas, procura nas normais
        for note in normal_notes_section.controls[1].content.controls:
            if note.content.content == card:
                normal_notes_section.controls[1].content.controls.remove(note)
                break
        
        # Verifica se precisa mostrar o empty state
        if len(pinned_notes_section.controls[1].content.controls) == 0 and len(normal_notes_section.controls[1].content.controls) == 0:
            content_area.content.controls[1].content = create_empty_state()
        
        page.update()

    # Seção de notas fixadas atualizada para usar DragTarget
    pinned_notes_section = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text(
                    "FIXADAS",
                    size=12,
                    weight=ft.FontWeight.W_500,
                    color="#E2E2E3",
                ),
                padding=ft.padding.only(left=30, bottom=10, top=20),
            ),
            ft.Container(
                content=ft.GridView(
                    runs_count=0,
                    max_extent=250,
                    spacing=10,
                    run_spacing=10,
                    padding=30,
                    controls=[],  # Lista vazia de notas fixadas
                ),
            ),
        ],
        visible=True,
    )

    # Seção de notas normais atualizada para usar DragTarget
    normal_notes_section = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text(
                    "OUTRAS",
                    size=12,
                    weight=ft.FontWeight.W_500,
                    color="#E2E2E3",
                ),
                padding=ft.padding.only(left=30, bottom=10, top=20),
            ),
            ft.Container(
                content=ft.GridView(
                    runs_count=0,
                    max_extent=250,
                    spacing=10,
                    run_spacing=10,
                    padding=30,
                    controls=[],  # Lista vazia de notas normais
                ),
            ),
        ],
    )

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

    # Container da área central atualizado com as grades de notas
    content_area = ft.Container(
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

    # Container principal que vai conter a navbar e o menu lateral
    main_container = ft.Container(
        content=ft.Column(
            [
                navbar,
                ft.Row(
                    [
                        side_menu,
                        content_area,  # Substituímos o container vazio pelo content_area
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
        
        for nota in notas:
            # Cria o card
            card = create_note_card(
                title=nota[1],  # titulo
                content=nota[2],  # conteudo
                is_pinned=bool(nota[7]),  # fixada
                bgcolor=nota[8],  # corFundo
                note_id=nota[0]  # id
            )
            
            # Adiciona na grade apropriada
            if nota[7]:  # fixada
                pinned_notes_section.controls[1].content.controls.append(card)
            else:
                normal_notes_section.controls[1].content.controls.append(card)
        
        # Atualiza o content_area baseado na existência de notas
        content_area.content.controls[1].content = create_empty_state() if len(notas) == 0 else ft.Column(
            [
                pinned_notes_section,
                normal_notes_section,
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    
    # Carrega as notas existentes
    load_notes()
    
    # Adiciona o container principal à página (ao invs de apenas a navbar)
    page.add(main_container)
    
    # Atualiza a página com as configurações
    page.update()

# Inicia a aplicação
ft.app(main) 