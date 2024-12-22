import flet as ft

def create_menu_item(icon, text, selected=False, menu_expanded=False, on_click=None, page=None):
    # Estilo quando fechado (72px)
    def get_collapsed_style():
        icon_container = ft.Container(
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
        )

        return ft.TextButton(
            content=ft.Row(
                [icon_container],
                alignment=ft.MainAxisAlignment.START,
            ),
            style=ft.ButtonStyle(
                padding=ft.padding.only(left=12, top=4, bottom=4),
                bgcolor={
                    ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
                    ft.MaterialState.HOVERED: "#28292C" if not selected else None,
                },
                animation_duration=300,
                overlay_color=ft.colors.TRANSPARENT,
            ),
            on_click=on_click,
        )

    # Estilo quando aberto (280px)
    def get_expanded_style():
        return ft.TextButton(
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
            style=ft.ButtonStyle(
                padding=ft.padding.only(left=12, right=12, top=4, bottom=4),
                bgcolor={
                    ft.MaterialState.DEFAULT: "#41331C" if selected else ft.colors.TRANSPARENT,
                    ft.MaterialState.HOVERED: "#28292C" if not selected else None,
                },
                shape=ft.RoundedRectangleBorder(radius=ft.border_radius.only(
                    top_right=28,
                    bottom_right=28
                )),
                animation_duration=300,
                overlay_color=ft.colors.TRANSPARENT,
            ),
            on_click=on_click,
        )

    return get_expanded_style() if menu_expanded else get_collapsed_style()

def create_side_menu(menu_expanded=False, handle_menu_hover=None, selected_page="notas", on_page_change=None, page=None):
    """Cria o menu lateral"""
    
    # Container do menu lateral
    side_menu = ft.Container(
        width=72 if not menu_expanded else 280,
        bgcolor="#202124",
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
        padding=ft.padding.only(top=8, right=0, left=0),
        content=ft.Column(
            [
                create_menu_item(
                    ft.Icons.LIGHTBULB_OUTLINE, 
                    "Notas", 
                    selected=selected_page == "notas", 
                    menu_expanded=menu_expanded,
                    on_click=lambda _: on_page_change("notas") if on_page_change else None,
                    page=page
                ),
                create_menu_item(
                    ft.Icons.ARCHIVE_OUTLINED, 
                    "Arquivo", 
                    selected=selected_page == "arquivo", 
                    menu_expanded=menu_expanded,
                    on_click=lambda _: on_page_change("arquivo") if on_page_change else None,
                    page=page
                ),
                create_menu_item(
                    ft.Icons.DELETE_OUTLINE, 
                    "Lixeira", 
                    selected=selected_page == "lixeira", 
                    menu_expanded=menu_expanded,
                    on_click=lambda _: on_page_change("lixeira") if on_page_change else None,
                    page=page
                ),
            ],
            spacing=8,  # Espaçamento entre itens
        ),
        on_hover=handle_menu_hover,
    )
    
    return side_menu