import flet as ft

def main(page: ft.Page):
    # Configurações da página
    page.title = "MrKeep"
    page.window_maximized = True
    page.window_title_bar_hidden = True
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#202124"
    page.padding = 0
    
    # Atualiza a página com as configurações
    page.update()

# Inicia a aplicação
ft.app(main) 