from bs4 import BeautifulSoup
import re
import chardet

def add_headers(html_content):
    """
    Adiciona tags de cabeçalho ao HTML com base em padrões de texto.

    :param html_content: Conteúdo HTML em formato de string.
    :return: HTML com tags de cabeçalho adicionadas.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Padrões de texto que indicam títulos e subtítulos
    patterns = {
        'h1': re.compile(r'^\s*LIVRO\s+[IVXLCDM]+.*$', re.IGNORECASE),
        'h2': re.compile(r'^\s*TÍTULO\s+[IVXLCDM]+.*$', re.IGNORECASE),
        'h3': re.compile(r'^\s*CAPÍTULO\s+[IVXLCDM]+.*$', re.IGNORECASE),
        'h4': re.compile(r'^\s*SEÇÃO\s+[IVXLCDM]+.*$', re.IGNORECASE),
        'h5': re.compile(r'^\s*SUBSEÇÃO\s+[IVXLCDM]+.*$', re.IGNORECASE)
    }

    # Iterar sobre todos os parágrafos e adicionar tags de cabeçalho
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        for tag, pattern in patterns.items():
            if pattern.match(text):
                new_tag = soup.new_tag(tag)
                new_tag.string = text
                p.replace_with(new_tag)
                break

    return str(soup)

def extract_content(html_content):
    """
    Extrai o conteúdo principal de um HTML, removendo elementos indesejados e ajustando o estilo do texto.

    :param html_content: Conteúdo HTML em formato de string.
    :return: Conteúdo principal extraído e índice.
    """
    # Adicionar tags de cabeçalho
    html_content = add_headers(html_content)

    soup = BeautifulSoup(html_content, 'html.parser')

    # Remover elementos indesejados (exemplo: scripts, estilos, cabeçalhos, rodapés, imagens, iframes, vídeos, áudios)
    for elem in soup(['script', 'style', 'header', 'footer', 'img', 'iframe', 'video', 'audio']):
        elem.decompose()

    # Garantir que todo o texto seja na cor preta e ajustar o alinhamento
    for tag in soup.find_all(True):
        if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5']:
            if 'style' in tag.attrs:
                tag.attrs['style'] += "; color: black; text-align: center;"
            else:
                tag.attrs['style'] = "color: black; text-align: center;"
        else:
            if 'style' in tag.attrs:
                tag.attrs['style'] += "; color: black; text-align: justify;"
            else:
                tag.attrs['style'] = "color: black; text-align: justify;"

    # Adicionar IDs únicos aos elementos de cabeçalho e criar o índice
    index = []
    header_count = 0
    for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5']):
        header_count += 1
        header_id = f'header-{header_count}'
        header['id'] = header_id
        index.append(f'<li><a href="#{header_id}">{header.get_text()}</a></li>')

    # Criar a estrutura do índice
    index_html = '<ul>' + ''.join(index) + '</ul>'

    # Extrair o conteúdo principal (pode ser ajustado conforme necessário)
    content = soup.find('body')

    return index_html + str(content)