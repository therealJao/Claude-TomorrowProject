# REGRA DE ACESSO
# Decide quais portais cada pessoa pode ver na tela "Meus acessos".


def portais_do_usuario(usuario, portais):
    liberados = []
    for portal in portais:
        if usuario["admin"]:
            # O administrador vê todos, para conferir o cadastro.
            liberados.append(portal)
        elif usuario["setor"] in portal["setores"]:
            # O funcionário vê o portal se o setor dele estiver na lista.
            liberados.append(portal)
    return liberados
