import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Define as dimensões da janela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Reduzindo a Escala da Imagem")

# Carrega a imagem (certifique-se de que o caminho está correto)
caminho_imagem = r"C:\Users\rafae\OneDrive\Desktop\python\projetoJogos\img\obstaculo amarelo.png"
imagem = pygame.image.load(caminho_imagem)

# Reduz a escala da imagem para 6.25% do tamanho original
nova_largura = imagem.get_width() // 1
nova_altura = imagem.get_height() // 1
imagem_reduzida = pygame.transform.scale(imagem, (nova_largura, nova_altura))

# Loop principal
while True:
    # Processa eventos (fechar a janela, etc.)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Preenche a tela com uma cor de fundo
    tela.fill((0, 0, 0))  # Preto

    # Desenha a imagem redimensionada na tela
    tela.blit(imagem_reduzida, (100, 100))  # Posição (x=100, y=100)

    # Atualiza o display
    pygame.display.flip()
