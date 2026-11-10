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
from tkinter import font as tkfont

from PIL import Image, ImageOps, ImageTk  # Pillow: deixa as imagens do tamanho certo

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

# As capas seguem a proporção 16:9 (a mesma de uma tela de computador).
CAPA_LARGURA = 256
CAPA_ALTURA = 144
FAIXA = 40  # altura da faixa "Ver detalhes"

SEGUNDOS_PARA_CONFERIR = 3  # de quanto em quanto tempo olha se alguém mudou os dados

dados = None
usuario_logado = None
tela_atual = ""   # qual tela está aberta agora
aba_atual = ""    # qual aba da Administração está aberta
ultima_mudanca = 0
fotos = []  # o Tkinter apaga da tela as imagens que não estão guardadas numa lista


# ---------------------------------------------------------------------
# Peças que se repetem nas telas
# ---------------------------------------------------------------------

def texto(pai, conteudo, fonte=FONTE, cor=PRETO):
    return tk.Label(pai, text=conteudo, font=fonte, fg=cor, bg=BRANCO, justify="left")


def botao_redondo(pai, conteudo, comando, fundo, cor, fundo_mouse, largura=0, esquerda=False):
    # O Tkinter não tem botão arredondado, então desenhamos um num Canvas.
    if largura == 0:
        largura = tkfont.Font(font=NEGRITO).measure(conteudo) + 44
    altura = 42
    botao = tk.Canvas(pai, width=largura, height=altura, bg=BRANCO,
                      highlightthickness=0, cursor="hand2")

    # Um retângulo com os cantos repetidos; o smooth=True arredonda esses cantos.
    r = 14
    cantos = [r, 0, largura - r, 0, largura, 0, largura, r,
              largura, altura - r, largura, altura, largura - r, altura,
              r, altura, 0, altura, 0, altura - r, 0, r, 0, 0]
    forma = botao.create_polygon(cantos, smooth=True, fill=fundo)
    if esquerda:
        botao.create_text(18, altura // 2, text=conteudo, fill=cor, font=NEGRITO, anchor="w")
    else:
        botao.create_text(largura // 2, altura // 2, text=conteudo, fill=cor, font=NEGRITO)

    botao.bind("<Button-1>", lambda evento: comando())
    botao.bind("<Enter>", lambda evento: botao.itemconfig(forma, fill=fundo_mouse))
    botao.bind("<Leave>", lambda evento: botao.itemconfig(forma, fill=fundo))
    return botao


def botao_vermelho(pai, conteudo, comando, largura=0):
    return botao_redondo(pai, conteudo, comando, VERMELHO, BRANCO, "#A00C24", largura)


def botao_cinza(pai, conteudo, comando):
    return botao_redondo(pai, conteudo, comando, CINZA, PRETO, LINHA)


def botao_link(pai, conteudo, comando, fonte=FONTE, cor=PRETO):
    return tk.Button(pai, text=conteudo, command=comando, font=fonte, bg=BRANCO, fg=cor,
                     activebackground=BRANCO, activeforeground=cor, relief="flat", bd=0,
                     padx=0, pady=0, cursor="hand2", anchor="w", justify="left",
                     highlightthickness=0)


def campo(pai, titulo, valor="", senha=False):
    texto(pai, titulo, NEGRITO).pack(anchor="w")
    # Fundo cinza-claro no lugar da borda. A borda grossa (bd) faz o espaço
    # interno, e a linha vermelha só aparece quando o campo está em uso.
    caixa = tk.Entry(pai, font=FONTE, width=36, fg=PRETO, bg=CINZA, relief="flat", bd=9,
                     highlightthickness=2, highlightbackground=CINZA, highlightcolor=VERMELHO)
    if senha:
        caixa.config(show="•")
    caixa.insert(0, valor)
    caixa.pack(fill="x", pady=(6, 16))
    return caixa


def tabela(pai):
    # Onde ficam as linhas das listas da Administração.
    caixa = tk.Frame(pai, bg=BRANCO)
    caixa.pack(fill="x", pady=(20, 0))
    caixa.columnconfigure(2, weight=1)
    return caixa


def linha(caixa, numero, nome, detalhe, editar, remover, capa=None):
    # Uma linha da lista: (capa) nome, detalhe em cinza e as ações na direita.
    posicao = numero * 2
    if capa is not None:
        quadro(caixa, capa, 96, 54).grid(row=posicao, column=0, padx=(0, 18), pady=10)
    texto(caixa, nome, NEGRITO).grid(row=posicao, column=1, sticky="w", pady=14)
    texto(caixa, detalhe, cor=CINZA_TEXTO).grid(row=posicao, column=2, sticky="w", padx=(32, 0))
    if editar is not None:
        botao_link(caixa, "Editar", editar).grid(row=posicao, column=3, padx=(0, 28))
    if remover is not None:
        botao_link(caixa, "Remover", remover, cor=VERMELHO).grid(row=posicao, column=4)
    tk.Frame(caixa, bg="#EEEEEE", height=1).grid(row=posicao + 1, column=0, columnspan=5, sticky="we")


def foto(caminho, largura, altura):
    # Devolve a imagem no tamanho exato do espaço, ou None se o portal não tem imagem.
    caminho = cadastro.caminho_da_imagem(caminho)
    if caminho == "" or not os.path.exists(caminho):
        return None

    # O ImageOps.fit (do Pillow) aumenta ou diminui a imagem até preencher
    # todo o espaço. Se sobrar um pouco, corta embaixo, para o topo do
    # sistema (onde ficam o nome e o menu) continuar aparecendo.
    imagem = ImageOps.fit(Image.open(caminho), (largura, altura), centering=(0.5, 0))
    imagem = ImageTk.PhotoImage(imagem)
    fotos.append(imagem)
    return imagem


def quadro(pai, caminho, largura, altura):
    # Um retângulo com a imagem dentro. Usado nas capas e nos prints.
    tela = tk.Canvas(pai, width=largura, height=altura, bg=VERMELHO_CLARO,
                     highlightthickness=0, cursor="hand2")
    imagem = foto(caminho, largura, altura)
    if imagem is None:
        desenhar_portal(tela, largura, altura)
    else:
        tela.create_image(largura // 2, altura // 2, image=imagem)
    return tela


def desenhar_portal(tela, largura, altura):
    # Sem imagem, desenha o símbolo da Central: um portal em arco, no meio.
    meio = largura // 2
    abertura = altura // 4
    cima = altura // 3
    chao = cima + altura * 2 // 5
    espessura = altura // 30
    esquerda = meio - abertura // 2
    direita = meio + abertura // 2
    tela.create_arc(esquerda, cima, direita, cima + abertura, start=0, extent=180,
                    style="arc", outline=VERMELHO, width=espessura)
    tela.create_line(esquerda, cima + abertura // 2, esquerda, chao, fill=VERMELHO, width=espessura)
    tela.create_line(direita, cima + abertura // 2, direita, chao, fill=VERMELHO, width=espessura)
    tela.create_line(esquerda - abertura // 4, chao, direita + abertura // 4, chao,
                     fill=VERMELHO, width=espessura)


def escolher_imagem():
    caminho = filedialog.askopenfilename(title="Escolha uma imagem",
                                         filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif")])
    if caminho == "":
        return ""
    try:
        Image.open(caminho).verify()
    except OSError:
        messagebox.showwarning("Central de Acessos", "Não consegui abrir essa imagem. Use PNG ou JPG.")
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
    # O item aberto fica com fundo vermelho-claro e letra vermelha.
    if selecionado:
        item = botao_redondo(pai, nome, comando, VERMELHO_CLARO, VERMELHO, VERMELHO_CLARO)
    else:
        item = botao_redondo(pai, nome, comando, BRANCO, PRETO, CINZA)
    item.pack(side="left", padx=(0, 8), pady=10)


# ---------------------------------------------------------------------
# 1. ENTRADA
# ---------------------------------------------------------------------

def tela_entrada():
    global usuario_logado, tela_atual
    usuario_logado = None
    tela_atual = "entrada"
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

    caixa.update_idletasks()
    botao_vermelho(caixa, "Entrar", entrar, campo_usuario.winfo_reqwidth()).pack()
    campo_senha.bind("<Return>", lambda evento: entrar())
    campo_usuario.focus_set()


# ---------------------------------------------------------------------
# 2. MEUS ACESSOS
# ---------------------------------------------------------------------

def tela_meus_acessos():
    global tela_atual
    tela_atual = "meus acessos"
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
    global tela_atual
    tela_atual = "detalhes"
    area = montar_topo("acessos")
    botao_link(area, "‹  Voltar para Meus acessos", tela_meus_acessos, cor=VERMELHO).pack(anchor="w")
    texto(area, portal["nome"], TITULO).pack(anchor="w", pady=(8, 16))

    # O print grande ocupa todo o espaço que sobra ao lado da coluna da direita.
    if janela.winfo_width() < 1300:
        coluna = 280  # tela pequena: coluna da direita mais estreita
    else:
        coluna = 340
    largura = janela.winfo_width() - 96 - coluna - 40
    altura = largura * 9 // 16
    altura_livre = janela.winfo_height() - 350  # topo, título e miniaturas
    if altura > altura_livre:
        altura = altura_livre
        largura = altura * 16 // 9

    esquerda = tk.Frame(area, bg=BRANCO)
    esquerda.pack(side="left", anchor="n")
    direita = tk.Frame(area, bg=BRANCO)
    direita.pack(side="left", anchor="n", padx=(40, 0))

    prints = portal["prints"]
    if len(prints) > 0:
        quadro(esquerda, prints[print_aberto], largura, altura).pack()
    else:
        quadro(esquerda, portal["capa"], largura, altura).pack()
        texto(esquerda, "Ainda não há prints deste sistema.",
              cor=CINZA_TEXTO).pack(anchor="w", pady=(10, 0))

    # Miniaturas: as 4 dividem a largura do print grande. Clicar troca o print.
    miniaturas = tk.Frame(esquerda, bg=BRANCO)
    miniaturas.pack(anchor="w", pady=(12, 0))
    largura_mini = (largura - 3 * 12 - 4 * 6) // 4
    for numero in range(len(prints)):
        miniatura(miniaturas, portal, numero, numero == print_aberto, largura_mini)

    # Coluna da direita: capa, descrição, o botão, e depois setores e endereço
    quadro(direita, portal["capa"], coluna, coluna * 9 // 16).pack(anchor="w")
    descricao = texto(direita, portal["descricao"])
    descricao.config(wraplength=coluna)
    descricao.pack(anchor="w", pady=(18, 20))
    botao_vermelho(direita, "Abrir portal", lambda: abrir_portal(portal), coluna).pack(anchor="w", pady=(0, 24))

    texto(direita, "Liberado para", PEQUENA, CINZA_TEXTO).pack(anchor="w")
    setores = texto(direita, ", ".join(portal["setores"]))
    setores.config(wraplength=coluna)
    setores.pack(anchor="w", pady=(2, 14))
    texto(direita, "Endereço", PEQUENA, CINZA_TEXTO).pack(anchor="w")
    endereco = texto(direita, portal["endereco"])
    endereco.config(wraplength=coluna)
    endereco.pack(anchor="w", pady=(2, 0))


def miniatura(pai, portal, numero, aberto, largura):
    # Uma moldura de 3 pixels em volta. Fica vermelha no print que está aberto.
    if aberto:
        cor = VERMELHO
    else:
        cor = BRANCO
    moldura = tk.Frame(pai, bg=cor, padx=3, pady=3)
    moldura.pack(side="left", padx=(0, 12))
    mini = quadro(moldura, portal["prints"][numero], largura, largura * 9 // 16)
    mini.bind("<Button-1>", lambda evento: tela_detalhes(portal, numero))
    mini.pack()


# ---------------------------------------------------------------------
# 4. ADMINISTRAÇÃO
# ---------------------------------------------------------------------

def tela_administracao(aba="Portais"):
    global tela_atual, aba_atual
    tela_atual = "administração"
    aba_atual = aba
    area = montar_topo("admin")

    # Menu do lado esquerdo
    menu = tk.Frame(area, bg=BRANCO)
    menu.pack(side="left", anchor="n", padx=(0, 48))
    for nome in ["Portais", "Setores", "Funcionários"]:
        item_lateral(menu, nome, aba == nome)

    conteudo = tk.Frame(area, bg=BRANCO)
    conteudo.pack(side="left", anchor="n", fill="both", expand=True)
    if aba == "Portais":
        aba_portais(conteudo)
    elif aba == "Setores":
        aba_setores(conteudo)
    else:
        aba_funcionarios(conteudo)


def item_lateral(menu, nome, selecionado):
    if selecionado:
        item = botao_redondo(menu, nome, lambda: tela_administracao(nome),
                             VERMELHO_CLARO, VERMELHO, VERMELHO_CLARO, 200, esquerda=True)
    else:
        item = botao_redondo(menu, nome, lambda: tela_administracao(nome),
                             BRANCO, PRETO, CINZA, 200, esquerda=True)
    item.pack(pady=(0, 6))


def cabecalho(conteudo, titulo, botao, comando):
    # Título da aba com o botão principal ao lado.
    topo = tk.Frame(conteudo, bg=BRANCO)
    topo.pack(fill="x")
    texto(topo, titulo, TITULO).pack(side="left")
    if botao != "":
        botao_vermelho(topo, botao, comando).pack(side="right")


# ----- Portais -----

def aba_portais(conteudo):
    cabecalho(conteudo, "Portais", "Novo portal", lambda: tela_portal(None))
    caixa = tabela(conteudo)
    for numero in range(len(dados["portais"])):
        linha_portal(caixa, numero)


def linha_portal(caixa, numero):
    portal = dados["portais"][numero]
    linha(caixa, numero, portal["nome"], ", ".join(portal["setores"]),
          lambda: tela_portal(numero), lambda: remover_portal(numero), portal["capa"])


def remover_portal(numero):
    nome = dados["portais"][numero]["nome"]
    if messagebox.askyesno("Remover portal", "Remover " + nome + "?\nEle some para todos os setores."):
        dados["portais"].pop(numero)
        cadastro.salvar(dados)
        tela_administracao("Portais")


def tela_portal(numero):
    # numero = None é um portal novo. Senão, é a posição dele na lista.
    if numero is None:
        portal = {"nome": "", "endereco": "https://", "descricao": "",
                  "capa": "", "prints": [], "setores": []}
    else:
        portal = dados["portais"][numero]

    global tela_atual
    tela_atual = "formulário"
    area = montar_topo("admin")
    if numero is None:
        texto(area, "Novo portal", TITULO).pack(anchor="w", pady=(0, 20))
    else:
        texto(area, "Editar portal", TITULO).pack(anchor="w", pady=(0, 20))

    esquerda = tk.Frame(area, bg=BRANCO)
    esquerda.pack(side="left", anchor="n")
    direita = tk.Frame(area, bg=BRANCO)
    direita.pack(side="left", anchor="n", padx=(56, 0))

    # As imagens escolhidas ficam guardadas aqui até a pessoa clicar em Salvar.
    imagens = {"capa": portal["capa"], "prints": list(portal["prints"])}

    # Coluna da esquerda: textos e setores
    campo_nome = campo(esquerda, "Nome", portal["nome"])
    campo_endereco = campo(esquerda, "Endereço (começa com http:// ou https://)", portal["endereco"])
    campo_descricao = campo(esquerda, "O que o sistema faz (uma frase)", portal["descricao"])

    texto(esquerda, "Setores que veem este portal", NEGRITO).pack(anchor="w")
    marcados = {}
    for setor in dados["setores"]:
        marcado = tk.BooleanVar(value=setor in portal["setores"])
        tk.Checkbutton(esquerda, text=setor, variable=marcado, font=FONTE, bg=BRANCO,
                       activebackground=BRANCO, highlightthickness=0, bd=0).pack(anchor="w", pady=1)
        marcados[setor] = marcado

    # Coluna da direita: capa e prints
    texto(direita, "Capa", NEGRITO).pack(anchor="w")
    area_capa = tk.Frame(direita, bg=BRANCO)
    area_capa.pack(anchor="w", pady=(6, 20))

    def desenhar_capa():
        for parte in area_capa.winfo_children():
            parte.destroy()
        quadro(area_capa, imagens["capa"], 192, 108).pack(side="left")
        botao_cinza(area_capa, "Escolher capa", trocar_capa).pack(side="left", padx=16)

    def trocar_capa():
        caminho = escolher_imagem()
        if caminho != "":
            imagens["capa"] = caminho
            desenhar_capa()

    texto(direita, "Prints do sistema (até 4)", NEGRITO).pack(anchor="w")
    area_prints = tk.Frame(direita, bg=BRANCO)
    area_prints.pack(anchor="w", pady=(6, 0))

    def desenhar_prints():
        for parte in area_prints.winfo_children():
            parte.destroy()
        for numero_print in range(len(imagens["prints"])):
            print_do_formulario(area_prints, imagens["prints"], numero_print, desenhar_prints)
        if len(imagens["prints"]) < 4:
            botao_cinza(area_prints, "Adicionar print", adicionar_print).pack(side="left", anchor="n")

    def adicionar_print():
        caminho = escolher_imagem()
        if caminho != "":
            imagens["prints"].append(caminho)
            desenhar_prints()

    desenhar_capa()
    desenhar_prints()

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
                    "descricao": campo_descricao.get().strip(), "capa": imagens["capa"],
                    "prints": imagens["prints"], "setores": setores}
            if numero is None:
                dados["portais"].append(novo)
            else:
                dados["portais"][numero] = novo
            cadastro.salvar(dados)
            tela_administracao("Portais")

    fim = tk.Frame(direita, bg=BRANCO)
    fim.pack(anchor="w", pady=(40, 0))
    botao_vermelho(fim, "Salvar portal", salvar).pack(side="left")
    botao_cinza(fim, "Cancelar", lambda: tela_administracao("Portais")).pack(side="left", padx=12)
    campo_nome.focus_set()


def print_do_formulario(pai, prints, numero, redesenhar):
    caixa = tk.Frame(pai, bg=BRANCO)
    caixa.pack(side="left", padx=(0, 12))
    quadro(caixa, prints[numero], 96, 54).pack()

    def tirar():
        prints.pop(numero)
        redesenhar()

    botao_link(caixa, "Tirar", tirar, PEQUENA, VERMELHO).pack(anchor="w", pady=(4, 0))


# ----- Setores -----

def aba_setores(conteudo):
    cabecalho(conteudo, "Setores", "", None)

    novo = tk.Frame(conteudo, bg=BRANCO)
    novo.pack(anchor="w", pady=(20, 0))
    campo_setor = tk.Entry(novo, font=FONTE, width=28, fg=PRETO, bg=CINZA, relief="flat", bd=9,
                           highlightthickness=2, highlightbackground=CINZA, highlightcolor=VERMELHO)
    campo_setor.pack(side="left", padx=(0, 12))
    botao_vermelho(novo, "Adicionar setor", lambda: adicionar_setor(campo_setor.get())).pack(side="left")

    caixa = tabela(conteudo)
    for numero in range(len(dados["setores"])):
        linha_setor(caixa, numero)


def linha_setor(caixa, numero):
    setor = dados["setores"][numero]
    quantos = 0
    for usuario in dados["usuarios"]:
        if usuario["setor"] == setor:
            quantos = quantos + 1
    if quantos == 1:
        detalhe = "1 funcionário"
    else:
        detalhe = str(quantos) + " funcionários"
    linha(caixa, numero, setor, detalhe, None, lambda: remover_setor(numero))


def adicionar_setor(nome):
    nome = nome.strip()
    if nome == "":
        messagebox.showinfo("Central de Acessos", "Escreva o nome do setor ao lado do botão.")
    elif nome in dados["setores"]:
        messagebox.showinfo("Central de Acessos", "Esse setor já existe.")
    else:
        dados["setores"].append(nome)
        cadastro.salvar(dados)
        tela_administracao("Setores")


def remover_setor(numero):
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


# ----- Funcionários -----

def aba_funcionarios(conteudo):
    cabecalho(conteudo, "Funcionários", "Novo funcionário", lambda: tela_funcionario(None))
    caixa = tabela(conteudo)
    for numero in range(len(dados["usuarios"])):
        linha_funcionario(caixa, numero)


def linha_funcionario(caixa, numero):
    usuario = dados["usuarios"][numero]
    if usuario["admin"]:
        detalhe = "Administrador  —  " + usuario["usuario"]
        remover = None  # o administrador não pode ser removido
    else:
        detalhe = usuario["setor"] + "  —  " + usuario["usuario"]
        remover = lambda: remover_funcionario(numero)
    linha(caixa, numero, usuario["nome"], detalhe, lambda: tela_funcionario(numero), remover)


def remover_funcionario(numero):
    usuario = dados["usuarios"][numero]
    if messagebox.askyesno("Remover funcionário", "Remover " + usuario["nome"] + "?"):
        dados["usuarios"].pop(numero)
        cadastro.salvar(dados)
        tela_administracao("Funcionários")


def tela_funcionario(numero):
    if numero is None:
        usuario = {"usuario": "", "senha": "", "nome": "", "setor": "", "admin": False}
    else:
        usuario = dados["usuarios"][numero]

    global tela_atual
    tela_atual = "formulário"
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
        escolha.pack(fill="x", ipady=6, pady=(6, 0))

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
    fim.pack(anchor="w", pady=(32, 0))
    botao_vermelho(fim, "Salvar funcionário", salvar).pack(side="left")
    botao_cinza(fim, "Cancelar", lambda: tela_administracao("Funcionários")).pack(side="left", padx=12)
    campo_nome.focus_set()


# ---------------------------------------------------------------------
# 5. AO VIVO: mostra as mudanças feitas por outros computadores
# ---------------------------------------------------------------------

def acompanhar_mudancas():
    global dados, usuario_logado, ultima_mudanca

    # Quem está preenchendo um formulário não pode perder o que digitou,
    # então só atualizamos depois que a pessoa sair dele.
    if tela_atual != "formulário" and cadastro.quando_mudou() != ultima_mudanca:
        try:
            novos_dados = cadastro.carregar()
        except ValueError:
            novos_dados = None  # o arquivo estava sendo salvo; tenta de novo daqui a pouco

        if novos_dados is not None:
            dados = novos_dados
            ultima_mudanca = cadastro.quando_mudou()
            atualizar_tela()

    janela.after(SEGUNDOS_PARA_CONFERIR * 1000, acompanhar_mudancas)


def atualizar_tela():
    global usuario_logado
    if usuario_logado is None:
        return

    # Procura a pessoa de novo nos dados novos: o setor dela pode ter mudado.
    login = usuario_logado["usuario"]
    usuario_logado = None
    for usuario in dados["usuarios"]:
        if usuario["usuario"] == login:
            usuario_logado = usuario

    if usuario_logado is None:
        tela_entrada()  # a conta foi removida
    elif tela_atual == "meus acessos":
        tela_meus_acessos()
    elif tela_atual == "administração":
        tela_administracao(aba_atual)


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

try:
    dados = cadastro.carregar()
    ultima_mudanca = cadastro.quando_mudou()
except OSError:
    messagebox.showerror("Central de Acessos", "Não consegui abrir a pasta dos dados:\n" + cadastro.PASTA_DADOS +
                         "\n\nConfira se o computador está na rede e se o caminho em pasta_dados.txt está certo.")
    janela.destroy()
else:
    tela_entrada()
    acompanhar_mudancas()
    janela.mainloop()
