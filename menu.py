import flet as ft

def create_menu_item(icon, text, selected=False, menu_expanded=False):
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
                container.content.update()
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

def create_side_menu(menu_expanded, handle_menu_hover):
    return ft.Container(
        width=72 if not menu_expanded else 280,
        bgcolor="#202124",
        border=ft.border.only(right=ft.BorderSide(1, "#525355")),
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
        padding=ft.padding.only(top=8, right=0, left=0),
        content=ft.Column(
            [
                create_menu_item(ft.Icons.LIGHTBULB_OUTLINE, "Notas", selected=True, menu_expanded=menu_expanded),
                create_menu_item(ft.Icons.ARCHIVE_OUTLINED, "Arquivo", menu_expanded=menu_expanded),
                create_menu_item(ft.Icons.DELETE_OUTLINE, "Lixeira", menu_expanded=menu_expanded),
            ],
            spacing=8,  # Espaçamento entre itens
        ),
        on_hover=handle_menu_hover,
    ) 