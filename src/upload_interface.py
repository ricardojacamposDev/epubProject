import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz  # PyMuPDF
import pdfplumber
from html_parser import extract_content
from epub_generator import create_epub
import chardet

def upload_file():
    # Abrir a caixa de diálogo para selecionar o arquivo
    file_path = filedialog.askopenfilename(
        title="Selecionar Arquivo",
        filetypes=[("Arquivos HTML", "*.html;*.htm"), ("Arquivos PDF", "*.pdf")]
    )
    if file_path:
        if file_path.lower().endswith(('.pdf')):
            # Ler o conteúdo do arquivo PDF com pdfplumber
            content = '<html><body>'
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        content += f'<p>{text.replace("\n", "<br>")}</p>'
            content += '</body></html>'
        else:
            # Detectar a codificação do arquivo HTML
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']

            # Ler o conteúdo do arquivo HTML com a codificação detectada
            with open(file_path, 'r', encoding=encoding) as file:
                html_content = file.read()
            content = extract_content(html_content)

        # Obter metadados dos campos de entrada
        numero_lei = numero_lei_entry.get()
        ano_lei = ano_lei_entry.get()
        tipo_lei = tipo_lei_entry.get()

        # Definir o caminho do arquivo EPUB de saída
        output_path = filedialog.asksaveasfilename(
            defaultextension=".epub",
            filetypes=[("Arquivos EPUB", "*.epub")]
        )
        if output_path:
            # Criar EPUB com metadados
            create_epub_with_metadata(content, 'Livro EPUB Convertido', output_path, numero_lei, ano_lei, tipo_lei)
            messagebox.showinfo("Sucesso", "Arquivo EPUB criado com sucesso!")

def create_epub_with_metadata(content, title, output_path, numero_lei, ano_lei, tipo_lei):
    from ebooklib import epub

    book = epub.EpubBook()

    # Definir metadados
    book.set_identifier(numero_lei)
    book.set_title(title)
    book.add_author(tipo_lei)
    book.set_language('pt')

    # Adicionar metadados personalizados
    book.add_metadata('DC', 'identifier', numero_lei)
    book.add_metadata('DC', 'date', ano_lei)
    book.add_metadata('DC', 'type', tipo_lei)

    # Criar um capítulo
    chapter = epub.EpubHtml(title='Capítulo 1', file_name='chap_1.xhtml', lang='pt')
    chapter.content = content

    # Adicionar capítulo ao livro
    book.add_item(chapter)
    book.spine = [chapter]

    # Adicionar itens de navegação
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Gerar o arquivo EPUB
    epub.write_epub(output_path, book, {})

def start_conversion():
    # Verificar se todos os campos estão preenchidos
    if not numero_lei_entry.get() or not ano_lei_entry.get() or not tipo_lei_entry.get():
        messagebox.showerror("Erro", "Por favor, preencha todos os campos de metadados.")
        return

    # Chamar a função de upload
    upload_file()

def main():
    global root, numero_lei_entry, ano_lei_entry, tipo_lei_entry

    # Configurar a janela principal
    root = tk.Tk()
    root.title("Conversor HTML/PDF para EPUB")
    root.geometry("600x400")
    root.resizable(True, True)

    # Estilo
    style = ttk.Style()
    style.configure("TLabel", padding=5, font=('Arial', 12))
    style.configure("TButton", padding=6, relief="flat", font=('Arial', 12), background='white', foreground='#007BFF')
    style.configure("TEntry", padding=5, font=('Arial', 12))

    # Frame para campos de entrada
    input_frame = ttk.Frame(root, padding="10")
    input_frame.pack(fill='both', expand=True)

    # Campos de entrada para metadados
    ttk.Label(input_frame, text="Número da Lei:").grid(row=0, column=0, pady=5, sticky='w')
    numero_lei_entry = ttk.Entry(input_frame, width=40)
    numero_lei_entry.grid(row=0, column=1, pady=5)

    ttk.Label(input_frame, text="Ano da Lei:").grid(row=1, column=0, pady=5, sticky='w')
    ano_lei_entry = ttk.Entry(input_frame, width=40)
    ano_lei_entry.grid(row=1, column=1, pady=5)

    ttk.Label(input_frame, text="Tipo de Lei:").grid(row=2, column=0, pady=5, sticky='w')
    tipo_lei_entry = ttk.Entry(input_frame, width=40)
    tipo_lei_entry.grid(row=2, column=1, pady=5)

    # Botão de início
    start_button = ttk.Button(input_frame, text="Iniciar Conversão", command=start_conversion)
    start_button.grid(row=3, column=0, columnspan=2, pady=20)

    # Executar a interface
    root.mainloop()

if __name__ == "__main__":
    main()