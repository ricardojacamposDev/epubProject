from bs4 import BeautifulSoup

def extract_content(html_content):
    """
    Extrai o conteúdo principal de um HTML, removendo elementos indesejados.

    :param html_content: Conteúdo HTML em formato de string.
    :return: Conteúdo principal extraído.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remover elementos indesejados (exemplo: scripts, estilos, cabeçalhos, rodapés)
    for elem in soup(['script', 'style', 'header', 'footer']):
        elem.decompose()

    # Extrair o conteúdo principal (pode ser ajustado conforme necessário)
    content = soup.find('body')

    return str(content)
