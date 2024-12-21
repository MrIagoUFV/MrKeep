import flet as ft
from cardnotas import create_note_card

def handle_drag_accept(e, target_card, pinned_grid, normal_grid, db=None):
    """Gerencia o drag and drop de notas"""
    if not db:
        return
        
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
        # Obtém os IDs das notas
        source_id = grid.controls[source_index].content.content.data.get("id")
        target_id = grid.controls[target_index].content.content.data.get("id")
        
        # Obtém as ordens atuais
        source_nota = db.obter_nota(source_id)
        target_nota = db.obter_nota(target_id)
        
        if source_nota and target_nota:
            # Calcula a nova ordem para a nota de origem
            if target_index > source_index:
                # Movendo para baixo
                if target_index < len(grid.controls) - 1:
                    # Se não for o último, pega a média entre o alvo e o próximo
                    next_nota = db.obter_nota(grid.controls[target_index + 1].content.content.data.get("id"))
                    nova_ordem = (target_nota[12] + next_nota[12]) / 2  # índice 12 é o campo ordem
                else:
                    # Se for o último, adiciona 1000 à ordem do alvo
                    nova_ordem = target_nota[12] + 1000
            else:
                # Movendo para cima
                if target_index > 0:
                    # Se não for o primeiro, pega a média entre o anterior e o alvo
                    prev_nota = db.obter_nota(grid.controls[target_index - 1].content.content.data.get("id"))
                    nova_ordem = (prev_nota[12] + target_nota[12]) / 2
                else:
                    # Se for o primeiro, subtrai 1000 da ordem do alvo
                    nova_ordem = target_nota[12] - 1000
            
            # Atualiza a ordem no banco de dados
            db.atualizar_ordem(source_id, nova_ordem)
            
            # Atualiza a ordem na interface
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
        on_edit=handlers['on_edit'],
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