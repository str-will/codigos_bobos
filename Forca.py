# BIBLIOTECAS
import random
# VARIAVEIS GLOBAIS
palavras_secretas = ['CARRO', 'CASA', 'PRAIA', 'TRABALHO', 'ESTUDO', 'PROGRAMACAO', 'FUTEBOL', 'ESCOLA', 'COMPUTADOR', 'INTERNET']
# FUNCOES
def jogo_da_forca():
    palavra_sorteada = random.choice(palavras_secretas)
    n_caracteres = len(palavra_sorteada)
    chutes_jogador = list()
    espacos = ['_']*n_caracteres
    acertos = 0
    tentativas = 0
    while tentativas < 10:
        print('__________________________________________')
        print('▮ Restam %d tentativas  ▮'%(10-tentativas))
        print('▮ Chutes anteriores: ',' '.join(chutes_jogador) ,' ▮')
        print('▮ Palavra secreta: '+' '.join(espacos),' ▮')
        resp_jogador = input('Seu chute: ')
        if resp_jogador not in chutes_jogador:
            chutes_jogador.append(resp_jogador)
        if resp_jogador.upper() not in (palavra_sorteada):
            tentativas += 1
        elif resp_jogador in espacos:
            print('\n▮ Você já chutou esse número, bobão ▮')
        else:
            for pos,letra in enumerate(palavra_sorteada):
                if resp_jogador.upper() == letra:
                    espacos[pos] = resp_jogador
                    acertos += 1
        if acertos == n_caracteres:
            print('Parabéns, você venceu!!')
            break
        if tentativas == 10:
            print('Perdeste')
    return print('Palavra secreta:',' '.join(espacos))
#BLOCO PRINCIPAL
print(' ▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮\n',' JOGO DA FORCA\n','▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮\n'),
resp_jogador = input('Gostaria do jogar o jogo da Forca (Game of the year remastered deluxe)?\n')
if resp_jogador.lower() in ['sim','s','ss','obvio']:
    while resp_jogador.lower() in ['sim','s','ss','obvio']:
        jogo_da_forca()
        resp_jogador = input('▮▮▮▮▮▮\nJogar novamente?\n')