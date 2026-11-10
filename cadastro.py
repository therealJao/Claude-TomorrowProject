# CADASTRO
# Aqui o programa lê e grava tudo no arquivo dados.json.
# json é só o formato do arquivo: json.load lê e json.dump grava.

import json

# Pra ver ao vivo em vários computadores, coloque aqui a pasta da rede,
# por exemplo: PASTA = "//servidor/central/"
# Deixando vazio, usa o dados.json que está junto com o programa.
PASTA = ""
ARQUIVO = PASTA + "dados.json"


def carregar():
    arquivo = open(ARQUIVO, "r", encoding="utf-8")
    dados = json.load(arquivo)
    arquivo.close()
    return dados


def salvar(dados):
    arquivo = open(ARQUIVO, "w", encoding="utf-8")
    json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    arquivo.close()


def ler_texto():
    # Usado no "ao vivo": lê o arquivo inteiro como texto,
    # pra comparar com a última vez e ver se alguém mudou alguma coisa.
    arquivo = open(ARQUIVO, "r", encoding="utf-8")
    texto = arquivo.read()
    arquivo.close()
    return texto


def texto_para_dados(texto):
    return json.loads(texto)
