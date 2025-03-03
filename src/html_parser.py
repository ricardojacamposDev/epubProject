from bs4 import BeautifulSoup

def extract_content(html_content):
    """
    Extrai o conteúdo principal de um HTML, removendo elementos indesejados e ajustando o estilo do texto.

    :param html_content: Conteúdo HTML em formato de string.
    :return: Conteúdo principal extraído.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remover elementos indesejados (exemplo: scripts, estilos, cabeçalhos, rodapés, imagens, iframes, vídeos, áudios)
    for elem in soup(['script', 'style', 'header', 'footer', 'img', 'iframe', 'video', 'audio']):
        elem.decompose()

    # Garantir que todo o texto seja na cor preta
    for tag in soup.find_all(True):
        if 'style' in tag.attrs:
            tag.attrs['style'] += "; color: black;"
        else:
            tag.attrs['style'] = "color: black;"

    # Manter as estruturas hierárquicas (exemplo: h1, h2, h3, etc.)
    for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if 'style' in header.attrs:
            header.attrs['style'] += "; color: black;"
        else:
            header.attrs['style'] = "color: black;"

    # Extrair o conteúdo principal (pode ser ajustado conforme necessário)
    content = soup.find('body')

    return str(content)
