# CADASTRO
# Lê e grava todos os dados da Central no arquivo dados.json.
# É por causa deste arquivo que nada se perde quando o programa fecha.

import json
import os

ARQUIVO = "dados.json"


def carregar():
    # Na primeira vez o arquivo ainda não existe: criamos com os exemplos.
    if not os.path.exists(ARQUIVO):
        salvar(dados_de_exemplo())

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def dados_de_exemplo():
    # Tudo aqui é EXEMPLO para o ensaio. A empresa troca pela interface.
    return {
        "setores": ["Financeiro", "Operações", "Recursos Humanos"],
        "usuarios": [
            {"usuario": "admin", "senha": "admin123", "nome": "Administrador (exemplo)",
             "setor": "", "admin": True},
            {"usuario": "ana", "senha": "ana123", "nome": "Ana Souza (exemplo)",
             "setor": "Financeiro", "admin": False},
            {"usuario": "bruno", "senha": "bruno123", "nome": "Bruno Lima (exemplo)",
             "setor": "Operações", "admin": False},
        ],
        "portais": [
            {"nome": "Agendamento de caminhões (exemplo)",
             "endereco": "https://example.com/agendamento",
             "descricao": "Reserva de horários para a entrada de caminhões no terminal.",
             "imagem": "",
             "setores": ["Operações"]},
            {"nome": "Escala de turnos (exemplo)",
             "endereco": "https://example.com/escala",
             "descricao": "Consulta da escala semanal e pedidos de troca de turno.",
             "imagem": "",
             "setores": ["Operações", "Recursos Humanos"]},
            {"nome": "Holerite e férias (exemplo)",
             "endereco": "https://example.com/holerite",
             "descricao": "Contracheques, informe de rendimentos e pedido de férias.",
             "imagem": "",
             "setores": ["Financeiro", "Operações", "Recursos Humanos"]},
        ],
    }
