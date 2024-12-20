import flet as ft
from database import Database

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

    # Lista de cores para as notas
    note_colors = [
        "#28292C",  # Cinza padrão
        "#1E6F50",  # Verde
        "#614A19",  # Marrom
        "#4B443A",  # Bege escuro
        "#662E1E",  # Vermelho escuro
        "#3C3F43",  # Cinza escuro
        "#1A237E",  # Azul escuro
        "#4A148C",  # Roxo escuro
    ]

    def toggle_menu(e):
        nonlocal menu_expanded
        menu_expanded = not menu_expanded
        menu_button.icon = ft.Icons.CLOSE if menu_expanded else ft.Icons.MENU
        
        # Atualiza o menu lateral com os novos estilos
        side_menu.width = 280 if menu_expanded else 72
        side_menu.content.controls = [
            create_menu_item(ft.Icons.LIGHTBULB_OUTLINE, "Notas", selected=True),
            create_menu_item(ft.Icons.ARCHIVE_OUTLINED, "Arquivo"),
            create_menu_item(ft.Icons.DELETE_OUTLINE, "Lixeira"),
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
            create_menu_item(ft.Icons.LIGHTBULB_OUTLINE, "Notas", selected=True),
            create_menu_item(ft.Icons.ARCHIVE_OUTLINED, "Arquivo"),
            create_menu_item(ft.Icons.DELETE_OUTLINE, "Lixeira"),
        ]
        
        side_menu.update()
        page.update()

    def toggle_input(e):
        nonlocal input_expanded
        input_expanded = not input_expanded
        update_note_input()
        page.update()

    def close_note(e):
        nonlocal input_expanded
        input_expanded = False
        update_note_input()
        page.update()

    def create_collapsed_input():
        return ft.Container(
            content=ft.TextField(
                border_color="transparent",
                bgcolor="#28292C",
                text_size=16,
                color="#E2E2E3",
                cursor_color="#E2E2E3",
                hint_text="Criar uma nota...",
                hint_style=ft.TextStyle(
                    color="#E2E2E3",
                    size=16,
                ),
                width=600,
                height=50,
                border_radius=10,
                on_focus=toggle_input,
            ),
            padding=ft.padding.only(top=32),
            alignment=ft.alignment.center,
        )

    def create_expanded_input():
        return ft.Container(
            content=ft.Container(
                content=ft.Column([
                    # Barra superior com título e ícone de fixar
                    ft.Row([
                        ft.TextField(
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
                        ),
                        ft.IconButton(
                            icon=ft.Icons.PUSH_PIN_OUTLINED,
                            icon_color="#E2E2E3",
                            icon_size=20,
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    # Área de conteúdo
                    ft.TextField(
                        border_color="transparent",
                        bgcolor="transparent",
                        text_size=14,
                        color="#E2E2E3",
                        cursor_color="#E2E2E3",
                        hint_text="Criar uma nota...",
                        hint_style=ft.TextStyle(
                            color="#E2E2E3",
                            size=14,
                        ),
                        width=600,
                        height=120,
                        multiline=True,
                    ),

                    # Barra inferior com ícones
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.PALETTE_OUTLINED,
                            icon_color="#E2E2E3",
                            icon_size=20,
                        ),
                        ft.TextButton(
                            text="Fechar",
                            style=ft.ButtonStyle(
                                color="#E2E2E3",
                            ),
                            on_click=close_note,
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ]),
                bgcolor="#28292C",
                padding=10,
                border_radius=10,
                width=600,
            ),
            padding=ft.padding.only(top=32),
            alignment=ft.alignment.center,
        )

    def update_note_input():
        note_input.content = create_expanded_input() if input_expanded else create_collapsed_input()
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

    # Ícone do Keep
    keep_icon = ft.Image(
        src="https://www.gstatic.com/images/branding/product/1x/keep_2020q4_48dp.png",
        width=40,
        height=40,
        fit=ft.ImageFit.CONTAIN,
    )

    # Título
    title = ft.Text(
        "MrKeep",
        color="#E2E2E3",
        size=20,
        weight=ft.FontWeight.W_500
    )

    # Navbar
    navbar = ft.Container(
        content=ft.Row(
            [
                # Grupo da esquerda
                ft.Row(
                    [menu_button, keep_icon, title],
                    spacing=10,
                ),
                # Grupo da direita
                exit_button,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(left=10, right=10),
        height=64,
        bgcolor="#202124",
        border=ft.border.only(bottom=ft.BorderSide(1, "#525355"))
    )

    # Menu Items
    def create_menu_item(icon, text, selected=False):
        # Estilo quando fechado (72px)
        def get_collapsed_style():
            container = ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                name=icon,
                                size=24,
                                color="#E2E2E3",
                            ),
                            bgcolor="#41331C" if selected else None,
                            padding=ft.padding.all(12),
                            border_radius=ft.border_radius.all(50),
                            width=48,
                            height=48,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.padding.only(left=12, top=4, bottom=4),
                animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
            )

            if not selected:
                def handle_hover(e):
                    container.content.controls[0].bgcolor = "#3C3C3C" if e.data == "true" else None
                    container.update()
                container.on_hover = handle_hover

            return container

        # Estilo quando aberto (280px)
        def get_expanded_style():
            container = ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                name=icon,
                                size=24,
                                color="#E2E2E3",
                            ),
                            width=48,
                            height=48,
                            alignment=ft.alignment.center,
                        ),
                        ft.Text(
                            text,
                            color="#E2E2E3",
                            size=16,
                            opacity=1,
                            animate_opacity=300,
                        )
                    ],
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor="#41331C" if selected else None,
                padding=ft.padding.only(left=12, right=12, top=4, bottom=4),
                border_radius=ft.border_radius.only(
                    top_right=28,
                    bottom_right=28
                ),
                margin=ft.margin.only(right=8),
                animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
            )

            if not selected:
                def handle_hover(e):
                    container.bgcolor = "#28292C" if e.data == "true" else None
                    container.update()
                container.on_hover = handle_hover

            return container

        return get_expanded_style() if menu_expanded else get_collapsed_style()

    # Menu Lateral atualizado
    side_menu = ft.Container(
        width=72 if not menu_expanded else 280,
        bgcolor="#202124",
        border=ft.border.only(right=ft.BorderSide(1, "#525355")),
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
        padding=ft.padding.only(top=8, right=0, left=0),
        content=ft.Column(
            [
                create_menu_item(ft.Icons.LIGHTBULB_OUTLINE, "Notas", selected=True),
                create_menu_item(ft.Icons.ARCHIVE_OUTLINED, "Arquivo"),
                create_menu_item(ft.Icons.DELETE_OUTLINE, "Lixeira"),
            ],
            spacing=8,  # Espaçamento entre itens
        ),
        on_hover=handle_menu_hover,
    )

    # Container do input de notas (inicialmente colapsado)
    note_input = ft.Container(
        content=create_collapsed_input(),
    )

    def create_note_card(title, content, is_pinned=False, bgcolor=None):
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
                ]),
                width=240,
                height=120,
                padding=15,
                border_radius=10,
                bgcolor=bgcolor if bgcolor else ("#1E6F50" if is_pinned else "#28292C"),
                data=title,  # Usa o título como identificador
            )

        # Cria o card principal
        card = create_card_content()

        def on_hover(e):
            pin_button.opacity = 1 if e.data == "true" or is_pinned else 0
            card.update()

        card.on_hover = on_hover

        # Container invisível para mostrar durante o drag
        placeholder = ft.Container(
            width=240,
            height=120,
            opacity=0,
        )

        # Cria uma cópia do card para o feedback do drag
        feedback_card = create_card_content()

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
            content_when_dragging=placeholder,  # Container invisível no lugar original
            content_feedback=feedback_card,  # Mostra o card inteiro durante o drag
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
                    controls=[
                        create_note_card("Nota Fixada 1", "Conteúdo da nota fixada 1...", True),
                        create_note_card("Nota Fixada 2", "Conteúdo da nota fixada 2...", True, bgcolor="#614A19"),
                        create_note_card("Nota Fixada 3", "Uma nota fixada mais longa para testar o layout do card...", True, bgcolor="#4A148C"),
                        create_note_card("Nota Fixada 4", "Outra nota fixada com conteúdo diferente...", True, bgcolor="#1A237E"),
                    ],
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
                    controls=[
                        create_note_card("Reunião de Segunda", "Discutir pontos do projeto novo..."),
                        create_note_card("Lista de Compras", "Pão\nLeite\nOvos\nFrutas"),
                        create_note_card("Ideias Projeto", "1. Implementar dark mode\n2. Adicionar animações"),
                        *[
                            create_note_card(
                                f"Nota {i}",
                                f"Conteúdo da nota {i}...\nMais algumas linhas\npara testar o layout",
                                bgcolor=note_colors[i % len(note_colors)]
                            )
                            for i in range(4, 24)
                        ],
                    ],
                ),
            ),
        ],
    )

    # Container da área central atualizado com as grades de notas
    content_area = ft.Container(
        content=ft.Column(
            [
                note_input,
                pinned_notes_section,
                normal_notes_section,
            ],
            scroll=ft.ScrollMode.AUTO,
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

    # Adiciona o container principal à página (ao invs de apenas a navbar)
    page.add(main_container)
    
    # Atualiza a página com as configurações
    page.update()

# Inicia a aplicação
ft.app(main) 