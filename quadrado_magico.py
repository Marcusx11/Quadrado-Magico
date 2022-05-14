def faz_logica_circular(linha_atual, coluna_atual, ordem) -> tuple:
    if linha_atual < 0:
        linha_atual = ordem - 1
    elif linha_atual >= ordem:
        linha_atual = 0

    if coluna_atual >= ordem:
        coluna_atual = 0
    elif coluna_atual < 0:
        coluna_atual = ordem - 1

    return linha_atual, coluna_atual


def verifica_se_eh_quadrado_perfeito(matriz, soma: int) -> bool:
    quadrado_magico = True

    # Checando a soma por linha
    for linha in matriz:
        soma_l = 0
        for i in linha:
            soma_l += i
        if soma_l != soma:
            quadrado_magico = False
            return quadrado_magico

    # Checando a soma por colunas
    for i in range(len(matriz)):
        soma_c = 0
        for j in range(len(matriz)):
            soma_c += matriz[j][i]

        if soma_c != soma:
            quadrado_magico = False
            return quadrado_magico

    # Checando a soma pela diagonal principal
    soma_dp = 0
    for i in range(len(matriz)):
        soma_dp += matriz[i][i]
    if soma_dp != soma:
        quadrado_magico = False
        return quadrado_magico

    # Checando a soma pela diagonal secundária
    soma_ds = 0
    ordem = len(matriz) - 1
    for i in range(len(matriz)):
        soma_ds += matriz[i][ordem]
        ordem -= 1
    if soma_ds != soma:
        quadrado_magico = False
        return quadrado_magico

    return quadrado_magico


def constroi_quadrado_impar(ordem: int, matriz: list, disp: list) -> list:
    meio = ordem // 2
    matriz[0][meio] = disp[0]
    disp.remove(disp[0])
    linha_atual = 0
    coluna_atual = meio

    while len(disp) > 0:
        prox = disp.pop(0)
        linha_atual = linha_atual - 1
        coluna_atual = coluna_atual + 1

        linha_atual, coluna_atual = faz_logica_circular(linha_atual, coluna_atual, ordem)

        if matriz[linha_atual][coluna_atual] != 0:
            linha_atual = linha_atual + 1
            coluna_atual = coluna_atual - 1

            linha_atual, coluna_atual = faz_logica_circular(linha_atual, coluna_atual, ordem)

            linha_atual = linha_atual + 1

        matriz[linha_atual][coluna_atual] = prox

    return matriz


def constroi_realce_quad_esquerda(quadrante: list) -> dict:
    realce = dict()
    meio_matriz = len(quadrante) // 2
    for i in range(len(quadrante)):
        for j in range(len(quadrante)):
            if i != meio_matriz and j < meio_matriz:
                realce[(i, j)] = quadrante[i][j]

    # Pega-se os realces do meio da matriz
    for i in range(len(quadrante)):
        if i != 0 and i <= meio_matriz:
            realce[(meio_matriz, i)] = quadrante[meio_matriz][i]

    return realce


def substitui_valores_pelo_realce(quadrante: list, realce: dict) -> list:
    for tupla in realce:
        quadrante[tupla[0]][tupla[1]] = realce[tupla]
    return quadrante


def preenche_matriz_com_quadrantes(matriz: list, quadrante: list, lin_matriz: int, col_matriz: int):
    i_matriz = lin_matriz
    j_matriz = col_matriz
    for i in range(len(quadrante)):
        j_matriz = col_matriz
        for j in range(len(quadrante)):
            matriz[i_matriz][j_matriz] = quadrante[i][j]
            j_matriz += 1
        i_matriz += 1

    return matriz


def constroi_realce_quad_direita(quadrante: list) -> dict:
    meio_matriz = len(quadrante) // 2
    realce = dict()
    for i in range(len(quadrante)):
        for j in range(len(quadrante) - 1, meio_matriz + 1, -1):
            realce[(i, j)] = quadrante[i][j]

    return realce


def troca_se_valor_realce(realce_a: dict, realce_b: dict) -> tuple:
    for tupla in list(realce_a):
        aux = realce_b[tupla]
        realce_b[tupla] = realce_a[tupla]
        realce_a[tupla] = aux

    return realce_a, realce_b


def constroi_quadrado_par(ordem: int, matriz: list, disp: list) -> list:
    num_casas_quadrantes = ordem // 2
    quadrantes = dict()

    # Separando os quadrantes
    for quad in range(4):
        novo_quadrante = list()
        for i in range(num_casas_quadrantes):
            novo_quadrante.append([0] * num_casas_quadrantes)

        nova_lista_disp = list()
        for e in range(num_casas_quadrantes * num_casas_quadrantes):
            elem = disp.pop(0)
            nova_lista_disp.append(elem)

        quadrantes[quad + 1] = {
            "quadrante": novo_quadrante,
            "lista_disp": nova_lista_disp
        }

    # Resolvendo cada quadrante ímpar individualmente
    for k in list(quadrantes.keys()):
        quadrantes[k]["resultado"] = constroi_quadrado_impar(
            num_casas_quadrantes,
            quadrantes[k]["quadrante"],
            quadrantes[k]["lista_disp"]
        )

    # Criando os realces no primeiro e quarto quadrantes:
    # 1º quadrante:
    realce_1_quad = constroi_realce_quad_esquerda(quadrantes[1]["quadrante"])
    # 4º quadrante:
    realce_4_quad = constroi_realce_quad_esquerda(quadrantes[4]["quadrante"])

    # Trocando-se os valores dos realces
    realce_1_quad, realce_4_quad = troca_se_valor_realce(realce_1_quad, realce_4_quad)

    # Substituindo no primeiro e quarto quadrante
    quadrantes[1]["quadrante"] = substitui_valores_pelo_realce(quadrantes[1]["quadrante"], realce_1_quad)
    quadrantes[4]["quadrante"] = substitui_valores_pelo_realce(quadrantes[4]["quadrante"], realce_4_quad)

    # Para caso o quadrado seja de ordem maior que 6, precisa realizar uma lógica de trocar os quadrantes 3 e 2
    if ordem > 6:
        realce_3_quad = constroi_realce_quad_direita(quadrantes[3]["quadrante"])
        realce_2_quad = constroi_realce_quad_direita(quadrantes[2]["quadrante"])
        realce_3_quad, realce_2_quad = troca_se_valor_realce(realce_3_quad, realce_2_quad)

        # Substituindo no terceiro e segundo quadrante
        quadrantes[2]["quadrante"] = substitui_valores_pelo_realce(quadrantes[2]["quadrante"], realce_2_quad)
        quadrantes[3]["quadrante"] = substitui_valores_pelo_realce(quadrantes[3]["quadrante"], realce_3_quad)

    # Unindo os quadrantes em uma única matriz:
    matriz = preenche_matriz_com_quadrantes(matriz, quadrantes[1]["quadrante"], 0, 0)
    matriz = preenche_matriz_com_quadrantes(matriz, quadrantes[3]["quadrante"], 0, num_casas_quadrantes)
    matriz = preenche_matriz_com_quadrantes(matriz, quadrantes[4]["quadrante"], num_casas_quadrantes, 0)
    matriz = preenche_matriz_com_quadrantes(matriz, quadrantes[2]["quadrante"], num_casas_quadrantes,
                                            num_casas_quadrantes)

    return matriz


def cria_realces_par_perfeito(casas_realces: int, disp: list, ordem: int) -> dict:
    realce = dict()

    # Realces do canto superior esquerdo
    for i in range(casas_realces):
        for j in range(casas_realces):
            realce[(i, j)] = "REALCE"

    # Realces do canto superior direito
    for i in range(casas_realces):
        for j in range(ordem - casas_realces, ordem):
            realce[(i, j)] = "REALCE"

    # Realces do canto inferior esquerdo
    for i in range(ordem - casas_realces, ordem):
        for j in range(casas_realces):
            realce[(i, j)] = "REALCE"

    # Realces do canto inferior direito
    for i in range(ordem - casas_realces, ordem):
        for j in range(ordem - casas_realces, ordem):
            realce[(i, j)] = "REALCE"

    # Realces centrais da matriz
    for i in range(casas_realces, ordem - casas_realces):
        for j in range(casas_realces, ordem - casas_realces):
            realce[(i, j)] = "REALCE"

    # Preenchendo os realces
    c_disp = 0
    disp_a_deletar = list()
    for i in range(ordem):
        for j in range(ordem):
            if (i, j) in realce:
                elem = disp[c_disp]
                disp_a_deletar.append(elem)
                realce[(i, j)] = elem
            c_disp += 1

    # Deletando os elementos da lista que já foram preenchidos no realce
    for d in disp_a_deletar:
        disp.remove(d)

    return realce


def constroi_quadrado_par_perfeito(ordem: int, matriz: list, disp: list) -> list:
    casas_realces = ordem // 4
    realce_cantos = cria_realces_par_perfeito(casas_realces, disp, ordem)
    matriz = substitui_valores_pelo_realce(matriz, realce_cantos)

    # Terminando de preencher o resto da matriz
    for i in range(ordem - 1, -1, -1):
        for j in range(ordem - 1, -1, -1):
            if matriz[i][j] == 0:
                elem = disp.pop(0)
                matriz[i][j] = elem

    return matriz


def constroi_quadrado_magico(ordem):
    matriz = list()
    matriz = [[0] * ordem for i in range(ordem)]
    disp = [i + 1 for i in range(ordem * ordem)]
    soma = (ordem * (ordem * ordem + 1)) // 2

    # Caso de um quadrado mágico ímpar
    if ordem % 2 != 0:
        matriz = constroi_quadrado_impar(ordem, matriz, disp)
    elif ordem % 4 == 0:
        matriz = constroi_quadrado_par_perfeito(ordem, matriz, disp)
    else:
        """ O menor quadrado perfeito possível é um quadrado de tamanho 6x6 pois não existem
                    quadrados mágicos de tamanho 2x2, devido ao fato de que deve-se dividir os quadrantes """
        if ordem == 2:
            return None
        matriz = constroi_quadrado_par(ordem, matriz, disp)

    if verifica_se_eh_quadrado_perfeito(matriz, soma):
        return matriz
    return None


if __name__ == "__main__":
    matriz = constroi_quadrado_magico(150)
    if matriz is not None:
        for l in matriz:
            print(l)
    else:
        print(matriz)
