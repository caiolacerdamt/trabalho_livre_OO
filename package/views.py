import tkinter as tk
from tkinter import messagebox, ttk
import datetime
from package.controllers import GerenciadorFinanceiro
from package.models import Receita, Despesa, Categoria, Transacao 
from package.persistence import PersistenciaDados

class AppFinanceiro:
    def __init__(self, master):
        self.master = master
        master.title("Sistema de Gestão Financeira Pessoal")
        master.geometry("800x600")

        self.gerenciador = GerenciadorFinanceiro()
        self.persistencia = PersistenciaDados("dados_financeiros.json")

        self._carregar_dados_iniciais()

        self._configurar_ui()
        self._atualizar_saldo()
        self._atualizar_extrato()
        self._preencher_combobox_categorias()


    def _carregar_dados_iniciais(self):
        dados_carregados = self.persistencia.carregar_dados()
        if dados_carregados:
            self.gerenciador.transacoes = dados_carregados.get('transacoes', [])
            self.gerenciador.categorias = dados_carregados.get('categorias', [])
        else:
            if not self.gerenciador.categorias:
                self.gerenciador.adicionar_categoria(Categoria(self.gerenciador.gerar_id_categoria(), "Salário"))
                self.gerenciador.adicionar_categoria(Categoria(self.gerenciador.gerar_id_categoria(), "Alimentação"))
                self.gerenciador.adicionar_categoria(Categoria(self.gerenciador.gerar_id_categoria(), "Transporte"))
                self.gerenciador.adicionar_categoria(Categoria(self.gerenciador.gerar_id_categoria(), "Moradia"))
                self.gerenciador.adicionar_categoria(Categoria(self.gerenciador.gerar_id_categoria(), "Lazer"))
                self._salvar_dados()

    def _salvar_dados(self):
        dados_para_salvar = {
            "transacoes": self.gerenciador.transacoes,
            "categorias": self.gerenciador.categorias
        }
        self.persistencia.salvar_dados(dados_para_salvar)

    def _configurar_ui(self):
        self.frame_saldo = ttk.LabelFrame(self.master, text="Saldo Atual")
        self.frame_saldo.pack(pady=10, padx=10, fill="x")
        self.label_saldo = ttk.Label(self.frame_saldo, text="Carregando saldo...", font=("Arial", 16, "bold"))
        self.label_saldo.pack(pady=5)

        self.frame_transacao = ttk.LabelFrame(self.master, text="Nova Transação")
        self.frame_transacao.pack(pady=10, padx=10, fill="x")

        self.frame_transacao.columnconfigure(0, weight=1)
        self.frame_transacao.columnconfigure(1, weight=3)

        ttk.Label(self.frame_transacao, text="Tipo:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.tipo_transacao = ttk.Combobox(self.frame_transacao, values=["Receita", "Despesa"], state="readonly")
        self.tipo_transacao.set("Despesa")
        self.tipo_transacao.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(self.frame_transacao, text="Valor (R$):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entrada_valor = ttk.Entry(self.frame_transacao)
        self.entrada_valor.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(self.frame_transacao, text="Descrição:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.entrada_descricao = ttk.Entry(self.frame_transacao)
        self.entrada_descricao.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(self.frame_transacao, text="Data (DD/MM/AAAA):").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.entrada_data = ttk.Entry(self.frame_transacao)
        self.entrada_data.insert(0, datetime.date.today().strftime("%d/%m/%Y"))
        self.entrada_data.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(self.frame_transacao, text="Categoria:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.combo_categorias = ttk.Combobox(self.frame_transacao, state="readonly")
        self.combo_categorias.grid(row=4, column=1, sticky="ew", padx=5, pady=2)

        ttk.Button(self.frame_transacao, text="Adicionar Transação", command=self._adicionar_transacao).grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(self.master, text="Gerenciar Categorias", command=self._gerenciar_categorias).pack(pady=5, padx=10, fill="x")

        self.frame_extrato = ttk.LabelFrame(self.master, text="Extrato de Transações")
        self.frame_extrato.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree_extrato = ttk.Treeview(self.frame_extrato, columns=("Tipo", "Valor", "Descrição", "Data", "Categoria", "ID"), show="headings")
        self.tree_extrato.heading("Tipo", text="Tipo")
        self.tree_extrato.heading("Valor", text="Valor")
        self.tree_extrato.heading("Descrição", text="Descrição")
        self.tree_extrato.heading("Data", text="Data")
        self.tree_extrato.heading("Categoria", text="Categoria")
        self.tree_extrato.heading("ID", text="ID", anchor="center") 

        self.tree_extrato.column("Tipo", width=80, anchor="center")
        self.tree_extrato.column("Valor", width=100, anchor="e")
        self.tree_extrato.column("Descrição", width=200, anchor="w")
        self.tree_extrato.column("Data", width=100, anchor="center")
        self.tree_extrato.column("Categoria", width=120, anchor="w")
        self.tree_extrato.column("ID", width=0, stretch=tk.NO) 

        self.tree_extrato.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.tree_extrato, orient="vertical", command=self.tree_extrato.yview)
        self.tree_extrato.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree_extrato.bind("<Double-1>", self._on_double_click_extrato)


    def _preencher_combobox_categorias(self):
        categorias_nomes = [c.nome for c in self.gerenciador.listar_categorias()]
        self.combo_categorias['values'] = categorias_nomes
        if categorias_nomes:
            self.combo_categorias.set(categorias_nomes[0])
        else:
            self.combo_categorias.set("")


    def _adicionar_transacao(self):
        tipo = self.tipo_transacao.get()
        valor_str = self.entrada_valor.get()
        descricao = self.entrada_descricao.get().strip()
        data_str = self.entrada_data.get().strip()
        categoria_nome = self.combo_categorias.get().strip()

        if not valor_str or not descricao or not data_str or not categoria_nome:
            messagebox.showwarning("Campos Obrigatórios", "Todos os campos devem ser preenchidos.")
            return

        try:
            valor = float(valor_str.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro de Valor", "O valor deve ser um número válido.")
            return

        try:
            data = datetime.datetime.strptime(data_str, "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Erro de Data", "Formato de data inválido. Use DD/MM/AAAA.")
            return

        categoria = self.gerenciador.get_categoria_by_nome(categoria_nome)
        if not categoria:
            messagebox.showerror("Erro de Categoria", "Categoria selecionada não encontrada. Adicione-a primeiro.")
            return

        try:
            if tipo == "Receita":
                nova_transacao = Receita(self.gerenciador.gerar_id_transacao(), valor, descricao, data, categoria)
            elif tipo == "Despesa":
                nova_transacao = Despesa(self.gerenciador.gerar_id_transacao(), valor, descricao, data, categoria)
            else:
                messagebox.showerror("Erro", "Tipo de transação inválido.")
                return

            self.gerenciador.adicionar_transacao(nova_transacao)
            self._salvar_dados()
            messagebox.showinfo("Sucesso", f"{tipo} adicionada com sucesso!")
            self._limpar_campos_transacao()
            self._atualizar_saldo()
            self._atualizar_extrato()

        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao adicionar transação: {e}")
        except Exception as e:
            messagebox.showerror("Erro Desconhecido", f"Ocorreu um erro inesperado: {e}")

    def _limpar_campos_transacao(self):
        self.entrada_valor.delete(0, tk.END)
        self.entrada_descricao.delete(0, tk.END)
        self.entrada_data.delete(0, tk.END)
        self.entrada_data.insert(0, datetime.date.today().strftime("%d/%m/%Y"))
        self.combo_categorias.set("")


    def _atualizar_saldo(self):
        saldo = self.gerenciador.get_saldo_atual()
        cor = "green" if saldo >= 0 else "red"
        self.label_saldo.config(text=f"Saldo Atual: R$ {saldo:,.2f}".replace('.', '#').replace(',', '.').replace('#', ','), foreground=cor)


    def _atualizar_extrato(self):
        for item in self.tree_extrato.get_children():
            self.tree_extrato.delete(item)

        extrato = self.gerenciador.get_extrato()
        for transacao in extrato:
            self.tree_extrato.insert("", tk.END, values=(
                transacao.get_tipo(),
                f"R$ {transacao.valor:,.2f}".replace('.', '#').replace(',', '.').replace('#', ','),
                transacao.descricao,
                transacao.data.strftime("%d/%m/%Y"),
                transacao.categoria.nome,
                transacao.id
            ))

    def _on_double_click_extrato(self, event):
        item_id = self.tree_extrato.selection()
        if not item_id:
            return

        values = self.tree_extrato.item(item_id, 'values')
        transacao_id = int(values[5])

        confirm = messagebox.askyesno("Remover Transação",
                                      f"Tem certeza que deseja remover a transação:\n"
                                      f"Descrição: {values[2]}, Valor: {values[1]}, Categoria: {values[4]}?")
        if confirm:
            if self.gerenciador.remover_transacao(transacao_id):
                self._salvar_dados()
                messagebox.showinfo("Sucesso", "Transação removida com sucesso!")
                self._atualizar_saldo()
                self._atualizar_extrato()
            else:
                messagebox.showerror("Erro", "Não foi possível remover a transação.")

    def _gerenciar_categorias(self):
        top = tk.Toplevel(self.master)
        top.title("Gerenciar Categorias")
        top.transient(self.master)
        top.grab_set()

        frame_cat = ttk.LabelFrame(top, text="Categorias Existentes")
        frame_cat.pack(pady=10, padx=10, fill="both", expand=True)

        tree_categorias = ttk.Treeview(frame_cat, columns=("ID", "Nome"), show="headings")
        tree_categorias.heading("ID", text="ID")
        tree_categorias.heading("Nome", text="Nome")
        tree_categorias.column("ID", width=50, anchor="center")
        tree_categorias.column("Nome", width=200, anchor="w")
        tree_categorias.pack(fill="both", expand=True)

        def _carregar_lista_categorias():
            for item in tree_categorias.get_children():
                tree_categorias.delete(item)
            for cat in self.gerenciador.listar_categorias():
                tree_categorias.insert("", tk.END, values=(cat.id, cat.nome))

        _carregar_lista_categorias()

        frame_add_cat = ttk.LabelFrame(top, text="Adicionar Nova Categoria")
        frame_add_cat.pack(pady=10, padx=10, fill="x")

        ttk.Label(frame_add_cat, text="Nome da Categoria:").pack(side=tk.LEFT, padx=5, pady=2)
        entrada_nova_cat = ttk.Entry(frame_add_cat)
        entrada_nova_cat.pack(side=tk.LEFT, expand=True, fill="x", padx=5, pady=2)

        def _adicionar_categoria_dialog():
            nome = entrada_nova_cat.get().strip()
            if nome:
                nova_cat = Categoria(self.gerenciador.gerar_id_categoria(), nome)
                if self.gerenciador.adicionar_categoria(nova_cat):
                    self._salvar_dados()
                    messagebox.showinfo("Sucesso", f"Categoria '{nome}' adicionada.")
                    _carregar_lista_categorias()
                    self._preencher_combobox_categorias()
                    entrada_nova_cat.delete(0, tk.END)
                else:
                    messagebox.showwarning("Aviso", f"A categoria '{nome}' já existe.")
            else:
                messagebox.showwarning("Aviso", "O nome da categoria não pode ser vazio.")

        ttk.Button(frame_add_cat, text="Adicionar", command=_adicionar_categoria_dialog).pack(side=tk.LEFT, padx=5)

        def _on_double_click_cat(event):
            item_id = tree_categorias.selection()
            if not item_id:
                return
            values = tree_categorias.item(item_id, 'values')
            cat_id = int(values[0])
            cat_nome = values[1]

            transacoes_associadas = [t for t in self.gerenciador.transacoes if t.categoria.id == cat_id]
            if transacoes_associadas:
                messagebox.showerror("Erro", f"Não é possível remover a categoria '{cat_nome}' porque há {len(transacoes_associadas)} transações associadas a ela.")
                return

            confirm = messagebox.askyesno("Remover Categoria", f"Tem certeza que deseja remover a categoria '{cat_nome}'?")
            if confirm:
                self.gerenciador.categorias = [c for c in self.gerenciador.categorias if c.id != cat_id]
                self._salvar_dados()
                messagebox.showinfo("Sucesso", f"Categoria '{cat_nome}' removida.")
                _carregar_lista_categorias()
                self._preencher_combobox_categorias()

        tree_categorias.bind("<Double-1>", _on_double_click_cat)