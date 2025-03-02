from ebooklib import epub

def create_epub(content, title, output_path):
    """
    Cria um arquivo EPUB a partir do conteúdo extraído.

    :param content: Conteúdo HTML extraído.
    :param title: Título do EPUB.
    :param output_path: Caminho para salvar o arquivo EPUB.
    """
    book = epub.EpubBook()

    # Definir metadados
    book.set_identifier('id123456')
    book.set_title(title)
    book.set_language('en')

    # Criar um capítulo
    chapter = epub.EpubHtml(title='Chapter 1', file_name='chap_1.xhtml', lang='en')
    chapter.content = content

    # Adicionar capítulo ao livro
    book.add_item(chapter)

    # Adicionar itens de navegação
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Definir a espinha do livro
    book.spine = ['nav', chapter]

    # Gerar o arquivo EPUB
    epub.write_epub(output_path, book, {})
