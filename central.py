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
VERMELHO = "#FF4560"
VERMELHO_ESCURO = "#DF2947"
VERMELHO_CLARO = "#39202B"
BRANCO = "#0D0F14"  # fundo das páginas e janelas
CINZA = "#181D27"
LINHA = "#2A3242"
TEXTO = "#F4F6FB"
TEXTO_SUAVE = "#AAB5C6"
PAINEL = "#141821"
NAV = "#10131B"
TEXTO_BOTAO = "#100B12"

FONTE = ("Segoe UI", 12)
FONTE_NEGRITO = ("Segoe UI", 12, "bold")
FONTE_PEQUENA = ("Segoe UI", 10)
FONTE_TITULO = ("Segoe UI", 29, "bold")
FONTE_SUBTITULO = ("Segoe UI", 20, "bold")
FONTE_PORTAL = ("Segoe UI", 16, "bold")
FONTE_DESTAQUE = ("Segoe UI", 35, "bold")

ICONE_PADRAO = "imagens/portal_padrao.png"

# Faz o programa achar dados.json e a pasta imagens mesmo se for aberto de outro lugar.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

dados = cadastro.carregar()
usuario_logado = None
imagens_na_tela = []  # o Tkinter apaga imagens que não ficam guardadas numa lista


# =====================================================================
# PEÇAS QUE SE REPETEM
# =====================================================================

def texto(pai, conteudo, fonte=FONTE, cor=TEXTO, fundo=BRANCO, **opcoes):
    return tk.Label(pai, text=conteudo, font=fonte, fg=cor, bg=fundo,
                    justify="left", **opcoes)


def botao(pai, nome, comando, fundo, cor, sobre, fonte=FONTE_NEGRITO, **opcoes):
    item = tk.Button(pai, text=nome, command=comando, font=fonte, bg=fundo, fg=cor,
                     activebackground=sobre, activeforeground=cor, relief="flat", bd=0,
                     highlightthickness=2, highlightbackground=fundo, highlightcolor=VERMELHO,
                     cursor="hand2", **opcoes)
    item.bind("<Enter>", lambda evento: item.config(bg=sobre))
    item.bind("<Leave>", lambda evento: item.config(bg=fundo))
    return item


def botao_vermelho(pai, conteudo, comando):
    return botao(pai, conteudo, comando, VERMELHO, TEXTO_BOTAO, "#FF6D82", padx=19, pady=9)


def botao_cinza(pai, conteudo, comando):
    return botao(pai, conteudo, comando, CINZA, TEXTO, LINHA, padx=15, pady=8)


def botao_link(pai, conteudo, comando, fonte=FONTE, cor=TEXTO, fundo=BRANCO, **opcoes):
    return botao(pai, conteudo, comando, fundo, cor, LINHA, fonte=fonte, **opcoes)


def campo(pai, valor="", esconder=False):
    caixa = tk.Entry(pai, font=FONTE, width=38, fg=TEXTO, bg=CINZA, relief="flat",
                     insertbackground=TEXTO, selectbackground=VERMELHO_CLARO,
                     selectforeground=TEXTO, highlightthickness=1,
                     highlightbackground=LINHA, highlightcolor=VERMELHO)
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
    try:
        imagem = tk.PhotoImage(file=caminho)
    except tk.TclError:
        imagem = tk.PhotoImage(file=ICONE_PADRAO)

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
    if not janela_pequena.winfo_viewable():
        janela_pequena.wait_visibility()
    janela_pequena.grab_set()


def limpar_tela():
    janela.unbind("<MouseWheel>")
    janela.unbind("<Control-f>")
    for parte in janela.winfo_children():
        parte.destroy()
    imagens_na_tela.clear()


def painel_destaque(pai, rotulo, titulo, legenda, altura=164):
    # A malha é desenhada pelo Tkinter e se ajusta ao tamanho da janela.
    painel = tk.Canvas(pai, bg="#151924", height=altura, highlightthickness=0)

    def desenhar(evento):
        painel.delete("all")
        largura, altura_atual = evento.width, evento.height
        centro = int(largura * .83)
        for x in range(max(32, largura // 2), largura, 24):
            painel.create_line(x, 0, x, altura_atual, fill="#202638")
        for y in range(14, altura_atual, 24):
            painel.create_line(largura // 2, y, largura, y, fill="#202638")
        painel.create_polygon(largura * .70, 0, largura, 0, largura, altura_atual,
                              largura * .60, altura_atual, fill="#211A29", stipple="gray50")
        for deslocamento in (0, 16, 32):
            painel.create_line(centro + deslocamento, 0,
                               centro - altura_atual // 2 + deslocamento, altura_atual,
                               fill="#603044", width=1)
        painel.create_rectangle(0, 0, 4, altura_atual, fill=VERMELHO, width=0)
        painel.create_text(24, 22, text=rotulo, anchor="nw",
                           fill="#FF8A9B", font=FONTE_PEQUENA)
        painel.create_text(22, 46, text=titulo, anchor="nw", fill=TEXTO, font=FONTE_DESTAQUE)
        painel.create_text(25, 115, text=legenda, anchor="nw", fill=TEXTO_SUAVE,
                           font=FONTE, width=max(200, largura - 52))

    painel.bind("<Configure>", desenhar)
    return painel


def montar_topo(pagina):
    limpar_tela()
    lateral = tk.Frame(janela, bg=NAV, width=214, highlightbackground=LINHA,
                       highlightthickness=1)
    lateral.pack(side="left", fill="y")
    lateral.pack_propagate(False)

    marca = tk.Frame(lateral, bg=NAV)
    marca.pack(fill="x", padx=19, pady=(26, 27))
    texto(marca, "CENTRAL", ("Segoe UI", 23, "bold"), TEXTO, NAV).pack(anchor="w")
    texto(marca, "ACESSOS DO TERMINAL", FONTE_PEQUENA, VERMELHO, NAV).pack(anchor="w")
    texto(lateral, "NAVEGAÇÃO", FONTE_PEQUENA, TEXTO_SUAVE, NAV).pack(anchor="w", padx=19, pady=(0, 8))

    for rotulo, chave, acao in (
        ("Meus acessos", "meus acessos", tela_meus_acessos),
        ("Administração", "administracao", tela_administracao),
    ):
        if chave == "administracao" and not usuario_logado["admin"]:
            continue
        fundo = VERMELHO_CLARO if pagina == chave else NAV
        cor = "#FF9FAE" if pagina == chave else TEXTO
        botao(lateral, rotulo, acao, fundo, cor, CINZA, anchor="w",
              padx=12, pady=9).pack(fill="x", padx=12, pady=3)

    sessao = tk.Frame(lateral, bg=NAV)
    sessao.pack(side="bottom", fill="x", padx=16, pady=(0, 18))
    tk.Frame(sessao, bg=LINHA, height=1).pack(fill="x", pady=(0, 12))
    texto(sessao, usuario_logado["nome"], FONTE_PEQUENA, TEXTO_SUAVE, NAV,
          wraplength=166).pack(anchor="w")
    botao_link(sessao, "Sair da conta", tela_entrada, cor=TEXTO, fundo=NAV,
               padx=0, pady=7).pack(anchor="w")

    area = tk.Frame(janela, bg=BRANCO)
    area.pack(side="left", fill="both", expand=True, padx=28, pady=24)
    return area


def item_do_menu(pai, nome, comando, selecionado):
    fundo = VERMELHO_CLARO if selecionado else BRANCO
    cor = "#FF9FAE" if selecionado else TEXTO_SUAVE
    botao(pai, nome, comando, fundo, cor, CINZA,
          padx=13, pady=7).pack(side="left", padx=(0, 8))


# =====================================================================
# 1. ENTRADA
# =====================================================================

def tela_entrada():
    global usuario_logado
    usuario_logado = None
    limpar_tela()

    centro = tk.Frame(janela, bg=BRANCO)
    centro.place(relx=.5, rely=.48, relwidth=.84, anchor="center")
    centro.columnconfigure(0, weight=3)
    centro.columnconfigure(1, weight=2)
    painel_destaque(centro, "CENTRAL  /  ACESSOS", "Portais do terminal",
                    "Os sistemas que você usa, reunidos em um catálogo.",
                    altura=360).grid(row=0, column=0, sticky="nsew", padx=(0, 22))

    caixa = tk.Frame(centro, bg=BRANCO, highlightbackground=LINHA,
                    highlightthickness=1, padx=23, pady=23)
    caixa.grid(row=0, column=1, sticky="nsew")
    texto(caixa, "Entrar", FONTE_TITULO).pack(anchor="w")
    texto(caixa, "Use sua conta da Central.", cor=TEXTO_SUAVE).pack(anchor="w", pady=(4, 17))
    campo_usuario = campo_com_titulo(caixa, "Usuário")
    campo_senha = campo_com_titulo(caixa, "Senha", esconder=True)
    mensagem = texto(caixa, "", FONTE_PEQUENA, "#FF9FAE")
    mensagem.pack(anchor="w", pady=(0, 6))

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
    painel_destaque(area, "CATÁLOGO  /  TERMINAL", "Meus acessos",
                    "Abra os portais que você usa no trabalho.").pack(fill="x")

    # O catálogo e a busca partem apenas dos portais liberados para a conta.
    portais = acessos.portais_do_usuario(usuario_logado, dados["portais"])
    barra = tk.Frame(area, bg=BRANCO)
    barra.pack(fill="x", pady=(19, 12))
    resultado = texto(barra, "", FONTE_NEGRITO)
    resultado.pack(side="left")
    busca = tk.StringVar()
    caixa = campo(barra)
    caixa.config(textvariable=busca, width=22)
    caixa.pack(side="right", ipady=5)
    texto(barra, "Buscar portal", FONTE_PEQUENA, TEXTO_SUAVE).pack(side="right", padx=9)

    corpo = tk.Frame(area, bg=BRANCO)
    corpo.pack(fill="both", expand=True)
    tela = tk.Canvas(corpo, bg=BRANCO, highlightthickness=0)
    rolagem = ttk.Scrollbar(corpo, orient="vertical", command=tela.yview)
    tela.configure(yscrollcommand=rolagem.set)
    rolagem.pack(side="right", fill="y")
    tela.pack(side="left", fill="both", expand=True)
    grade = tk.Frame(tela, bg=BRANCO)
    bloco = tela.create_window((0, 0), window=grade, anchor="nw")
    ultimo_estado = None

    def atualizar(evento=None):
        nonlocal ultimo_estado
        largura = tela.winfo_width()
        tela.itemconfigure(bloco, width=largura)
        if largura >= 1000:
            colunas = 3
        elif largura >= 550:
            colunas = 2
        else:
            colunas = 1
        termo = busca.get().strip().casefold()
        estado = (colunas, termo)
        if estado == ultimo_estado:
            return
        ultimo_estado = estado

        for filho in grade.winfo_children():
            filho.destroy()
        imagens_na_tela.clear()
        for coluna in range(3):
            grade.columnconfigure(coluna, weight=1 if coluna < colunas else 0,
                                  uniform="portais" if coluna < colunas else "")
        filtrados = [portal for portal in portais if termo in portal["nome"].casefold()]
        total = len(filtrados)
        resultado.config(text=f"{total:02d} {'portal disponível' if total == 1 else 'portais disponíveis'}")
        tela.yview_moveto(0)

        if not filtrados:
            mensagem = "Nenhum portal encontrado." if termo else "Seu setor ainda não tem portais liberados."
            texto(grade, mensagem, FONTE, TEXTO_SUAVE).grid(row=0, column=0, sticky="w", pady=17)
        for indice, portal in enumerate(filtrados):
            mostrar_portal(grade, portal, indice // colunas, indice % colunas)

    def rolar(evento):
        if evento.delta:
            tela.yview_scroll(-1 if evento.delta > 0 else 1, "units")

    grade.bind("<Configure>", lambda evento: tela.config(scrollregion=tela.bbox("all")))
    tela.bind("<Configure>", atualizar)
    janela.bind("<MouseWheel>", rolar)
    janela.bind("<Control-f>", lambda evento: caixa.focus_set())
    busca.trace_add("write", lambda *args: atualizar())
    caixa.bind("<Escape>", lambda evento: busca.set(""))
    atualizar()


def mostrar_portal(grade, portal, linha, coluna):
    item = tk.Frame(grade, bg=PAINEL, highlightbackground=LINHA, highlightthickness=1)
    item.grid(row=linha, column=coluna, sticky="nsew", padx=(0, 13), pady=(0, 13))
    topo = tk.Frame(item, bg=PAINEL)
    topo.pack(fill="x", padx=14, pady=(14, 8))
    miniatura = botao_link(topo, "", lambda: abrir_portal(portal), fundo=CINZA, padx=7, pady=6)
    miniatura.configure(image=carregar_icone(portal))
    miniatura.pack(side="left")
    texto(topo, "PORTAL", FONTE_PEQUENA, "#FF8A9B", PAINEL).pack(side="right", anchor="n")

    nome = botao_link(item, portal["nome"], lambda: abrir_portal(portal),
                      FONTE_PORTAL, TEXTO, PAINEL, wraplength=205, anchor="w", justify="left")
    nome.pack(fill="x", padx=13, pady=(1, 8))

    tk.Frame(item, bg=LINHA, height=1).pack(fill="x", padx=14)
    acoes = tk.Frame(item, bg=PAINEL)
    acoes.pack(fill="x", padx=14, pady=8)
    botao_link(acoes, "Detalhes", lambda: janela_detalhes(portal), FONTE_PEQUENA,
               TEXTO_SUAVE, PAINEL, padx=4, pady=5).pack(side="left")
    botao_link(acoes, "Abrir  ↗", lambda: abrir_portal(portal), FONTE_PEQUENA,
               "#FF9FAE", VERMELHO_CLARO, padx=10, pady=5).pack(side="right")


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
    texto(corpo, portal["endereco"], FONTE_PEQUENA, TEXTO_SUAVE,
          wraplength=440).pack(anchor="w")

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
    painel_destaque(area, "GESTÃO  /  CENTRAL", "Administração",
                    "Cadastre portais e escolha quem pode vê-los.").pack(fill="x")

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
    janela.geometry("1280x800")
    janela.minsize(1000, 640)
    estilo = ttk.Style(janela)
    estilo.theme_use("clam")
    estilo.configure("TScrollbar", background=CINZA, troughcolor=BRANCO,
                     bordercolor=BRANCO, arrowcolor=TEXTO_SUAVE)
    estilo.configure("TCombobox", fieldbackground=CINZA, foreground=TEXTO,
                     background=CINZA, arrowcolor=TEXTO, bordercolor=LINHA)
    estilo.map("TCombobox", fieldbackground=[("readonly", CINZA)],
               foreground=[("readonly", TEXTO)], selectbackground=[("readonly", CINZA)],
               selectforeground=[("readonly", TEXTO)])
    try:
        janela.state("zoomed")  # abre maximizada no Windows
    except tk.TclError:
        janela.attributes("-zoomed", True)  # no Linux, onde testamos, o comando é outro
    tela_entrada()
    janela.mainloop()
