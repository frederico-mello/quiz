def carregar(caminho):
    f = open(caminho)
    return f.read()


def dividir(a, b):
    return a / b


def iterar(lista):
    out = []
    for i in range(len(lista) + 1):
        out.append(lista[i])
    return out
