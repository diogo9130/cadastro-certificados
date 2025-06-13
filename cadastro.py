import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk

def entrada_variaveis():
    nome = entrada_nome.get().strip().title()
    tipo = entrada_tipo.get().strip().upper()
    numero = entrada_numero.get().strip()

    return nome, tipo, numero

def validacao(nome, tipo, numero):
    if not nome or not tipo or not numero:
        messagebox.showwarning("Atenção", "Insira informações em todos os campos")
        return False
    
    if tipo not in ["MFC", "CHB"]:
        messagebox.showerror("Erro", "Tipo não aceito")
        return False
    
    return True

def salvamento(nome, tipo, numero):
    tree.insert("", tk.END, values=(nome, tipo, numero))

def salvamento_bem_sucedido():
    messagebox.showinfo("Sucesso", "Certificado cadastrado com sucesso")
    return

def limpar_campos():
    entrada_nome.delete(0, tk.END)
    entrada_tipo.delete(0, tk.END)
    entrada_numero.delete(0, tk.END)

def cadastro():
    nome, tipo, numero = entrada_variaveis()
    if validacao(nome, tipo, numero):
        salvamento(nome, tipo, numero)
        salvamento_bem_sucedido()
        limpar_campos()
        verificar_estado_botoes()

def item_selecionado():
    selecionado = tree.selection()

    return selecionado

def validacao_selecao(selecionado):
    if not selecionado:
        messagebox.showerror("Erro", "Nehum item selecionado.")
        return False
    
    return True
    
def apagar_selecionado(selecionado):
    tree.delete(selecionado[0])

def mensagem_itens_apagados_sucesso():
    messagebox.showinfo("Sucesso", "Certificado(s) apagado(s) com sucesso.")

def mensagem_item_atualizado_sucesso():
    messagebox.showinfo("Sucesso", "Certificado atualizado com sucesso.")

def mensagem_itens_exportados_sucesso():
    messagebox.showinfo("Sucesso", "Certificados exportados com sucesso.")

def decisao_apagar_todos():
    decisao = messagebox.askyesno("Confirmar", "Tem certeza que deseja apagar todos os certificados?")

    return decisao

def botao_apagar_tudo():
    if decisao_apagar_todos():
        for item in tree.get_children():
            tree.delete(item)
        mensagem_itens_apagados_sucesso()
        verificar_estado_botoes()

def decisao_apagar_selecionado():
    decisao = messagebox.askyesno("Confirmar", "Tem certeza que deseja apagar o certificado selecionado?")

    return decisao

def botao_apagar_selecionado():
    selecionado = item_selecionado()
    if validacao_selecao(selecionado):
        if decisao_apagar_selecionado():
            apagar_selecionado(selecionado)
            mensagem_itens_apagados_sucesso()
            verificar_estado_botoes()

def decisao_atualizar_certificado():
    decisao = messagebox.askyesno("Confirmar", "Tem certeza que deseja atualizar o certificado selecionado?")

    return decisao

def botao_atualizar_certificado():
    selecionado = item_selecionado()
    if validacao_selecao(selecionado):
        if decisao_atualizar_certificado():
            nome, tipo, numero = entrada_variaveis()
            if validacao(nome, tipo, numero):
                tree.item(selecionado, values=(nome, tipo, numero))
                mensagem_item_atualizado_sucesso()
                limpar_campos()
                verificar_estado_botoes()

def botao_exportar_csv():
    with open("cadastro.csv", "w", encoding="utf-8") as arquivo:
        for item in tree.get_children():
            nome, tipo, numero = tree.item(item, "values")
            arquivo.write(f'{nome},{tipo},{numero}\n')
        mensagem_itens_exportados_sucesso()

def ordenar_coluna(treeview, coluna, reverso):
    lista = [(treeview.set(k, coluna), k) for k in treeview.get_children('')]
    lista.sort(reverse=reverso)

    for index, (val, k) in enumerate(lista):
        treeview.move(k, '', index)

    treeview.heading(coluna, command=lambda: ordenar_coluna(treeview, coluna, not reverso))

def verificar_estado_botoes():
    if tree.get_children():
        bt_apagar.config(state="normal")
        bt_apagar_selecionado.config(state="normal")
        bt_atualizar_certificado.config(state="normal")
        bt_exportar_csv.config(state="normal")
    else:
        bt_apagar.config(state="disabled")
        bt_apagar_selecionado.config(state="disabled")
        bt_atualizar_certificado.config(state="disabled")
        bt_exportar_csv.config(state="disabled")

root = ThemedTk(theme="equilux")
root.title("Cadastro de certificados")
root.geometry("800x800")
root.configure(bg="#3C3F41")

frame_conteudo_principal = ttk.Frame(root, padding=10)
frame_conteudo_principal.pack(pady=20)

frame = ttk.Frame(frame_conteudo_principal, padding=20)
frame.pack(side="left", padx=5)

ttk.Label(frame, text="Material", font=("Segoe UI", 12)).pack(anchor="w", pady=5)
entrada_nome = ttk.Entry(frame, width=35)
entrada_nome.pack(pady=5)

ttk.Label(frame, text="Tipo (MFC ou CHB)", font=("Segoe UI", 12)).pack(anchor="w", pady=5)
entrada_tipo = ttk.Entry(frame, width=35)
entrada_tipo.pack(pady=5)

ttk.Label(frame, text="Número certificado", font=("Segoe UI", 12)).pack(anchor="w", pady=5)
entrada_numero = ttk.Entry(frame, width=35)
entrada_numero.pack(pady=5)

frame_botao = ttk.Frame(frame)
frame_botao.pack(pady=20)

ttk.Button(frame_botao, text="Cadastrar", width=10, command=cadastro).pack(side="left", padx=5)

frame_treeview = ttk.Frame(root, padding=15)
frame_treeview.pack(pady=10)

tree = ttk.Treeview(frame_treeview, columns=("Nome", "Tipo", "Número"), show="headings", height=12)
tree.heading("Nome", text="Nome", command=lambda: ordenar_coluna(tree, "Nome", False))
tree.heading("Tipo", text="Tipo", command=lambda: ordenar_coluna(tree, "Tipo", False))
tree.heading("Número", text="Número do Certificado", command=lambda: ordenar_coluna(tree, "Número", False))
tree.column("Nome", width=150)
tree.column("Tipo", width=150)
tree.column("Número", width=150)
tree.pack(padx=5)

frame_botao_2 = ttk.Frame(frame_treeview)
frame_botao_2.pack(pady=(10, 0))

bt_apagar = ttk.Button(frame_botao_2, text="Apagar tudo", width=15, command=botao_apagar_tudo, state="disabled")
bt_apagar.pack(side="left", padx=2)
bt_apagar_selecionado = ttk.Button(frame_botao_2, text="Apagar selecionado", width=18, command=botao_apagar_selecionado, state="disabled")
bt_apagar_selecionado.pack(side="left", padx=2)
bt_atualizar_certificado = ttk.Button(frame_botao_2, text="Atualizar certificado", width=18, command=botao_atualizar_certificado, state="disabled")
bt_atualizar_certificado.pack(side="left", padx=2)
bt_exportar_csv = ttk.Button(frame_botao_2, text="Exportar csv", width=18, command=botao_exportar_csv, state="disabled")
bt_exportar_csv.pack(side="left", padx=2)

root.mainloop()



