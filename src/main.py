from html_parser import extract_content
from epub_generator import create_epub

def main():
    # Exemplo de conteúdo HTML
    html_content = """
    <html>
        <body>
            <h1>Hello, World!</h1>
            <p>This is a test.</p>
        </body>
    </html>
    """

    # Extrair conteúdo
    content = extract_content(html_content)

    # Criar EPUB
    create_epub(content, 'My EPUB Book', 'output.epub')

if __name__ == "__main__":
    main()
