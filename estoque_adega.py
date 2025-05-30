import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from tkinter import ttk
import sqlite3
import shutil
import os
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

# --- Banco de dados ---
conn = sqlite3.connect("estoque.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS bebidas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo TEXT,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    imagem TEXT
)
""")
conn.commit()

# --- Funções ---
def adicionar_bebida():
    nome = entry_nome.get().strip()
    tipo = entry_tipo.get().strip()
    quantidade = entry_quantidade.get().strip()
    preco = entry_preco.get().strip()
    imagem_path = imagem_path_var.get()

    if not nome or not quantidade or not preco:
        messagebox.showwarning("Campos obrigatórios", "Preencha nome, quantidade e preço.")
        return

    try:
        qtd_int = int(quantidade)
        preco_float = float(preco)
    except:
        messagebox.showwarning("Erro", "Quantidade deve ser inteiro e preço decimal.")
        return

    try:
        imagem_destino = None
        if imagem_path:
            pasta_imagens = "imagens"
            if not os.path.exists(pasta_imagens):
                os.makedirs(pasta_imagens)
            nome_arquivo = os.path.basename(imagem_path)
            imagem_destino = os.path.join(pasta_imagens, nome_arquivo)

            caminho_origem = os.path.abspath(imagem_path)
            caminho_destino = os.path.abspath(imagem_destino)

            if caminho_origem != caminho_destino:
                shutil.copyfile(caminho_origem, caminho_destino)

        cursor.execute("INSERT INTO bebidas (nome, tipo, quantidade, preco, imagem) VALUES (?, ?, ?, ?, ?)",
                       (nome, tipo, qtd_int, preco_float, imagem_destino))
        conn.commit()
        limpar_form()
        listar_bebidas()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def limpar_form():
    entry_nome.delete(0, tk.END)
    entry_tipo.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    imagem_path_var.set("")
    label_imagem_preview.config(image='')

def listar_bebidas():
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("SELECT * FROM bebidas")
    for bebida in cursor.fetchall():
        tree.insert("", tk.END, iid=bebida[0], values=(bebida[1], bebida[2], bebida[3], f"R$ {bebida[4]:.2f}"))

def remover_bebida():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione uma bebida para remover.")
        return
    id_bebida = selecionado[0]
    cursor.execute("DELETE FROM bebidas WHERE id = ?", (id_bebida,))
    conn.commit()
    listar_bebidas()

def atualizar_quantidade():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione uma bebida para atualizar.")
        return
    id_bebida = selecionado[0]
    nova_qtd = simpledialog.askinteger("Atualizar Quantidade", "Digite a nova quantidade:")
    if nova_qtd is not None:
        cursor.execute("UPDATE bebidas SET quantidade = ? WHERE id = ?", (nova_qtd, id_bebida))
        conn.commit()
        listar_bebidas()

def selecionar_imagem():
    caminho = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Imagens", "*.jpg;*.jpeg;*.png;*.gif")]
    )
    if caminho:
        imagem_path_var.set(caminho)
        carregar_imagem_preview(caminho)

def carregar_imagem_preview(caminho):
    try:
        img = Image.open(caminho)
        img.thumbnail((100, 100))
        img_tk = ImageTk.PhotoImage(img)
        label_imagem_preview.image = img_tk
        label_imagem_preview.config(image=img_tk)
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def exibir_imagem_detalhe(event):
    selecionado = tree.selection()
    if not selecionado:
        return
    id_bebida = selecionado[0]
    cursor.execute("SELECT imagem FROM bebidas WHERE id = ?", (id_bebida,))
    resultado = cursor.fetchone()
    if resultado and resultado[0] and os.path.exists(resultado[0]):
        try:
            img = Image.open(resultado[0])
            img.thumbnail((300, 300))
            img_tk = ImageTk.PhotoImage(img)

            popup = tk.Toplevel(root)
            popup.title("Visualização da Imagem")
            popup.configure(bg="#2e2e2e")
            popup.resizable(False, False)

            label = tk.Label(popup, image=img_tk, bg="#2e2e2e")
            label.image = img_tk
            label.pack(padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir imagem: {e}")

def gerar_pdf():
    cursor.execute("SELECT * FROM bebidas")
    bebidas = cursor.fetchall()

    if not bebidas:
        messagebox.showinfo("Sem dados", "Não há bebidas para gerar relatório.")
        return

    pasta_relatorios = "relatorios"
    if not os.path.exists(pasta_relatorios):
        os.makedirs(pasta_relatorios)

    caminho_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        initialdir=pasta_relatorios,
        filetypes=[("PDF files", "*.pdf")],
        title="Salvar relatório como"
    )
    if not caminho_pdf:
        return

    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, y, "Relatório de Estoque da Adega")
    y -= 40

    for bebida in bebidas:
        c.setFont("Helvetica", 12)
        texto = f"ID: {bebida[0]} | Nome: {bebida[1]} | Tipo: {bebida[2]} | Qtd: {bebida[3]} | Preço: R$ {bebida[4]:.2f}"
        c.drawString(50, y, texto)
        y -= 20

        if bebida[5] and os.path.exists(bebida[5]):
            try:
                img = Image.open(bebida[5])
                img.thumbnail((100, 100))
                img_io = ImageReader(img)
                c.drawImage(img_io, 400, y - 20, width=60, height=60)
            except:
                pass

        y -= 80
        if y < 150:
            c.showPage()
            y = height - 50

    c.save()
    messagebox.showinfo("PDF criado", f"Relatório salvo em: {caminho_pdf}")

# --- Interface ---
root = tk.Tk()
root.title("Estoque da Adega 🍇")
root.geometry("950x600")
root.configure(bg="#2e2e2e")  # Modo escuro

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#3c3c3c", foreground="white", fieldbackground="#3c3c3c")
style.map("Treeview", background=[("selected", "#555")])

frame_form = tk.Frame(root, bg="#1e1e1e", padx=10, pady=10)
frame_form.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Formulário
entry_nome = tk.Entry(frame_form, width=30)
entry_tipo = tk.Entry(frame_form, width=30)
entry_quantidade = tk.Entry(frame_form, width=30)
entry_preco = tk.Entry(frame_form, width=30)

imagem_path_var = tk.StringVar()

tk.Label(frame_form, text="Nome:", bg="#1e1e1e", fg="white").grid(row=0, column=0, sticky="w")
entry_nome.grid(row=0, column=1)

tk.Label(frame_form, text="Tipo:", bg="#1e1e1e", fg="white").grid(row=1, column=0, sticky="w")
entry_tipo.grid(row=1, column=1)

tk.Label(frame_form, text="Quantidade:", bg="#1e1e1e", fg="white").grid(row=2, column=0, sticky="w")
entry_quantidade.grid(row=2, column=1)

tk.Label(frame_form, text="Preço:", bg="#1e1e1e", fg="white").grid(row=3, column=0, sticky="w")
entry_preco.grid(row=3, column=1)

btn_img = tk.Button(frame_form, text="Selecionar Imagem", command=selecionar_imagem, bg="#444", fg="white")
btn_img.grid(row=4, column=0, pady=5)

label_imagem_preview = tk.Label(frame_form, bg="#1e1e1e")
label_imagem_preview.grid(row=4, column=1)

btn_add = tk.Button(root, text="Adicionar Bebida", command=adicionar_bebida, bg="#007acc", fg="white", font=("Helvetica", 12))
btn_add.pack(pady=5)

frame_lista = tk.Frame(root)
frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

cols = ("Nome", "Tipo", "Quantidade", "Preço")
tree = ttk.Treeview(frame_lista, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tree.bind("<ButtonRelease-1>", exibir_imagem_detalhe)

scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)

frame_botoes = tk.Frame(root, bg="#2e2e2e")
frame_botoes.pack(pady=10)

btn_atualizar = tk.Button(frame_botoes, text="Atualizar Qtd", command=atualizar_quantidade, bg="#ff9800", fg="white")
btn_atualizar.grid(row=0, column=0, padx=10)

btn_remover = tk.Button(frame_botoes, text="Remover", command=remover_bebida, bg="#f44336", fg="white")
btn_remover.grid(row=0, column=1, padx=10)

btn_pdf = tk.Button(frame_botoes, text="Gerar PDF", command=gerar_pdf, bg="#607d8b", fg="white")
btn_pdf.grid(row=0, column=2, padx=10)

listar_bebidas()
root.mainloop()
