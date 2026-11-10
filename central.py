# CENTRAL DE ACESSOS
# Comece a leitura por aqui. Cada tela do programa é uma função:
#
#   tela_entrada         usuário e senha
#   tela_meus_acessos    as capas dos portais liberados para o setor
#   tela_detalhes        prints, descrição e o botão "Abrir portal"
#   tela_administracao   portais, setores e funcionários (só o admin)

import os
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox, ttk

import acessos
import cadastro

VERMELHO = "#C8102E"  # trocar pelo vermelho oficial da Portonave, se tiverem
VERMELHO_CLARO = "#FBECEE"
BRANCO = "#FFFFFF"
CINZA = "#F2F2F2"
LINHA = "#E3E3E3"
PRETO = "#1F2328"
CINZA_TEXTO = "#5C6066"

FONTE = ("Segoe UI", 13)
NEGRITO = ("Segoe UI", 13, "bold")
PEQUENA = ("Segoe UI", 11)
TITULO = ("Segoe UI", 24, "bold")

# Tudo em 16:9. Uma imagem de 1280 x 720 encaixa certinho em todos os tamanhos.
CAPA_LARGURA = 256
CAPA_ALTURA = 144
FAIXA = 40  # altura da faixa "Ver detalhes"

# Faz o programa achar o dados.json e a pasta imagens.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

dados = cadastro.carregar()
usuario_logado = None
fotos = []  # o Tkinter apaga da tela as imagens que não estão guardadas numa lista


# ---------------------------------------------------------------------
# Peças que se repetem nas telas
# ---------------------------------------------------------------------

def texto(pai, conteudo, fonte=FONTE, cor=PRETO):
    return tk.Label(pai, text=conteudo, font=fonte, fg=cor, bg=BRANCO, justify="left")


def botao_vermelho(pai, conteudo, comando):
    return tk.Button(pai, text=conteudo, command=comando, font=NEGRITO, bg=VERMELHO, fg=BRANCO,
                     activebackground="#A00C24", activeforeground=BRANCO,
                     relief="flat", padx=22, pady=8, cursor="hand2", highlightthickness=0)


def botao_cinza(pai, conteudo, comando):
    return tk.Button(pai, text=conteudo, command=comando, font=FONTE, bg=CINZA, fg=PRETO,
                     activebackground=LINHA, relief="flat", padx=18, pady=8,
                     cursor="hand2", highlightthickness=0)


def botao_link(pai, conteudo, comando, fonte=FONTE, cor=PRETO):
    return tk.Button(pai, text=conteudo, command=comando, font=fonte, bg=BRANCO, fg=cor,
                     activebackground=BRANCO, activeforeground=cor, relief="flat", bd=0,
                     padx=0, pady=0, cursor="hand2", anchor="w", justify="left",
                     highlightthickness=0)


def campo(pai, titulo, valor="", senha=False):
    texto(pai, titulo, NEGRITO).pack(anchor="w")
    caixa = tk.Entry(pai, font=FONTE, width=36, fg=PRETO, relief="flat",
                     highlightthickness=1, highlightbackground="#949494", highlightcolor=VERMELHO)
    if senha:
        caixa.config(show="•")
    caixa.insert(0, valor)
    caixa.pack(fill="x", ipady=6, pady=(4, 14))
    return caixa


def lista(pai, linhas):
    caixa = tk.Listbox(pai, font=FONTE, fg=PRETO, relief="flat", height=6,
                       highlightthickness=1, highlightbackground=LINHA,
                       selectbackground=VERMELHO_CLARO, selectforeground=PRETO, activestyle="none")
    for linha in linhas:
        caixa.insert("end", linha)
    caixa.pack(fill="both", expand=True, pady=(16, 0))
    return caixa


def escolhido(caixa):
    # Devolve a posição do item clicado na lista, ou None se nada foi clicado.
    if len(caixa.curselection()) == 0:
        messagebox.showinfo("Central de Acessos", "Primeiro clique em um item da lista.")
        return None
    return caixa.curselection()[0]


def foto(caminho, largura, altura):
    # Sem imagem, aparece o ícone padrão no meio.
    if caminho == "" or not os.path.exists(caminho):
        imagem = tk.PhotoImage(file="imagens/portal_padrao.png")
        fotos.append(imagem)
        return imagem

    imagem = tk.PhotoImage(file=caminho)
    # O Tkinter só diminui imagens dividindo o tamanho por um número inteiro.
    # Vamos aumentando o divisor até a imagem caber no espaço.
    divisor = 1
    while imagem.width() / divisor > largura or imagem.height() / divisor > altura:
        divisor = divisor + 1
    imagem = imagem.subsample(divisor)
    fotos.append(imagem)
    return imagem


def quadro(pai, caminho, largura, altura):
    # Um retângulo com a imagem dentro. Usado nas capas e nos prints.
    tela = tk.Canvas(pai, width=largura, height=altura, bg=VERMELHO_CLARO,
                     highlightthickness=0, cursor="hand2")
    tela.create_image(largura // 2, altura // 2, image=foto(caminho, largura, altura))
    return tela


def escolher_imagem():
    caminho = filedialog.askopenfilename(title="Escolha uma imagem",
                                         filetypes=[("Imagem PNG", "*.png"), ("Imagem GIF", "*.gif")])
    if caminho == "":
        return ""
    try:
        tk.PhotoImage(file=caminho)
    except tk.TclError:
        messagebox.showwarning("Central de Acessos", "Não consegui abrir essa imagem. Use PNG ou GIF.")
        return ""
    return cadastro.copiar_imagem(caminho)


def limpar_tela():
    for parte in janela.winfo_children():
        parte.destroy()
    fotos.clear()


def montar_topo(pagina):
    limpar_tela()
    tk.Frame(janela, bg=VERMELHO, height=4).pack(fill="x")
    barra = tk.Frame(janela, bg=BRANCO)
    barra.pack(fill="x", padx=48)

    texto(barra, "Central de Acessos", ("Segoe UI", 15, "bold")).pack(side="left", padx=(0, 48))
    item_do_menu(barra, "Meus acessos", tela_meus_acessos, pagina == "acessos")
    if usuario_logado["admin"]:
        item_do_menu(barra, "Administração", tela_administracao, pagina == "admin")
    botao_link(barra, "Sair", tela_entrada, cor=VERMELHO).pack(side="right")
    texto(barra, usuario_logado["nome"], cor=CINZA_TEXTO).pack(side="right", padx=(0, 24))

    tk.Frame(janela, bg=LINHA, height=1).pack(fill="x")
    area = tk.Frame(janela, bg=BRANCO)
    area.pack(fill="both", expand=True, padx=48, pady=(32, 24))
    return area


def item_do_menu(pai, nome, comando, selecionado):
    caixa = tk.Frame(pai, bg=BRANCO)
    caixa.pack(side="left", padx=(0, 32))
    # O item selecionado fica vermelho e com uma linha vermelha embaixo.
    if selecionado:
        botao_link(caixa, nome, comando, NEGRITO, VERMELHO).pack(pady=(16, 12))
        tk.Frame(caixa, bg=VERMELHO, height=3).pack(fill="x")
    else:
        botao_link(caixa, nome, comando, NEGRITO).pack(pady=(16, 12))
        tk.Frame(caixa, bg=BRANCO, height=3).pack(fill="x")


# ---------------------------------------------------------------------
# 1. ENTRADA
# ---------------------------------------------------------------------

def tela_entrada():
    global usuario_logado
    usuario_logado = None
    limpar_tela()
    tk.Frame(janela, bg=VERMELHO, height=4).pack(fill="x")

    caixa = tk.Frame(janela, bg=BRANCO)
    caixa.place(relx=0.5, rely=0.42, anchor="center")
    texto(caixa, "Central de Acessos", TITULO).pack(anchor="w")
    texto(caixa, "Entre para ver os sistemas do seu setor.",
          cor=CINZA_TEXTO).pack(anchor="w", pady=(6, 28))
    campo_usuario = campo(caixa, "Usuário")
    campo_senha = campo(caixa, "Senha", senha=True)
    erro = texto(caixa, "", PEQUENA, VERMELHO)
    erro.pack(anchor="w", pady=(0, 10))

    def entrar():
        global usuario_logado
        for usuario in dados["usuarios"]:
            if usuario["usuario"] == campo_usuario.get().strip().lower() and usuario["senha"] == campo_senha.get():
                usuario_logado = usuario
                tela_meus_acessos()
                return
        erro.config(text="Usuário ou senha incorretos.")

    botao_vermelho(caixa, "Entrar", entrar).pack(fill="x")
    campo_senha.bind("<Return>", lambda evento: entrar())
    campo_usuario.focus_set()


# ---------------------------------------------------------------------
# 2. MEUS ACESSOS
# ---------------------------------------------------------------------

def tela_meus_acessos():
    area = montar_topo("acessos")
    texto(area, "Meus acessos", TITULO).pack(anchor="w")

    # A regra que decide quem vê o quê está no arquivo acessos.py
    portais = acessos.portais_do_usuario(usuario_logado, dados["portais"])
    if len(portais) == 0:
        texto(area, "Ainda não há sistemas liberados para o seu setor.",
              NEGRITO).pack(anchor="w", pady=(28, 4))
        texto(area, "Peça ao administrador da Central para liberar o que você precisa.",
              cor=CINZA_TEXTO).pack(anchor="w")
        return

    # Quantas capas cabem lado a lado na largura da janela
    colunas = (janela.winfo_width() - 96) // (CAPA_LARGURA + 24)
    if colunas < 1:
        colunas = 1

    grade = tk.Frame(area, bg=BRANCO)
    grade.pack(anchor="w", pady=(24, 0))
    numero = 0
    for portal in portais:
        cartao(grade, portal, numero // colunas, numero % colunas)
        numero = numero + 1


def cartao(grade, portal, linha, coluna):
    caixa = tk.Frame(grade, bg=BRANCO)
    caixa.grid(row=linha, column=coluna, sticky="nw", padx=(0, 24), pady=(0, 28))

    capa = quadro(caixa, portal["capa"], CAPA_LARGURA, CAPA_ALTURA)
    capa.pack()
    nome = botao_link(caixa, portal["nome"], lambda: abrir_portal(portal), ("Segoe UI", 14, "bold"))
    nome.config(wraplength=CAPA_LARGURA)
    nome.pack(anchor="w", pady=(10, 0))

    # Com o mouse em cima, aparece a faixa "Ver detalhes" na parte de baixo da capa.
    def mouse_entrou(evento):
        capa.create_rectangle(0, CAPA_ALTURA - FAIXA, CAPA_LARGURA, CAPA_ALTURA,
                              fill=VERMELHO, width=0, tags="faixa")
        capa.create_text(CAPA_LARGURA // 2, CAPA_ALTURA - FAIXA // 2, text="Ver detalhes",
                         fill=BRANCO, font=NEGRITO, tags="faixa")
        nome.config(fg=VERMELHO)

    def mouse_saiu(evento):
        capa.delete("faixa")
        nome.config(fg=PRETO)

    def clicou(evento):
        if evento.y > CAPA_ALTURA - FAIXA:
            tela_detalhes(portal)  # clicou na faixa
        else:
            abrir_portal(portal)  # clicou na imagem

    capa.bind("<Enter>", mouse_entrou)
    capa.bind("<Leave>", mouse_saiu)
    capa.bind("<Button-1>", clicou)


def abrir_portal(portal):
    # Igual a clicar num link: abre o endereço no navegador.
    # O login quem pede é o próprio sistema.
    webbrowser.open(portal["endereco"])


# ---------------------------------------------------------------------
# 3. DETALHES (como a página de um jogo na Steam)
# ---------------------------------------------------------------------

def tela_detalhes(portal, print_aberto=0):
    area = montar_topo("acessos")
    botao_link(area, "‹  Voltar para Meus acessos", tela_meus_acessos, cor=VERMELHO).pack(anchor="w")
    texto(area, portal["nome"], TITULO).pack(anchor="w", pady=(8, 12))

    esquerda = tk.Frame(area, bg=BRANCO)
    esquerda.pack(side="left", anchor="n")
    direita = tk.Frame(area, bg=BRANCO)
    direita.pack(side="left", anchor="n", fill="x", expand=True, padx=(32, 0))

    # Print grande. Em tela grande ele fica maior.
    if janela.winfo_width() > 1700:
        largura = 1280
        altura = 720
    else:
        largura = 640
        altura = 360

    prints = portal["prints"]
    if len(prints) > 0:
        quadro(esquerda, prints[print_aberto], largura, altura).pack()
    else:
        quadro(esquerda, portal["capa"], largura, altura).pack()
        texto(esquerda, "Ainda não há prints deste sistema.",
              cor=CINZA_TEXTO).pack(anchor="w", pady=(10, 0))

    # Miniaturas: clicar numa delas troca o print grande.
    miniaturas = tk.Frame(esquerda, bg=BRANCO)
    miniaturas.pack(anchor="w", pady=(10, 0))
    for numero in range(len(prints)):
        miniatura(miniaturas, portal, numero, numero == print_aberto)

    # Coluna da direita
    quadro(direita, portal["capa"], CAPA_LARGURA, CAPA_ALTURA).pack(anchor="w")
    descricao = texto(direita, portal["descricao"])
    descricao.config(wraplength=CAPA_LARGURA)
    descricao.pack(anchor="w", pady=(16, 16))
    texto(direita, "Endereço", PEQUENA, CINZA_TEXTO).pack(anchor="w")
    endereco = texto(direita, portal["endereco"], PEQUENA)
    endereco.config(wraplength=CAPA_LARGURA)
    endereco.pack(anchor="w")
    botao_vermelho(direita, "Abrir portal", lambda: abrir_portal(portal)).pack(anchor="w", pady=(24, 0))


def miniatura(pai, portal, numero, aberto):
    mini = quadro(pai, portal["prints"][numero], 128, 72)
    if aberto:
        mini.config(highlightthickness=3, highlightbackground=VERMELHO)
    else:
        mini.config(highlightthickness=3, highlightbackground=BRANCO)
    mini.bind("<Button-1>", lambda evento: tela_detalhes(portal, numero))
    mini.pack(side="left", padx=(0, 8))


# ---------------------------------------------------------------------
# 4. ADMINISTRAÇÃO
# ---------------------------------------------------------------------

def tela_administracao(aba="Portais"):
    area = montar_topo("admin")
    abas = tk.Frame(area, bg=BRANCO)
    abas.pack(anchor="w")
    item_do_menu(abas, "Portais", lambda: tela_administracao("Portais"), aba == "Portais")
    item_do_menu(abas, "Setores", lambda: tela_administracao("Setores"), aba == "Setores")
    item_do_menu(abas, "Funcionários", lambda: tela_administracao("Funcionários"), aba == "Funcionários")
    tk.Frame(area, bg=LINHA, height=1).pack(fill="x", pady=(0, 24))

    if aba == "Portais":
        aba_portais(area)
    elif aba == "Setores":
        aba_setores(area)
    else:
        aba_funcionarios(area)


# ----- Portais -----

def aba_portais(area):
    botoes = tk.Frame(area, bg=BRANCO)
    botoes.pack(anchor="w")
    linhas = []
    for portal in dados["portais"]:
        linhas.append("  " + portal["nome"] + "     ·     " + ", ".join(portal["setores"]))

    def editar():
        numero = escolhido(caixa)
        if numero is not None:
            tela_portal(numero)

    def remover():
        numero = escolhido(caixa)
        if numero is None:
            return
        nome = dados["portais"][numero]["nome"]
        if messagebox.askyesno("Remover portal", "Remover " + nome + "?\nEle some para todos os setores."):
            dados["portais"].pop(numero)
            cadastro.salvar(dados)
            tela_administracao("Portais")

    botao_vermelho(botoes, "Novo portal", lambda: tela_portal(None)).pack(side="left")
    botao_cinza(botoes, "Editar", editar).pack(side="left", padx=12)
    botao_cinza(botoes, "Remover", remover).pack(side="left")
    caixa = lista(area, linhas)


def tela_portal(numero):
    # numero = None é um portal novo. Senão, é a posição dele na lista.
    if numero is None:
        portal = {"nome": "", "endereco": "https://", "descricao": "",
                  "capa": "", "prints": [], "setores": []}
    else:
        portal = dados["portais"][numero]

    area = montar_topo("admin")
    if numero is None:
        texto(area, "Novo portal", TITULO).pack(anchor="w", pady=(0, 20))
    else:
        texto(area, "Editar portal", TITULO).pack(anchor="w", pady=(0, 20))

    esquerda = tk.Frame(area, bg=BRANCO)
    esquerda.pack(side="left", anchor="n")
    direita = tk.Frame(area, bg=BRANCO)
    direita.pack(side="left", anchor="n", padx=(56, 0))

    # Coluna da esquerda: textos e capa
    campo_nome = campo(esquerda, "Nome", portal["nome"])
    campo_endereco = campo(esquerda, "Endereço (começa com http:// ou https://)", portal["endereco"])
    campo_descricao = campo(esquerda, "O que o sistema faz (uma frase)", portal["descricao"])
    campo_capa = campo(esquerda, "Capa (imagem PNG de 1280 x 720)", portal["capa"])

    def trocar_capa():
        caminho = escolher_imagem()
        if caminho != "":
            campo_capa.delete(0, "end")
            campo_capa.insert(0, caminho)

    botao_cinza(esquerda, "Escolher capa…", trocar_capa).pack(anchor="w")

    # Coluna da direita: setores e prints
    texto(direita, "Setores que veem este portal", NEGRITO).pack(anchor="w")
    marcados = {}
    for setor in dados["setores"]:
        marcado = tk.BooleanVar(value=setor in portal["setores"])
        tk.Checkbutton(direita, text=setor, variable=marcado, font=FONTE, bg=BRANCO,
                       activebackground=BRANCO, highlightthickness=0, bd=0).pack(anchor="w")
        marcados[setor] = marcado

    texto(direita, "Prints do sistema (até 4, PNG de 1280 x 720)", NEGRITO).pack(anchor="w", pady=(18, 0))
    caixa_prints = tk.Listbox(direita, font=PEQUENA, height=4, width=42, relief="flat",
                              highlightthickness=1, highlightbackground="#949494",
                              selectbackground=VERMELHO_CLARO, selectforeground=PRETO)
    for caminho in portal["prints"]:
        caixa_prints.insert("end", caminho)
    caixa_prints.pack(anchor="w", pady=(4, 8))

    def adicionar_print():
        if caixa_prints.size() == 4:
            messagebox.showinfo("Central de Acessos", "Cada portal pode ter até 4 prints.")
            return
        caminho = escolher_imagem()
        if caminho != "":
            caixa_prints.insert("end", caminho)

    def remover_print():
        numero_print = escolhido(caixa_prints)
        if numero_print is not None:
            caixa_prints.delete(numero_print)

    botoes_prints = tk.Frame(direita, bg=BRANCO)
    botoes_prints.pack(anchor="w")
    botao_cinza(botoes_prints, "Adicionar print…", adicionar_print).pack(side="left")
    botao_cinza(botoes_prints, "Remover print", remover_print).pack(side="left", padx=12)

    def salvar():
        endereco = campo_endereco.get().strip()
        setores = []
        for setor in marcados:
            if marcados[setor].get():
                setores.append(setor)

        if campo_nome.get().strip() == "":
            messagebox.showwarning("Falta o nome", "Escreva o nome do portal.")
        elif not (endereco.startswith("http://") or endereco.startswith("https://")) or len(endereco) < 10:
            messagebox.showwarning("Endereço", "Use o endereço completo, começando com http:// ou https://.")
        elif campo_descricao.get().strip() == "":
            messagebox.showwarning("Falta a descrição", "Escreva uma frase sobre o que o sistema faz.")
        elif len(setores) == 0:
            messagebox.showwarning("Faltam os setores", "Marque pelo menos um setor.")
        else:
            novo = {"nome": campo_nome.get().strip(), "endereco": endereco,
                    "descricao": campo_descricao.get().strip(), "capa": campo_capa.get().strip(),
                    "prints": list(caixa_prints.get(0, "end")), "setores": setores}
            if numero is None:
                dados["portais"].append(novo)
            else:
                dados["portais"][numero] = novo
            cadastro.salvar(dados)
            tela_administracao("Portais")

    fim = tk.Frame(direita, bg=BRANCO)
    fim.pack(anchor="w", pady=(32, 0))
    botao_vermelho(fim, "Salvar portal", salvar).pack(side="left")
    botao_cinza(fim, "Cancelar", lambda: tela_administracao("Portais")).pack(side="left", padx=12)
    campo_nome.focus_set()


# ----- Setores -----

def aba_setores(area):
    linha = tk.Frame(area, bg=BRANCO)
    linha.pack(anchor="w")
    novo_setor = tk.Entry(linha, font=FONTE, width=26, relief="flat", highlightthickness=1,
                          highlightbackground="#949494", highlightcolor=VERMELHO)
    novo_setor.pack(side="left", ipady=7, padx=(0, 12))

    def adicionar():
        nome = novo_setor.get().strip()
        if nome == "":
            messagebox.showinfo("Central de Acessos", "Escreva o nome do setor ao lado do botão.")
        elif nome in dados["setores"]:
            messagebox.showinfo("Central de Acessos", "Esse setor já existe.")
        else:
            dados["setores"].append(nome)
            cadastro.salvar(dados)
            tela_administracao("Setores")

    def remover():
        numero = escolhido(caixa)
        if numero is None:
            return
        setor = dados["setores"][numero]
        for usuario in dados["usuarios"]:
            if usuario["setor"] == setor:
                messagebox.showinfo("Central de Acessos", "Ainda tem funcionários em " + setor +
                                    ".\nMude o setor deles antes de remover.")
                return
        if messagebox.askyesno("Remover setor", "Remover o setor " + setor + "?"):
            dados["setores"].remove(setor)
            for portal in dados["portais"]:
                if setor in portal["setores"]:
                    portal["setores"].remove(setor)
            cadastro.salvar(dados)
            tela_administracao("Setores")

    botao_vermelho(linha, "Adicionar setor", adicionar).pack(side="left")
    botao_cinza(linha, "Remover setor", remover).pack(side="left", padx=12)
    linhas = []
    for setor in dados["setores"]:
        linhas.append("  " + setor)
    caixa = lista(area, linhas)


# ----- Funcionários -----

def aba_funcionarios(area):
    botoes = tk.Frame(area, bg=BRANCO)
    botoes.pack(anchor="w")
    linhas = []
    for usuario in dados["usuarios"]:
        if usuario["admin"]:
            setor = "Administrador"
        else:
            setor = usuario["setor"]
        linhas.append("  " + usuario["nome"] + "     ·     " + setor + "     ·     usuário: " + usuario["usuario"])

    def editar():
        numero = escolhido(caixa)
        if numero is not None:
            tela_funcionario(numero)

    def remover():
        numero = escolhido(caixa)
        if numero is None:
            return
        usuario = dados["usuarios"][numero]
        if usuario["admin"]:
            messagebox.showinfo("Central de Acessos", "A conta do administrador não pode ser removida.")
        elif messagebox.askyesno("Remover funcionário", "Remover " + usuario["nome"] + "?"):
            dados["usuarios"].pop(numero)
            cadastro.salvar(dados)
            tela_administracao("Funcionários")

    botao_vermelho(botoes, "Novo funcionário", lambda: tela_funcionario(None)).pack(side="left")
    botao_cinza(botoes, "Editar", editar).pack(side="left", padx=12)
    botao_cinza(botoes, "Remover", remover).pack(side="left")
    caixa = lista(area, linhas)


def tela_funcionario(numero):
    if numero is None:
        usuario = {"usuario": "", "senha": "", "nome": "", "setor": "", "admin": False}
    else:
        usuario = dados["usuarios"][numero]

    area = montar_topo("admin")
    if numero is None:
        texto(area, "Novo funcionário", TITULO).pack(anchor="w", pady=(0, 20))
    else:
        texto(area, "Editar funcionário", TITULO).pack(anchor="w", pady=(0, 20))

    formulario = tk.Frame(area, bg=BRANCO)
    formulario.pack(anchor="w")
    campo_nome = campo(formulario, "Nome", usuario["nome"])
    campo_usuario = campo(formulario, "Usuário para entrar (sem espaços)", usuario["usuario"])
    campo_senha = campo(formulario, "Senha (pelo menos 6 letras ou números)", usuario["senha"], senha=True)

    texto(formulario, "Setor", NEGRITO).pack(anchor="w")
    escolha = ttk.Combobox(formulario, values=dados["setores"], state="readonly", font=FONTE)
    escolha.set(usuario["setor"])
    if usuario["admin"]:
        texto(formulario, "O administrador não tem setor: ele vê todos os portais.",
              cor=CINZA_TEXTO).pack(anchor="w", pady=(4, 0))
    else:
        escolha.pack(fill="x", ipady=4, pady=(4, 0))

    def salvar():
        login = campo_usuario.get().strip().lower()
        repetido = False
        for posicao in range(len(dados["usuarios"])):
            if dados["usuarios"][posicao]["usuario"] == login and posicao != numero:
                repetido = True

        if campo_nome.get().strip() == "":
            messagebox.showwarning("Falta o nome", "Escreva o nome do funcionário.")
        elif login == "" or " " in login:
            messagebox.showwarning("Usuário", "Escreva um usuário sem espaços, por exemplo: maria.silva")
        elif repetido:
            messagebox.showwarning("Usuário", "Esse usuário já existe.")
        elif len(campo_senha.get()) < 6:
            messagebox.showwarning("Senha", "A senha precisa ter pelo menos 6 caracteres.")
        elif not usuario["admin"] and escolha.get() == "":
            messagebox.showwarning("Falta o setor", "Escolha o setor do funcionário.")
        else:
            novo = {"usuario": login, "senha": campo_senha.get(), "nome": campo_nome.get().strip(),
                    "setor": escolha.get(), "admin": usuario["admin"]}
            if numero is None:
                dados["usuarios"].append(novo)
            else:
                dados["usuarios"][numero] = novo
            cadastro.salvar(dados)
            tela_administracao("Funcionários")

    fim = tk.Frame(formulario, bg=BRANCO)
    fim.pack(anchor="w", pady=(28, 0))
    botao_vermelho(fim, "Salvar funcionário", salvar).pack(side="left")
    botao_cinza(fim, "Cancelar", lambda: tela_administracao("Funcionários")).pack(side="left", padx=12)
    campo_nome.focus_set()


# ---------------------------------------------------------------------
# Início do programa
# ---------------------------------------------------------------------

janela = tk.Tk()
janela.title("Central de Acessos")
janela.configure(bg=BRANCO)
janela.minsize(1000, 640)
try:
    janela.state("zoomed")  # maximizada no Windows
except tk.TclError:
    janela.attributes("-zoomed", True)  # no Linux o comando é outro
tela_entrada()
janela.mainloop()
