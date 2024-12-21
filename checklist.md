# CHEKLIST DE DESENVOLVIMENTO

Ainda falta:

## VIEWS

- Criar a visualização e funcionalidade de lixeira

    - Visualização:
        - Criar lixeirasections.py (DRY: usar o que for útil do notesections.py)
            - Quando houver notas na lixeira:
                - Mostrar a grade de notas com as notas da lixeira
                    - Na lixeira, as notas não podem ser fixadas, ou seja, só existe uma seção de grade.
                    - A grade de notas deve ter o mesmo estilo e comportamento das notas da página inicial, porém não tem título como "Lixeira", "outras notas", "fixadas" etc.
            - Quando não houver notas na lixeira:
                    - Mostrar a tela de lixeira vazia (similar à tela de arquivo vazio)
                    
    - Cards de notas lixeira:
        - Criar o cardlixeira.py (DRY: usar o que for útil do cardnotas.py)
            - O card de lixeira tem o mesmo comportamento do card de notas, porém tem os icones diferentes:
                - Não tem o ícone de fixar e icone de mudar cor de fundo
                - Tem o ícone de restaurar no lugar do ícone de arquivar
                - Tem o ícone de excluir permanentemente no lugar do ícone de excluir normal
            - Criar o action handler de cada icone do card da lixeira:
                - Restaurar:
                    - Restaurar a nota atualiza o db para retirar o estado de lixeira e tira ela da view de lixeira, e volta para a view de anterior:
                        - Se estava na view de arquivos, volta para a view de arquivos
                        - Se estava na view de notas, volta para a view de notas
                - Excluir permanentemente:
                    - Excluir a nota permanentemente do banco de dados (diferente da exclusão normal que só move para a lixeira)

    - Atualizar as funções de card da página inicial:

        - Ao clicar em arquivar: fazer as funções de arquivar corretamente no db
        - Ao clicar em deletar: fazer as funções de deletar corretamente no db para mandar para a lixeira (não excluir permanentemente)


## DND

- Criar a funcionalidade de reordenação de notas nos arquivos com drag and drop

- Criar a funcionalidade de reordenação de notas na página de visualização de notas com drag and drop

## FIXAR E DESFIXAR

- Criar a funcionalidade de fixar e desfixar notas na página de visualização de notas



