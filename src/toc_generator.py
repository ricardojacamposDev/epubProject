from bs4 import BeautifulSoup
import re

def generate_toc(html_content):
    """
    Gera um sumário em formato .toc a partir do conteúdo HTML.

    :param html_content: Conteúdo HTML em formato de string.
    :return: Sumário em formato .toc.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Adicionar IDs únicos aos elementos de cabeçalho e criar o índice
    toc = []
    header_count = 0
    for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5']):
        header_count += 1
        header_id = f'header-{header_count}'
        header['id'] = header_id
        toc.append(f'{header.name.upper()}: {header.get_text()} - #{header_id}')

    # Criar a estrutura do sumário
    toc_content = '\n'.join(toc)

    return toc_content

def save_toc(toc_content, output_path):
    """
    Salva o sumário em formato .toc em um arquivo.

    :param toc_content: Conteúdo do sumário em formato de string.
    :param output_path: Caminho do arquivo de saída.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(toc_content)

# Exemplo de uso
if __name__ == "__main__":
    html_content = "<html><body><h1>LIVRO I</h1><h2>TÍTULO I</h2><h3>CAPÍTULO I</h3><h4>SEÇÃO I</h4><h5>SUBSEÇÃO I</h5></body></html>"
    toc_content = generate_toc(html_content)
    save_toc(toc_content, '/c:/Users/ricar/source/epubProject/output.toc')
