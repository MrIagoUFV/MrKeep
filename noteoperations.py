import flet as ft
from cardnotas import create_note_card

def handle_drag_accept(e, target_card, pinned_grid, normal_grid):
    """Gerencia o drag and drop de notas"""
    # Obtém o card de origem e destino
    source_card = e.control.content
    target_content = target_card

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

def create_note_card_from_data(nota, handlers, page):
    """Cria um card de nota a partir dos dados do banco"""
    return create_note_card(
        title=nota[1],  # titulo
        content=nota[2],  # conteudo
        is_pinned=bool(nota[7]),  # fixada
        bgcolor=nota[8],  # corFundo
        note_id=nota[0],  # id
        on_color_change=handlers['on_color_change'],
        on_archive=handlers['on_archive'],
        on_delete=handlers['on_delete'],
        on_drag_accept=handlers['on_drag_accept'],
        on_pin=handlers['on_pin'],
        page=page
    )

def remove_note_from_sections(card, pinned_section, normal_section):
    """Remove um card de nota das seções"""
    # Procura nas notas fixadas
    for note in pinned_section.controls[1].content.controls:
        if note.content.content == card:
            pinned_section.controls[1].content.controls.remove(note)
            return True
    
    # Se não encontrou nas fixadas, procura nas normais
    for note in normal_section.controls[1].content.controls:
        if note.content.content == card:
            normal_section.controls[1].content.controls.remove(note)
            return True
            
    return False 