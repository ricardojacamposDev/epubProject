from bs4 import BeautifulSoup
from ebooklib import epub

def html_to_epub(html_content, epub_title):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create a new EPUB book
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier('id123456')
    book.set_title(epub_title)
    book.set_language('en')

    # Create a chapter
    chapter = epub.EpubHtml(title='Chapter 1', file_name='chap_1.xhtml', lang='en')
    chapter.content = soup.prettify()

    # Add chapter to the book
    book.add_item(chapter)

    # Define the book's spine (order of chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define CSS style
    style = 'body { font-family: Times, serif; }'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

    # Add CSS file
    book.add_item(nav_css)

    # Add links
    book.add_item(epub.Link(href="style/nav.css", rel="stylesheet", type="text/css"))

    # Add navigation files
    book.spine = ['nav']

    # Add chapter to the spine
    book.spine.append(chapter)

    # Create EPUB file
    epub.write_epub('output.epub', book, {})

# Example usage
html_content = "<html><body><h1>Hello, World!</h1><p>This is a test.</p></body></html>"
html_to_epub(html_content, 'My EPUB Book')
