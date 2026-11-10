# CENTRAL DE ACESSOS
# Comece a leitura por aqui. Este arquivo tem todas as telas do programa.
#
#   tela_entrada         usuário e senha
#   tela_meus_acessos    portais liberados para o setor da pessoa
#   janela_detalhes      descrição do portal e botão "Abrir portal"
#   tela_administracao   portais, setores e funcionários (só o administrador)

import os
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox, ttk

import acessos
import cadastro

# ---------- Cores e fontes ----------
VERMELHO = "#C8102E"  # provisório: trocar pelo vermelho oficial da Portonave
VERMELHO_ESCURO = "#A00C24"
VERMELHO_CLARO = "#FBECEE"
BRANCO = "#FFFFFF"
CINZA = "#F2F2F2"
LINHA = "#E3E3E3"
TEXTO = "#1F2328"
TEXTO_SUAVE = "#5C6066"

FONTE = ("Segoe UI", 13)
FONTE_NEGRITO = ("Segoe UI", 13, "bold")
FONTE_PEQUENA = ("Segoe UI", 11)
FONTE_TITULO = ("Segoe UI", 24, "bold")
FONTE_SUBTITULO = ("Segoe UI", 18, "bold")
FONTE_PORTAL = ("Segoe UI", 15, "bold")

ICONE_PADRAO = "imagens/portal_padrao.png"
COLUNAS = 3  # quantos portais aparecem em cada linha

# Faz o programa achar dados.json e a pasta imagens mesmo se for aberto de outro lugar.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

dados = cadastro.carregar()
usuario_logado = None
imagens_na_tela = []  # o Tkinter apaga imagens que não ficam guardadas numa lista


# =====================================================================
# PEÇAS QUE SE REPETEM
# =====================================================================

def texto(pai, conteudo, fonte=FONTE, cor=TEXTO):
    return tk.Label(pai, text=conteudo, font=fonte, fg=cor, bg=BRANCO, justify="left")


def botao_vermelho(pai, conteudo, comando):
    return tk.Button(pai, text=conteudo, command=comando, font=FONTE_NEGRITO,
                     bg=VERMELHO, fg=BRANCO, activebackground=VERMELHO_ESCURO,
                     activeforeground=BRANCO, relief="flat", padx=22, pady=8, cursor="hand2",
                     highlightthickness=0)


def botao_cinza(pai, conteudo, comando):
    return tk.Button(pai, text=conteudo, command=comando, font=FONTE,
                     bg=CINZA, fg=TEXTO, activebackground=LINHA,
                     relief="flat", padx=18, pady=8, cursor="hand2", highlightthickness=0)


def botao_link(pai, conteudo, comando, fonte=FONTE, cor=TEXTO):
    return tk.Button(pai, text=conteudo, command=comando, font=fonte,
                     bg=BRANCO, fg=cor, activebackground=BRANCO, activeforeground=cor,
                     relief="flat", bd=0, padx=0, pady=0, cursor="hand2",
                     anchor="w", justify="left", highlightthickness=0)


def campo(pai, valor="", esconder=False):
    caixa = tk.Entry(pai, font=FONTE, width=40, fg=TEXTO, bg=BRANCO, relief="flat",
                     highlightthickness=1, highlightbackground="#949494",
                     highlightcolor=VERMELHO)
    if esconder:
        caixa.config(show="•")
    caixa.insert(0, valor)
    return caixa


def campo_com_titulo(pai, titulo, valor="", esconder=False):
    texto(pai, titulo, FONTE_NEGRITO).pack(anchor="w")
    caixa = campo(pai, valor, esconder)
    caixa.pack(fill="x", ipady=6, pady=(4, 14))
    return caixa


def criar_lista(pai):
    lista = tk.Listbox(pai, font=FONTE, fg=TEXTO, bg=BRANCO, relief="flat",
                       highlightthickness=1, highlightbackground=LINHA, highlightcolor=LINHA,
                       selectbackground=VERMELHO_CLARO, selectforeground=TEXTO,
                       activestyle="none")
    lista.pack(fill="both", expand=True, pady=(20, 0))
    return lista


def item_selecionado(lista):
    selecao = lista.curselection()
    if len(selecao) == 0:
        messagebox.showinfo("Central de Acessos", "Primeiro clique em um item da lista.")
        return None
    return selecao[0]


def carregar_icone(portal):
    caminho = portal["imagem"]
    if caminho == "" or not os.path.exists(caminho):
        caminho = ICONE_PADRAO
    imagem = tk.PhotoImage(file=caminho)

    # Imagens grandes são reduzidas até ficarem com no máximo 72 pixels.
    reducao = 1
    while imagem.width() / reducao > 72 or imagem.height() / reducao > 72:
        reducao = reducao + 1
    imagem = imagem.subsample(reducao)

    imagens_na_tela.append(imagem)
    return imagem


def aviso(janela_pequena, mensagem):
    messagebox.showwarning("Confira o formulário", mensagem, parent=janela_pequena)


def abrir_janela_pequena(titulo):
    janela_pequena = tk.Toplevel(janela)
    janela_pequena.title(titulo)
    janela_pequena.configure(bg=BRANCO)
    janela_pequena.resizable(False, False)
    janela_pequena.transient(janela)
    return janela_pequena


def centralizar(janela_pequena):
    # Coloca a janela no meio da tela e bloqueia a janela principal até ela fechar.
    janela_pequena.update_idletasks()
    x = (janela_pequena.winfo_screenwidth() - janela_pequena.winfo_width()) // 2
    y = (janela_pequena.winfo_screenheight() - janela_pequena.winfo_height()) // 3
    janela_pequena.geometry(f"+{x}+{y}")
    janela_pequena.wait_visibility()
    janela_pequena.grab_set()


def limpar_tela():
    for parte in janela.winfo_children():
        parte.destroy()
    imagens_na_tela.clear()


def montar_topo(pagina):
    # Topo de todas as páginas: nome, menu, pessoa logada e "Sair".
    limpar_tela()
    tk.Frame(janela, bg=VERMELHO, height=4).pack(fill="x")

    barra = tk.Frame(janela, bg=BRANCO)
    barra.pack(fill="x", padx=48)
    texto(barra, "Central de Acessos", ("Segoe UI", 15, "bold")).pack(side="left", padx=(0, 48))
    item_do_menu(barra, "Meus acessos", tela_meus_acessos, pagina == "meus acessos")
    if usuario_logado["admin"]:
        item_do_menu(barra, "Administração", tela_administracao, pagina == "administracao")
    botao_link(barra, "Sair", tela_entrada, cor=VERMELHO).pack(side="right")
    texto(barra, usuario_logado["nome"], cor=TEXTO_SUAVE).pack(side="right", padx=(0, 24))

    tk.Frame(janela, bg=LINHA, height=1).pack(fill="x")
    area = tk.Frame(janela, bg=BRANCO)
    area.pack(fill="both", expand=True, padx=48, pady=(36, 24))
    return area


def item_do_menu(pai, nome, comando, selecionado):
    # O item selecionado fica vermelho e com uma linha vermelha embaixo.
    if selecionado:
        cor = VERMELHO
        cor_da_linha = VERMELHO
    else:
        cor = TEXTO
        cor_da_linha = BRANCO
    caixa = tk.Frame(pai, bg=BRANCO)
    caixa.pack(side="left", padx=(0, 32))
    botao_link(caixa, nome, comando, FONTE_NEGRITO, cor).pack(pady=(16, 12))
    tk.Frame(caixa, bg=cor_da_linha, height=3).pack(fill="x")


# =====================================================================
# 1. ENTRADA
# =====================================================================

def tela_entrada():
    global usuario_logado
    usuario_logado = None
    limpar_tela()
    tk.Frame(janela, bg=VERMELHO, height=4).pack(fill="x")

    caixa = tk.Frame(janela, bg=BRANCO)
    caixa.place(relx=0.5, rely=0.42, anchor="center")
    texto(caixa, "Central de Acessos", FONTE_TITULO).pack(anchor="w")
    texto(caixa, "Entre para ver os sistemas liberados para o seu setor.",
          cor=TEXTO_SUAVE).pack(anchor="w", pady=(6, 28))

    campo_usuario = campo_com_titulo(caixa, "Usuário")
    campo_senha = campo_com_titulo(caixa, "Senha", esconder=True)
    mensagem = texto(caixa, "", FONTE_PEQUENA, VERMELHO)
    mensagem.pack(anchor="w", pady=(0, 10))

    def tentar_entrar():
        entrar(campo_usuario.get(), campo_senha.get(), mensagem)

    botao_vermelho(caixa, "Entrar", tentar_entrar).pack(fill="x")
    campo_senha.bind("<Return>", lambda evento: tentar_entrar())
    campo_usuario.focus_set()


def entrar(usuario_digitado, senha_digitada, mensagem):
    global usuario_logado
    usuario_digitado = usuario_digitado.strip().lower()
    for usuario in dados["usuarios"]:
        if usuario["usuario"] == usuario_digitado and usuario["senha"] == senha_digitada:
            usuario_logado = usuario
            tela_meus_acessos()
            return
    mensagem.config(text="Usuário ou senha incorretos.")


# =====================================================================
# 2. MEUS ACESSOS
# =====================================================================

def tela_meus_acessos():
    area = montar_topo("meus acessos")
    texto(area, "Meus acessos", FONTE_TITULO).pack(anchor="w")
    if usuario_logado["admin"]:
        texto(area, "Como administrador, você vê todos os portais cadastrados.",
              cor=TEXTO_SUAVE).pack(anchor="w", pady=(4, 0))

    # A regra que decide o que cada pessoa vê está em acessos.py.
    portais = acessos.portais_do_usuario(usuario_logado, dados["portais"])

    if len(portais) == 0:
        texto(area, "Ainda não há portais liberados para o seu setor.",
              FONTE_NEGRITO).pack(anchor="w", pady=(32, 4))
        texto(area, "Peça ao administrador da Central para liberar o sistema de que você precisa.",
              cor=TEXTO_SUAVE).pack(anchor="w")
        return

    grade = tk.Frame(area, bg=BRANCO)
    grade.pack(anchor="w", pady=(32, 0))
    for coluna in range(COLUNAS):
        grade.columnconfigure(coluna, minsize=300)

    numero = 0
    for portal in portais:
        linha = numero // COLUNAS
        coluna = numero % COLUNAS
        mostrar_portal(grade, portal, linha, coluna)
        numero = numero + 1


def mostrar_portal(grade, portal, linha, coluna):
    # Cada portal mostra só: imagem, nome e "Detalhes".
    item = tk.Frame(grade, bg=BRANCO)
    item.grid(row=linha, column=coluna, sticky="nw", pady=(0, 40))

    imagem = carregar_icone(portal)
    tk.Button(item, image=imagem, command=lambda: abrir_portal(portal),
              relief="flat", bd=0, bg=BRANCO, activebackground=BRANCO,
              cursor="hand2", highlightthickness=0).grid(row=0, column=0, rowspan=2, sticky="n", padx=(0, 16))

    nome = botao_link(item, portal["nome"], lambda: abrir_portal(portal), FONTE_PORTAL)
    nome.config(wraplength=200)
    nome.grid(row=0, column=1, sticky="w")
    # O nome fica vermelho quando o mouse passa por cima, como um link.
    nome.bind("<Enter>", lambda evento: nome.config(fg=VERMELHO))
    nome.bind("<Leave>", lambda evento: nome.config(fg=TEXTO))

    botao_link(item, "Detalhes", lambda: janela_detalhes(portal),
               FONTE, VERMELHO).grid(row=1, column=1, sticky="w", pady=(4, 0))


def abrir_portal(portal):
    # Igual a clicar num link: o navegador abre o endereço original,
    # e o sistema de destino pede o próprio login.
    webbrowser.open(portal["endereco"])


def janela_detalhes(portal):
    detalhes = abrir_janela_pequena(portal["nome"])
    corpo = tk.Frame(detalhes, bg=BRANCO, padx=32, pady=28)
    corpo.pack()

    titulo = texto(corpo, portal["nome"], FONTE_SUBTITULO)
    titulo.config(wraplength=440)
    titulo.pack(anchor="w")
    descricao = texto(corpo, portal["descricao"])
    descricao.config(wraplength=440)
    descricao.pack(anchor="w", pady=(16, 8))
    texto(corpo, portal["endereco"], FONTE_PEQUENA, TEXTO_SUAVE).pack(anchor="w")

    def abrir_e_fechar():
        abrir_portal(portal)
        detalhes.destroy()

    botoes = tk.Frame(corpo, bg=BRANCO)
    botoes.pack(fill="x", pady=(28, 0))
    botao_vermelho(botoes, "Abrir portal", abrir_e_fechar).pack(side="right")
    botao_cinza(botoes, "Fechar", detalhes.destroy).pack(side="right", padx=(0, 12))
    centralizar(detalhes)


# =====================================================================
# 3. ADMINISTRAÇÃO
# =====================================================================

def tela_administracao(aba="Portais"):
    area = montar_topo("administracao")
    texto(area, "Administração", FONTE_TITULO).pack(anchor="w")

    abas = tk.Frame(area, bg=BRANCO)
    abas.pack(anchor="w", pady=(8, 0))
    item_do_menu(abas, "Portais", lambda: tela_administracao("Portais"), aba == "Portais")
    item_do_menu(abas, "Setores", lambda: tela_administracao("Setores"), aba == "Setores")
    item_do_menu(abas, "Funcionários", lambda: tela_administracao("Funcionários"),
                 aba == "Funcionários")
    tk.Frame(area, bg=LINHA, height=1).pack(fill="x")

    corpo = tk.Frame(area, bg=BRANCO)
    corpo.pack(fill="both", expand=True, pady=(24, 0))
    if aba == "Portais":
        aba_portais(corpo)
    elif aba == "Setores":
        aba_setores(corpo)
    else:
        aba_funcionarios(corpo)


# ---------- Portais ----------

def aba_portais(corpo):
    botoes = tk.Frame(corpo, bg=BRANCO)
    botoes.pack(anchor="w")
    botao_vermelho(botoes, "Novo portal", lambda: janela_portal(None)).pack(side="left")
    botao_cinza(botoes, "Editar", lambda: editar_portal(lista)).pack(side="left", padx=12)
    botao_cinza(botoes, "Remover", lambda: remover_portal(lista)).pack(side="left")

    lista = criar_lista(corpo)
    for portal in dados["portais"]:
        setores = ", ".join(portal["setores"])
        lista.insert("end", f"  {portal['nome']}     ·     {setores}")


def editar_portal(lista):
    numero = item_selecionado(lista)
    if numero is not None:
        janela_portal(numero)


def remover_portal(lista):
    numero = item_selecionado(lista)
    if numero is None:
        return
    nome = dados["portais"][numero]["nome"]
    if messagebox.askyesno("Remover portal",
                           f"Remover “{nome}”?\nEle deixa de aparecer para todos os setores."):
        dados["portais"].pop(numero)
        cadastro.salvar(dados)
        tela_administracao("Portais")


def janela_portal(numero):
    # numero = None quer dizer portal novo. Senão, é a posição do portal na lista.
    if numero is None:
        portal = {"nome": "", "endereco": "https://", "descricao": "",
                  "imagem": "", "setores": []}
        titulo = "Novo portal"
    else:
        portal = dados["portais"][numero]
        titulo = "Editar portal"

    formulario = abrir_janela_pequena(titulo)
    corpo = tk.Frame(formulario, bg=BRANCO, padx=32, pady=24)
    corpo.pack()
    texto(corpo, titulo, FONTE_SUBTITULO).pack(anchor="w", pady=(0, 16))

    campo_nome = campo_com_titulo(corpo, "Nome", portal["nome"])
    campo_endereco = campo_com_titulo(corpo, "Endereço (começa com http:// ou https://)",
                                      portal["endereco"])
    campo_descricao = campo_com_titulo(corpo, "O que o sistema faz (uma frase)",
                                       portal["descricao"])
    campo_imagem = campo_com_titulo(corpo, "Imagem PNG (vazio = ícone padrão)", portal["imagem"])
    botao_cinza(corpo, "Escolher imagem…",
                lambda: escolher_imagem(campo_imagem, formulario)).pack(anchor="w")

    texto(corpo, "Setores que veem este portal", FONTE_NEGRITO).pack(anchor="w", pady=(18, 4))
    marcados = {}
    for setor in dados["setores"]:
        marcado = tk.BooleanVar(value=setor in portal["setores"])
        tk.Checkbutton(corpo, text=setor, variable=marcado, font=FONTE, fg=TEXTO,
                       bg=BRANCO, activebackground=BRANCO, highlightthickness=0,
                       bd=0, pady=3).pack(anchor="w")
        marcados[setor] = marcado

    def salvar():
        salvar_portal(numero, campo_nome.get(), campo_endereco.get(), campo_descricao.get(),
                      campo_imagem.get(), marcados, formulario)

    botoes = tk.Frame(corpo, bg=BRANCO)
    botoes.pack(fill="x", pady=(24, 0))
    botao_vermelho(botoes, "Salvar portal", salvar).pack(side="right")
    botao_cinza(botoes, "Cancelar", formulario.destroy).pack(side="right", padx=(0, 12))
    centralizar(formulario)
    campo_nome.focus_set()


def escolher_imagem(campo_imagem, formulario):
    caminho = filedialog.askopenfilename(parent=formulario, title="Escolha a imagem do portal",
                                         filetypes=[("Imagem PNG", "*.png"), ("Imagem GIF", "*.gif")])
    if caminho != "":
        campo_imagem.delete(0, "end")
        campo_imagem.insert(0, caminho)


def imagem_valida(caminho):
    try:
        tk.PhotoImage(file=caminho)
        return True
    except tk.TclError:
        return False


def salvar_portal(numero, nome, endereco, descricao, imagem, marcados, formulario):
    nome = nome.strip()
    endereco = endereco.strip()
    descricao = descricao.strip()
    imagem = imagem.strip()

    setores = []
    for setor in marcados:
        if marcados[setor].get():
            setores.append(setor)

    # Conferências antes de salvar
    if nome == "":
        aviso(formulario, "Informe o nome do portal.")
        return
    comeca_certo = endereco.startswith("http://") or endereco.startswith("https://")
    if not comeca_certo or endereco == "http://" or endereco == "https://":
        aviso(formulario, "Use o endereço completo, começando com http:// ou https://.")
        return
    if descricao == "":
        aviso(formulario, "Escreva uma frase sobre o que o sistema faz.")
        return
    if imagem != "" and not imagem_valida(imagem):
        aviso(formulario, "Não consegui abrir a imagem. Use um arquivo PNG ou GIF.")
        return
    if len(setores) == 0:
        aviso(formulario, "Marque pelo menos um setor.")
        return

    portal = {"nome": nome, "endereco": endereco, "descricao": descricao,
              "imagem": imagem, "setores": setores}
    if numero is None:
        dados["portais"].append(portal)
    else:
        dados["portais"][numero] = portal
    cadastro.salvar(dados)
    formulario.destroy()
    tela_administracao("Portais")


# ---------- Setores ----------

def aba_setores(corpo):
    linha = tk.Frame(corpo, bg=BRANCO)
    linha.pack(anchor="w")
    campo_setor = campo(linha)
    campo_setor.config(width=28)
    campo_setor.pack(side="left", ipady=6, padx=(0, 12))
    botao_vermelho(linha, "Adicionar setor",
                   lambda: adicionar_setor(campo_setor.get())).pack(side="left")
    botao_cinza(linha, "Remover setor", lambda: remover_setor(lista)).pack(side="left", padx=12)

    lista = criar_lista(corpo)
    for setor in dados["setores"]:
        lista.insert("end", f"  {setor}")


def adicionar_setor(nome):
    nome = nome.strip()
    if nome == "":
        messagebox.showinfo("Central de Acessos", "Digite o nome do setor ao lado do botão.")
        return
    if nome in dados["setores"]:
        messagebox.showinfo("Central de Acessos", f"O setor “{nome}” já existe.")
        return
    dados["setores"].append(nome)
    cadastro.salvar(dados)
    tela_administracao("Setores")


def remover_setor(lista):
    numero = item_selecionado(lista)
    if numero is None:
        return
    setor = dados["setores"][numero]

    for usuario in dados["usuarios"]:
        if usuario["setor"] == setor:
            messagebox.showinfo("Central de Acessos",
                                f"Ainda há funcionários em “{setor}”.\n"
                                "Mude o setor deles na aba Funcionários antes de remover.")
            return

    if messagebox.askyesno("Remover setor",
                           f"Remover “{setor}”?\nOs portais deixam de ser liberados para ele."):
        dados["setores"].remove(setor)
        for portal in dados["portais"]:
            if setor in portal["setores"]:
                portal["setores"].remove(setor)
        cadastro.salvar(dados)
        tela_administracao("Setores")


# ---------- Funcionários ----------

def aba_funcionarios(corpo):
    botoes = tk.Frame(corpo, bg=BRANCO)
    botoes.pack(anchor="w")
    botao_vermelho(botoes, "Novo funcionário", lambda: janela_funcionario(None)).pack(side="left")
    botao_cinza(botoes, "Editar", lambda: editar_funcionario(lista)).pack(side="left", padx=12)
    botao_cinza(botoes, "Remover", lambda: remover_funcionario(lista)).pack(side="left")

    lista = criar_lista(corpo)
    for usuario in dados["usuarios"]:
        if usuario["admin"]:
            setor = "Administrador"
        else:
            setor = usuario["setor"]
        lista.insert("end", f"  {usuario['nome']}     ·     {setor}     ·     usuário: {usuario['usuario']}")


def editar_funcionario(lista):
    numero = item_selecionado(lista)
    if numero is not None:
        janela_funcionario(numero)


def remover_funcionario(lista):
    numero = item_selecionado(lista)
    if numero is None:
        return
    usuario = dados["usuarios"][numero]
    if usuario["admin"]:
        messagebox.showinfo("Central de Acessos", "A conta de administrador não pode ser removida.")
        return
    if messagebox.askyesno("Remover funcionário", f"Remover “{usuario['nome']}”?"):
        dados["usuarios"].pop(numero)
        cadastro.salvar(dados)
        tela_administracao("Funcionários")


def janela_funcionario(numero):
    if numero is None:
        usuario = {"usuario": "", "senha": "", "nome": "", "setor": "", "admin": False}
        titulo = "Novo funcionário"
    else:
        usuario = dados["usuarios"][numero]
        titulo = "Editar funcionário"

    formulario = abrir_janela_pequena(titulo)
    corpo = tk.Frame(formulario, bg=BRANCO, padx=32, pady=24)
    corpo.pack()
    texto(corpo, titulo, FONTE_SUBTITULO).pack(anchor="w", pady=(0, 16))

    campo_nome = campo_com_titulo(corpo, "Nome", usuario["nome"])
    campo_usuario = campo_com_titulo(corpo, "Usuário para entrar (sem espaços)", usuario["usuario"])
    campo_senha = campo_com_titulo(corpo, "Senha (pelo menos 6 caracteres)", usuario["senha"],
                                   esconder=True)

    texto(corpo, "Setor", FONTE_NEGRITO).pack(anchor="w")
    if usuario["admin"]:
        escolha_setor = None
        texto(corpo, "Conta de administrador: vê todos os portais.",
              cor=TEXTO_SUAVE).pack(anchor="w", pady=(4, 0))
    else:
        escolha_setor = ttk.Combobox(corpo, values=dados["setores"], state="readonly", font=FONTE)
        escolha_setor.set(usuario["setor"])
        escolha_setor.pack(fill="x", ipady=4, pady=(4, 0))

    def salvar():
        if escolha_setor is None:
            setor = ""
        else:
            setor = escolha_setor.get()
        salvar_funcionario(numero, campo_nome.get(), campo_usuario.get(), campo_senha.get(),
                           setor, usuario["admin"], formulario)

    botoes = tk.Frame(corpo, bg=BRANCO)
    botoes.pack(fill="x", pady=(28, 0))
    botao_vermelho(botoes, "Salvar funcionário", salvar).pack(side="right")
    botao_cinza(botoes, "Cancelar", formulario.destroy).pack(side="right", padx=(0, 12))
    centralizar(formulario)
    campo_nome.focus_set()


def salvar_funcionario(numero, nome, login, senha, setor, admin, formulario):
    nome = nome.strip()
    login = login.strip().lower()

    # Conferências antes de salvar
    if nome == "":
        aviso(formulario, "Informe o nome do funcionário.")
        return
    if login == "" or " " in login:
        aviso(formulario, "Informe um usuário sem espaços, por exemplo: maria.silva")
        return
    for posicao in range(len(dados["usuarios"])):
        if dados["usuarios"][posicao]["usuario"] == login and posicao != numero:
            aviso(formulario, "Este usuário já está em uso.")
            return
    if len(senha) < 6:
        aviso(formulario, "A senha precisa ter pelo menos 6 caracteres.")
        return
    if not admin and setor == "":
        aviso(formulario, "Escolha o setor do funcionário.")
        return

    usuario = {"usuario": login, "senha": senha, "nome": nome, "setor": setor, "admin": admin}
    if numero is None:
        dados["usuarios"].append(usuario)
    else:
        dados["usuarios"][numero] = usuario
    cadastro.salvar(dados)
    formulario.destroy()
    tela_administracao("Funcionários")


# =====================================================================
# INÍCIO DO PROGRAMA
# =====================================================================

if __name__ == "__main__":
    janela = tk.Tk()
    janela.title("Central de Acessos")
    janela.configure(bg=BRANCO)
    janela.minsize(1000, 640)
    try:
        janela.state("zoomed")  # abre maximizada no Windows
    except tk.TclError:
        janela.attributes("-zoomed", True)  # no Linux, onde testamos, o comando é outro
    tela_entrada()
    janela.mainloop()
