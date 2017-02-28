import pygame, sys
from pygame.locals import *
from random import *

largura = 900
altura = 400
        

class BalaInimigo(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.ImagemBala = pygame.image.load('imagens/Green_laser.png')

        self.rect = self.ImagemBala.get_rect()
        self.velocidadeBala = 6
        self.rect.top = posy
        self.rect.left = posx

    def trajetoria(self):
        self.rect.top = self.rect.top + self.velocidadeBala

    def colocar(self, superficie):
        superficie.blit(self.ImagemBala, self.rect)
        

class NaveInimiga(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        
        self.ImagemInimigo1 = pygame.image.load('imagens/inimigo1.png')
        self.ImagemInimigo2 = pygame.image.load('imagens/inimigo2.png')
        self.ImagemInimigo3 = pygame.image.load('imagens/inimigo3.png')

        self.listaImagens = [self.ImagemInimigo1, self.ImagemInimigo2, self.ImagemInimigo3]
        self.posImagem = randint(0, len(self.listaImagens)-1)
        self.ImagemInimigos = self.listaImagens[self.posImagem]
        self.direcaox = randint(0,1)
        self.direcaoy = randint(0,1)
        self.remover = 0
        
        self.rect = self.ImagemInimigos.get_rect()
        
        self.listaDisparo = []
        self.velocidade = 20
        self.rect.top = posy
        self.rect.left = posx

        self.configTempo = 8

    def comportamento(self, tempo):
        if self.direcaox == 0:
            if self.rect.left < 830:
                self.rect.left += 1
            else:
                self.direcaox = 1
        else:
            if self.rect.left > 5:
                self.rect.left -= 1
            else:
                self.direcaox = 0

        if self.direcaoy == 0:
            if self.rect.top < 150:
                self.rect.top += 1
            else:
                self.direcaoy = 1
        else:
            if self.rect.top > 5:
                self.rect.top -= 1
            else:
                self.direcaoy = 0
        if tempo == self.configTempo:
            x,y = self.rect.center
            balaI = BalaInimigo(x, (y + 5))
            self.listaDisparo.append(balaI)
            self.configTempo +=1
        
    def colocar(self, superficie):
        self.ImagemInimigos = self.listaImagens[self.posImagem]
        superficie.blit(self.ImagemInimigos, self.rect)


class Bala(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.ImagemBala = pygame.image.load('imagens/Green_laser.png')

        self.rect = self.ImagemBala.get_rect()
        self.velocidadeBala = 5
        self.rect.top = posy
        self.rect.left = posx

    def trajetoria(self):
        self.rect.top = self.rect.top - self.velocidadeBala

    def colocar(self, superficie):
        superficie.blit(self.ImagemBala, self.rect)



class NaveEspacial(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ImagemNave = pygame.image.load('imagens/nave_player.png')

        self.rect = self.ImagemNave.get_rect()
        self.rect.centerx = largura/2
        self.rect.centery = altura - 60

        self.listaDisparo = []
        self.vida = True
        self.velocidade = 20

    def movimentoDireita(self):
        self.rect.right += self.velocidade
        self.__movimento()

    def movimentoEsquerda(self):
        self.rect.left -= self.velocidade
        self.__movimento()

    def __movimento(self):
        if self.vida == True:
            if self.rect.left <= 0:
                self.rect.left = 0

            elif self.rect.right > 900:
                self.rect.right = 900

    def movimento(self):
        if self.vida == True:
            if self.rect.left <= 0:
                self.rect.left = 0

            elif self.rect.right > 900:
                self.rect.right = 900
 
    def disparar(self, x, y):
        minhaBala = Bala(x, y)
        self.listaDisparo.append(minhaBala)

        
    def colocar(self, superficie):
        superficie.blit(self.ImagemNave, self.rect)
    
def invasaoEspaco():
    
    pygame.init()

    audio_musica_fundo = pygame.mixer.Sound('audio\musica_tecno.ogg')
    audio_tiro = pygame.mixer.Sound('audio\mtiro_pistola.ogg')

    tela = pygame.display.set_mode((largura, altura))

    jogador = NaveEspacial()

    ImagemFundo = pygame.image.load('imagens/fundo.png')

    jogando = True

    inimigos = []

    numeroDeInimigos = 25

    audio_musica_fundo.play()
    audio_musica_fundo.set_volume(0.30)

    pygame.font.init()
    font_padrao = pygame.font.get_default_font()
    fonte_ganhou = pygame.font.SysFont(font_padrao, 30)
    
    while numeroDeInimigos > 0:
        inimigo = NaveInimiga(randint(5,830) ,randint(10,150))
        inimigos.append(inimigo)
        numeroDeInimigos -= 1 

    relogio = pygame.time.Clock()
    pontos = 0

    sair = 0

    while sair == 0:
        
        relogio.tick(50)

        tempo = int(pygame.time.get_ticks()/1000)
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == K_LEFT:
                    jogador.movimentoEsquerda()

                    
                if evento.key == K_RIGHT:
                    jogador.movimentoDireita()

                if evento.key == K_SPACE:
                    x,y = jogador.rect.center
                    jogador.disparar(x, y-50)    

        tela.blit(ImagemFundo, (0,0))

        if len(jogador.listaDisparo) > 0:
            for d in jogador.listaDisparo:
                d.colocar(tela)
                d.trajetoria()
                for i in inimigos:
                    if d.rect.colliderect(i):
                        try:
                            jogador.listaDisparo.remove(d)
                            i.remover = 1
                            audio_tiro.play()
                            audio_tiro.set_volume(0.5)
                            pontos += 10
                        except:
                            pass
                    
                if d.rect.top < -10 :
                    jogador.listaDisparo.remove(d)
                    
        
        jogador.colocar(tela)
        
        
        if len(inimigos) >0:
            for i in inimigos:
                if i.remover == 1:
                    inimigos.remove(i)
                if len(i.listaDisparo) > 0:
                    for d in i.listaDisparo:
                        d.colocar(tela)
                        d.trajetoria()
                        if d .rect.colliderect(jogador):
                            s = 0
                            while s == 0:
                                text4 = fonte_ganhou.render('Perdeu', 1,(255,255,255))
                                tela.blit(text4,(350,150))
                                pygame.display.update()

                                for evento in pygame.event.get():
                                    if evento.type == QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if evento.type == pygame.KEYDOWN:
                                        if evento.key == K_SPACE:
                                            s = 1
                                            sair = 1
                                    
                                
                        if d.rect.top > 410:
                            i.listaDisparo.remove(d)
                i.comportamento(tempo)
                i.colocar(tela)
        
        
        text2 = fonte_ganhou.render('Pontos:', 1, (255, 255, 255))
        text3 = fonte_ganhou.render(str(pontos), 1, (255, 255, 255))
        
        tela.blit(text2, (10, 30))
        tela.blit(text3, (100, 30))

            
        pygame.display.update()

invasaoEspaco()
