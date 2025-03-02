import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz  # PyMuPDF
from html_parser import extract_content
from epub_generator import create_epub

def upload_file():
    # Abrir a caixa de diálogo para selecionar o arquivo
    file_path = filedialog.askopenfilename(
        title="Selecionar Arquivo",
        filetypes=[("Arquivos HTML", "*.html;*.htm"), ("Arquivos PDF", "*.pdf")]
    )
    if file_path:
        if file_path.lower().endswith(('.pdf')):
            # Ler o conteúdo do arquivo PDF
            document = fitz.open(file_path)
            content = ""
            for page_num in range(len(document)):
                page = document.load_page(page_num)
                text = page.get_text("html")  # Obter texto como HTML
                content += text
        else:
            # Ler o conteúdo do arquivo HTML
            with open(file_path, 'r', encoding='utf-8') as file:
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
            # Iniciar a barra de progresso
            progress_bar.start()
            root.update_idletasks()

            # Criar EPUB com metadados
            create_epub_with_metadata(content, 'Livro EPUB Convertido', output_path, numero_lei, ano_lei, tipo_lei)

            # Parar a barra de progresso
            progress_bar.stop()
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

    # Adicionar itens de navegação
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Definir a espinha do livro
    book.spine = ['nav', chapter]

    # Gerar o arquivo EPUB
    epub.write_epub(output_path, book, {})

def main():
    global root, progress_bar, numero_lei_entry, ano_lei_entry, tipo_lei_entry

    # Configurar a janela principal
    root = tk.Tk()
    root.title("Conversor HTML/PDF para EPUB")
    root.geometry("400x350")
    root.resizable(False, False)

    # Estilo
    style = ttk.Style()
    style.configure("TLabel", padding=5, font=('Arial', 12))
    style.configure("TButton", padding=6, relief="flat", font=('Arial', 12), background='#4CAF50', foreground='white')
    style.configure("TEntry", padding=5, font=('Arial', 12))
    style.configure("TProgressbar", thickness=20)

    # Campos de entrada para metadados
    ttk.Label(root, text="Número da Lei:").pack(pady=5)
    numero_lei_entry = ttk.Entry(root, width=30)
    numero_lei_entry.pack(pady=5)

    ttk.Label(root, text="Ano da Lei:").pack(pady=5)
    ano_lei_entry = ttk.Entry(root, width=30)
    ano_lei_entry.pack(pady=5)

    ttk.Label(root, text="Tipo de Lei:").pack(pady=5)
    tipo_lei_entry = ttk.Entry(root, width=30)
    tipo_lei_entry.pack(pady=5)

    # Configurar o botão de upload
    upload_button = ttk.Button(root, text="Carregar Arquivo", command=upload_file)
    upload_button.pack(pady=20)

    # Barra de progresso
    progress_bar = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
    progress_bar.pack(fill="x", padx=20, pady=10)

    # Executar a interface
    root.mainloop()

if __name__ == "__main__":
    main()
