# CADASTRO
# Lê e grava os dados da Central no arquivo dados.json.
# É por causa deste arquivo que nada se perde quando o programa fecha.

import json
import os
import shutil
import sys
import time

# A pasta onde o programa está. No executável (.exe) é a pasta do .exe.
if getattr(sys, "frozen", False):
    PASTA_DO_PROGRAMA = os.path.dirname(sys.executable)
else:
    PASTA_DO_PROGRAMA = os.path.dirname(os.path.abspath(__file__))

# Para várias pessoas verem os mesmos dados ao vivo, escreva no arquivo
# pasta_dados.txt o caminho de uma pasta da rede, por exemplo: \\servidor\central
# Sem esse arquivo, os dados ficam na mesma pasta do programa.
PASTA_DADOS = PASTA_DO_PROGRAMA
if os.path.exists(os.path.join(PASTA_DO_PROGRAMA, "pasta_dados.txt")):
    with open(os.path.join(PASTA_DO_PROGRAMA, "pasta_dados.txt"), encoding="utf-8") as arquivo:
        PASTA_DADOS = arquivo.read().strip()

ARQUIVO = os.path.join(PASTA_DADOS, "dados.json")


def carregar():
    # Na primeira vez o arquivo ainda não existe, então criamos um.
    if not os.path.exists(ARQUIVO):
        salvar(dados_iniciais())

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar(dados):
    # Primeiro grava num arquivo temporário e depois troca de uma vez.
    # Assim outro computador nunca lê o dados.json pela metade.
    temporario = ARQUIVO + ".tmp"
    with open(temporario, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    # Se outro computador estiver lendo o arquivo nessa hora, o Windows não
    # deixa trocar. Então esperamos um pouquinho e tentamos de novo.
    for tentativa in range(10):
        try:
            os.replace(temporario, ARQUIVO)
            return
        except PermissionError:
            time.sleep(0.2)
    os.replace(temporario, ARQUIVO)


def quando_mudou():
    # A hora da última vez que alguém salvou o dados.json.
    if not os.path.exists(ARQUIVO):
        return 0
    return os.path.getmtime(ARQUIVO)


def copiar_imagem(caminho):
    # Guarda uma cópia na pasta imagens, junto com os dados. Assim todos os
    # computadores enxergam a imagem, e ela não some se o original for apagado.
    os.makedirs(os.path.join(PASTA_DADOS, "imagens"), exist_ok=True)
    nome = "imagens/" + os.path.basename(caminho)
    destino = os.path.join(PASTA_DADOS, nome)
    if os.path.abspath(caminho) != os.path.abspath(destino):
        shutil.copy(caminho, destino)
    return nome


def caminho_da_imagem(nome):
    # No dados.json a imagem fica como "imagens/capa.png". Aqui vira o caminho completo.
    if nome == "":
        return ""
    return os.path.join(PASTA_DADOS, nome)


def dados_iniciais():
    return {
        "setores": ["Financeiro", "Operações", "Comercial", "Recursos Humanos"],

        "usuarios": [
            {"usuario": "admin", "senha": "admin123", "nome": "Administrador",
             "setor": "", "admin": True},
            # Contas de teste para a apresentação. Podem ser apagadas depois.
            {"usuario": "teste.financeiro", "senha": "teste123", "nome": "Teste Financeiro",
             "setor": "Financeiro", "admin": False},
            {"usuario": "teste.operacoes", "senha": "teste123", "nome": "Teste Operações",
             "setor": "Operações", "admin": False},
        ],

        "portais": [
            {"nome": "Site da Portonave",
             "endereco": "https://www.portonave.com.br",
             "descricao": "Site do terminal, com notícias, serviços e contatos.",
             "capa": "", "prints": [],
             "setores": ["Financeiro", "Operações", "Comercial", "Recursos Humanos"]},
            {"nome": "Portal Único Siscomex",
             "endereco": "https://portalunico.siscomex.gov.br",
             "descricao": "Registro e acompanhamento das operações de importação e exportação.",
             "capa": "", "prints": [],
             "setores": ["Operações", "Comercial"]},
            {"nome": "MarineTraffic",
             "endereco": "https://www.marinetraffic.com",
             "descricao": "Posição dos navios em tempo real e previsão de chegada ao porto.",
             "capa": "", "prints": [],
             "setores": ["Operações", "Comercial"]},
            {"nome": "Tábuas de maré",
             "endereco": "https://www.marinha.mil.br/chm/tabuas-de-mare",
             "descricao": "Previsão de marés dos portos brasileiros, publicada pela Marinha.",
             "capa": "", "prints": [],
             "setores": ["Operações"]},
            {"nome": "Portal da NF-e",
             "endereco": "https://www.nfe.fazenda.gov.br/portal/principal.aspx",
             "descricao": "Consulta de nota fiscal eletrônica pela chave de acesso.",
             "capa": "", "prints": [],
             "setores": ["Financeiro"]},
            {"nome": "eSocial",
             "endereco": "https://www.gov.br/esocial/pt-br",
             "descricao": "Envio das informações trabalhistas dos funcionários ao governo.",
             "capa": "", "prints": [],
             "setores": ["Recursos Humanos"]},
        ],
    }
