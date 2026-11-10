# CADASTRO
# Lê e grava os dados da Central no arquivo dados.json.
# É por causa deste arquivo que nada se perde quando o programa fecha.

import json
import os
import shutil

ARQUIVO = "dados.json"


def carregar():
    # Na primeira vez o arquivo ainda não existe, então criamos um.
    if not os.path.exists(ARQUIVO):
        salvar(dados_iniciais())

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def copiar_imagem(caminho):
    # Guarda uma cópia na pasta imagens. Assim a imagem não some
    # se alguém apagar ou mover o arquivo original.
    destino = "imagens/" + os.path.basename(caminho)
    if os.path.abspath(caminho) != os.path.abspath(destino):
        shutil.copy(caminho, destino)
    return destino


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
