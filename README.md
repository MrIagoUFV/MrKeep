# MrKeep

Esse projeto foi desenvolvido com o objetivo de demonstrar a atual capacidade da IA na programação quando usada da forma correta. Foi inteiramente desenvolvido por IA, com a ajuda de um humano para corrigir alguns erros. 

Eu gravei todo o processo: (em edição)

MrKeep é um clone do Google Keep desenvolvido em Python usando o framework Flet. É um aplicativo de notas que permite aos usuários criar, organizar e gerenciar suas anotações de forma eficiente.

![Gif Demonstração](<keep gif use.gif>)

## Comunidade e Missão

Esse foi o primeiro projeto para minha Comunidade de Programação com IA. 

Meu propósito é colaborar com material de qualidade que sirva de base para educação nessa nova era da programação. 

Além de:
- Formar a vanguarda dos programadores com IA no Brasil
- Conectar profissionais e entusiastas da área
- Desenvolver e compartilhar as melhores práticas de programação com IA
- Fomentar projetos inovadores em nossa comunidade

O que você irá encontrar ao Participar da Comunidade (em breve):
- Cursos completos de programação com IA.
- Projetos completos com IA, com todo processo de desenvolvimento gravado.
- Grupo de networking com profissionais e entusiastas da área.

Se você gostou da ideia e quer aprender com mais projetos, te convido a participar do nosso grupo gratuito e se inscrever no canal do Youtube:
- Grupo Whats: https://chat.whatsapp.com/CP7zu5ebSRY2RCiq5g8Slu
- Canal Youtube: https://www.youtube.com/@mriago

## 🚀 Funcionalidades

- ✏️ Criação de notas com título e conteúdo
- 📌 Fixação de notas importantes
- 🎨 Personalização com diferentes cores
- 📁 Arquivamento de notas
- 🗑️ Sistema de lixeira com restauração
- 🖱️ Suporte a drag and drop
- 🌙 Tema escuro
- 📱 Interface responsiva

## 📋 Pré-requisitos

- Python 3.7 ou superior
- Flet
- SQLite (para o banco de dados)

## 🔧 Instalação

![Gif Instalação](<keep gif install.gif>)

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/MrKeep.git
cd MrKeep
```

2. Instale as dependências:
```bash
pip install flet
```

3. Execute o aplicativo:
```bash
python main.py
```

## 💡 Como Usar

### Criar uma Nota
- Clique no campo "Criar uma nota..." para expandir o editor
- Digite um título e conteúdo
- Use os botões na barra inferior para:
  - Fixar/Desafixar a nota
  - Mudar a cor da nota
  - Salvar a nota

### Gerenciar Notas
- **Fixar**: Clique no ícone de alfinete para fixar/desafixar uma nota
- **Arquivar**: Use o ícone de arquivo para mover a nota para o arquivo
- **Excluir**: Mova a nota para a lixeira usando o ícone de lixeira
- **Restaurar**: Na lixeira, use o botão de restauração para recuperar notas
- **Arrastar e Soltar**: Reorganize as notas arrastando-as para diferentes seções

### Navegação
- Use o menu lateral para alternar entre:
  - Notas
  - Arquivo
  - Lixeira

## 🗑️ Sistema de Lixeira
- As notas na lixeira são automaticamente excluídas após 7 dias
- É possível restaurar notas da lixeira antes da exclusão permanente
- Notas podem ser excluídas permanentemente manualmente

## 🎨 Personalização
O aplicativo oferece várias cores predefinidas para personalizar suas notas:
- Cinza (padrão)
- Vermelho
- Verde
- Azul
- Amarelo
- E outras cores

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/) - Linguagem de programação
- [Flet](https://flet.dev/) - Framework para construção da interface
- SQLite - Banco de dados

## ✨ Recursos Especiais

- Interface moderna e intuitiva
- Barra de título personalizada
- Tema escuro por padrão
- Menu lateral retrátil
- Sistema de drag and drop intuitivo

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request 