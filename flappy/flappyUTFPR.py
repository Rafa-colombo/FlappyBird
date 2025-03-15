import pygame
import os
import random

largura, altura = 512, 512

img_cano = pygame.image.load(os.path.join('img', 'obstaculo amarelo.png'))
img_fundo = pygame.image.load(os.path.join('img', 'cartoon utfpr 2.png'))
img_raposa = pygame.image.load(os.path.join('img', 'raposinha.png'))

nova_largura_raposa = img_raposa.get_width() // 16
nova_altura_raposa = img_raposa.get_height() // 16
img_raposa_reduzida = pygame.transform.scale(img_raposa, (nova_largura_raposa, nova_altura_raposa))

pygame.font.init()
fonte_pontos = pygame.font.SysFont('arial', 30)

class Raposa:
    # animação
    rotacao_max = 25
    vel_rotacao = 20
    temp_animacao = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.imagem = img_raposa_reduzida

    def pular(self):
        self.velocidade = 20
        self.tempo = 0
        self.altura = self.y
        print("pulou")

    def mover(self):
        # cálculo deslocamento
        self.tempo -= 1
        deslocamento = 5.5 * (self.tempo**2) + self.velocidade * self.tempo

        # ajustes
        if deslocamento > 15:
            deslocamento = 15
        elif deslocamento < 0:
            deslocamento -= 15
        self.y += deslocamento

        # ângulo dos pulos
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacao_max:
                self.angulo = self.rotacao_max
        else:
            if self.angulo > -90:
                self.angulo -= self.vel_rotacao

    def desenhar(self, tela):
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Obstaculo:
    distancia, vel_cano = 200, 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.cano_top = img_cano
        self.cano_base = img_cano
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 320)
        self.pos_topo = self.altura - self.cano_top.get_height()
        self.pos_base = self.altura + self.distancia

    def mover(self):
        self.x -= self.vel_cano

    def desenhar(self, tela):
        tela.blit(self.cano_top, (self.x, self.pos_topo))
        tela.blit(self.cano_base, (self.x, self.pos_base))

    def colisao(self, Raposa):
        raposa_mask = Raposa.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_top)
        base_mask = pygame.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - Raposa.x, self.pos_topo - round(Raposa.y))
        distancia_base = (self.x - Raposa.x, self.pos_base - round(Raposa.y))

        colisao_topo = raposa_mask.overlap(topo_mask, distancia_topo)
        colisao_base = raposa_mask.overlap(base_mask, distancia_base)

        if colisao_topo or colisao_base:
            return True
        else:
            return False


def d_tela(tela, Raposas, Obstaculos, pontos):
    tela.blit(img_fundo, (0, 0))
    for Raposa in Raposas:
        Raposa.desenhar(tela)
    for Obstaculo in Obstaculos:
        Obstaculo.desenhar(tela)

    texto = fonte_pontos.render(f"Pontuação: {pontos}", True, (0, 0, 0))
    tela.blit(texto, (largura - 10 - texto.get_width(), 10))
    pygame.display.update()


Raposas = [Raposa(50, 10)]
Obstaculos = [Obstaculo(612)]

def append_obs():
    novo_obstaculo = Obstaculo(512)
    Obstaculos.append(novo_obstaculo)

def main():

    tela = pygame.display.set_mode((largura, altura))
    pontos, relogio = 0, pygame.time.Clock()

    while True:
        relogio.tick(30)  # renderizar 30hz

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for Raposa in Raposas:
                        Raposa.pular()

        for Raposa in Raposas:
            Raposa.mover()

        remover_obstaculos = []
        add_obs = False
        for Obstaculo in Obstaculos:
            for i, Raposa in enumerate(Raposas):
                if Obstaculo.colisao(Raposa):
                    Raposas.pop(i)
                    print("morreu, cano")
                if not Obstaculo.passou and Raposa.x > Obstaculo.x:
                    Obstaculo.passou = True
                    add_obs = True
            Obstaculo.mover()
            if Obstaculo.x + Obstaculo.cano_top.get_width() < 0:
                remover_obstaculos.append(Obstaculo)
        if add_obs:
            pontos += 1
            append_obs()
        for Obstaculo in remover_obstaculos:
            Obstaculos.remove(Obstaculo)

        for i, Raposa in enumerate(Raposas):
            if (Raposa.y + Raposa.imagem.get_height() > 512) or Raposa.y < 0:
                Raposas.pop(i)
                print("morreu, borsas")

        d_tela(tela, Raposas, Obstaculos, pontos)

if __name__ == '__main__':
    main()
