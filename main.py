import math
from random import randrange

from copy import deepcopy

inf = float(math.inf)

jogo = []
ultima_jogada = (None, None, None)  # linha/coluna/simbolo
VAZIO = "_"

jogador, adversario = 'X', 'O'

def todas_jogadas_possiveis(jogo_atual):
    cada_jogada_do_no = []
    for x in range(3):
        for i in range(3):
            if jogo_atual[x][i] == VAZIO:
                cada_jogada_do_no.append((x,i))
    return cada_jogada_do_no

def resultado_do_jogo(jogo):
    for i in range(3):
        if jogo[i][0] == jogador and jogo[i][1] == jogador and jogo[i][2] == jogador:
            return 10
        if jogo[i][0] == adversario and jogo[i][1] == adversario and jogo[i][2] == adversario:
            return -10
        if jogo[0][i] == jogador and jogo[1][i] == jogador and jogo[2][i] == jogador:
            return 10
        if jogo[0][i] == adversario and jogo[1][i] == adversario and jogo[2][i] == adversario:
            return -10

    if jogo[0][0] == jogador and jogo[1][1] == jogador and jogo [2][2] == jogador or jogo[0][2] == jogador and jogo[1][1] == jogador and jogo[2][0] == jogador:
        return 10
    if jogo[0][0] == adversario and jogo[1][1] == adversario and jogo [2][2] == adversario or jogo[0][2] == adversario and jogo[1][1] == adversario and jogo[2][0] == adversario:
        return -10

    return 0

def minmax(jogo, jogador_do_no, a=-inf, b=inf):
    copia_jogo = deepcopy(jogo)
    jogadas = todas_jogadas_possiveis(copia_jogo)
    pontuacao_das_jogadas = []

    if jogador_do_no == jogador:
        for jogada in jogadas:
            copia_jogo_da_jogada = deepcopy(copia_jogo)
            copia_jogo_da_jogada[jogada[0]][jogada[1]] = jogador
            vantagem_jogada = resultado_do_jogo(copia_jogo_da_jogada)

            if vantagem_jogada == 10 or vantagem_jogada == -10 or not tem_jogada(copia_jogo_da_jogada):
                pontuacao_das_jogadas.append(vantagem_jogada)
            else:
                pontos, tab = minmax(copia_jogo_da_jogada, adversario, a, b)
                if pontos >= b:
                    return pontos, tab
                a = max(a, pontos)
                pontuacao_das_jogadas.append(pontos)
        melhor_pontuacao = max(pontuacao_das_jogadas)
    else:
        for jogada in jogadas:
            copia_jogo_da_jogada = deepcopy(copia_jogo)
            copia_jogo_da_jogada[jogada[0]][jogada[1]] = adversario
            vantagem_jogada = resultado_do_jogo(copia_jogo_da_jogada)

            if vantagem_jogada == 10 or vantagem_jogada == -10 or not tem_jogada(copia_jogo_da_jogada):
                pontuacao_das_jogadas.append(vantagem_jogada)
            else:
                pontos, tab = minmax(copia_jogo_da_jogada, jogador, a, b)
                if pontos <= a:
                    return pontos, tab
                b = min(b, pontos)
                pontuacao_das_jogadas.append(pontos)
        melhor_pontuacao = min(pontuacao_das_jogadas)

    melhor_jogada = jogadas[pontuacao_das_jogadas.index(melhor_pontuacao)]

    return melhor_pontuacao, melhor_jogada

def inicia_jogo():
    global jogo, ultima_jogada
    ultima_jogada = (0, 0, jogador)

    jogo = [[VAZIO, VAZIO, VAZIO], [VAZIO, VAZIO, VAZIO], [VAZIO, VAZIO, VAZIO]]
    print("Jogo está iniciando\n")

def printa_jogo():
    display = f"\
  {jogo[0][0]}|{jogo[0][1]}|{jogo[0][2]}\n\
  {jogo[1][0]}|{jogo[1][1]}|{jogo[1][2]}\n\
  {jogo[2][0]}|{jogo[2][1]}|{jogo[2][2]}\n\
  "
    print(display)

def realiza_jogada(linha, coluna, simbolo):
    global jogo, ultima_jogada
    ultima_jogada = (linha, coluna, simbolo)
    jogo[linha][coluna] = simbolo

    if simbolo == jogador:
        return adversario
    return simbolo


def alguem_ganhou():
    global jogo

    simbolo = ultima_jogada[2]
    linha, coluna = 0, 0
    for i in range(3):  # vitoria por linhas/colunas
        if jogo[i][ultima_jogada[1]] == ultima_jogada[2]:
            coluna += 1
        if jogo[ultima_jogada[0]][i] == ultima_jogada[2]:
            linha += 1

    if linha == 3 or coluna == 3:
        return True

    # checa diagonais
    if jogo[0][0] == simbolo and jogo[1][1] == simbolo and jogo[2][2] == simbolo:
        return True
    if jogo[2][0] == simbolo and jogo[1][1] == simbolo and jogo[0][2] == simbolo:
        return True

    return False

def jogada_eh_valida(x, y):
    global jogo
    if x > 2 or y > 2 or x < 0 or y < 0:
        return False
    if jogo[x][y] == "_":
        return True
    return False

def da_resultado():
    global jogo, ultima_jogada
    if alguem_ganhou():
        print(f"O vencedor foi: {ultima_jogada[2]}")
    elif not tem_jogada(jogo):
        print("Houve empate")
    else:
        print("Resultado inconclusivo")

    printa_jogo()

def tem_jogada(jogo):
    if any(filter(lambda item: item == VAZIO, [x for y in jogo for x in y])):
        return True
    return False

def player_vs_bot():
    global jogo
    inicia_jogo()

    player = jogador
    while not alguem_ganhou():
        printa_jogo()
        if player == adversario:
            _, melhor_jogada = minmax(jogo, adversario)
            realiza_jogada(melhor_jogada[0], melhor_jogada[1], adversario)
            player = jogador
            continue
        try:
            x, y = input(f"Jogador: {player}, digite sua jogada (linha, coluna): ").split()
            x, y = int(x), int(y)
        except:
            print("Entrada invalida")
            continue

        if jogada_eh_valida(x, y):
            player = realiza_jogada(x, y, player)
        else:
            print("Jogada invalida")

        if not tem_jogada(jogo):
            break
    da_resultado()

def bot_vs_bot():
    global jogo
    inicia_jogo()

    x1 = randrange(3)
    y1 = randrange(3)
    jogo[x1][y1] = jogador
    player = adversario

    while not alguem_ganhou():
        printa_jogo()
        if player == adversario: # O
            _, melhor_jogada = minmax(jogo, adversario)
            realiza_jogada(melhor_jogada[0], melhor_jogada[1], adversario)
            player = jogador
        else: # X
            _, melhor_jogada = minmax(jogo, jogador)
            realiza_jogada(melhor_jogada[0], melhor_jogada[1], jogador)
            player = adversario

        if not tem_jogada(jogo):
            break
    da_resultado()


def main():
    try:
        print("Digite uma opção")
        opt = input("(1) jogador X maquina\n(2) maquina X maquina\n")
        opt = int(opt)
        if opt == 1:
            player_vs_bot()
        elif opt == 2:
            bot_vs_bot()
        else:
            raise Exception()
    except:
        print("houve um erro\n")
        main()
main()
