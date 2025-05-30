# Sistema de Estoque da Adega 🍇

Sistema simples de gerenciamento de estoque de bebidas desenvolvido em Python com interface gráfica usando Tkinter.  
Permite adicionar, atualizar, remover bebidas, visualizar imagens das bebidas e gerar relatório em PDF com imagens.

---

## Funcionalidades

- Cadastro de bebidas com nome, tipo, quantidade, preço e imagem.
- Visualização da lista de bebidas em tabela.
- Atualização da quantidade de bebidas.
- Remoção de bebidas cadastradas.
- Visualização da imagem ampliada ao selecionar uma bebida.
- Geração de relatório PDF com os dados do estoque e imagens das bebidas.
- Interface em modo escuro para melhor experiência visual.

---

## Tecnologias utilizadas

- Python 3
- Tkinter (interface gráfica)
- SQLite (banco de dados local)
- Pillow (manipulação de imagens)
- ReportLab (geração de PDFs)

---

## Como usar

1. Clone este repositório:
    ```bash
    git clone https://github.com/seuusuario/nome-do-repositorio.git
    cd nome-do-repositorio
    ```

2. Instale as dependências:
    ```bash
    pip install pillow reportlab
    ```

3. Execute o sistema:
    ```bash
    python seu_arquivo.py
    ```

4. Utilize a interface para adicionar bebidas, selecionar imagens, atualizar quantidades e gerar relatórios.

---

## Estrutura do projeto

├── imagens/ # Pasta onde as imagens das bebidas serão copiadas
├── relatorios/ # Pasta onde os relatórios PDF serão salvos
├── estoque.db # Banco de dados SQLite gerado automaticamente
├── seu_arquivo.py # Código principal do sistema
└── README.md # Documentação do projeto



---

## Observações

- As imagens selecionadas para as bebidas são copiadas para a pasta `imagens` para evitar problemas com caminhos absolutos.
- O relatório PDF é salvo na pasta `relatorios` (criada automaticamente).
- Para melhor experiência, utilize imagens no formato JPG, PNG ou GIF.
- Caso queira personalizar, modifique o arquivo Python principal.

---

## Contato

Desenvolvido por Robson.  
Se tiver dúvidas ou sugestões, abra uma issue ou entre em contato.

---

**Divirta-se gerenciando seu estoque da adega! 🍷🍾**

