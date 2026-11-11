import pygame
import sys
from mapa_prototipo import Mapa
from saude_ import SistemaSaude
from combate import SistemaCombate

# 1. Configurações Iniciais
pygame.init()
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Prédio 2D - Combate, Mapa e Saúde Separados")
relogio = pygame.time.Clock()

# Instancia os módulos
mapa = Mapa()
saude = SistemaSaude(vida_maxima=100)
combate = SistemaCombate()

# Fundo
try:
    imagem_fundo = pygame.image.load("fundo.jpg").convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA_TELA, ALTURA_TELA))
    tem_imagem_fundo = True
except pygame.error:
    tem_imagem_fundo = False

# Jogador e Física
jogador_rect = pygame.Rect(mapa.pos_inicial_jogador[0], mapa.pos_inicial_jogador[1], 24, 30)
vel_x = 0
vel_y = 0
velocidade_movimento = 5
gravidade = 0.75
forca_pulo = -15.5
no_chao = False

coyote_timer = 0
buffer_pulo_timer = 0
COYOTE_MAX = 7
BUFFER_MAX = 7

def reiniciar_jogo():
    global vel_x, vel_y, no_chao
    jogador_rect.topleft = mapa.pos_inicial_jogador
    saude.reiniciar()
    combate.parar_defesa()
    vel_x = 0
    vel_y = 0
    no_chao = False

# Loop Principal
executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

        if evento.type == pygame.KEYDOWN:
            if not saude.esta_vivo():
                if evento.key == pygame.K_r:
                    reiniciar_jogo()
            else:
                # Pulo
                if evento.key == pygame.K_SPACE or evento.key == pygame.K_UP:
                    buffer_pulo_timer = BUFFER_MAX
                
                # Ataque (J ou Z)
                if evento.key == pygame.K_j or evento.key == pygame.K_z:
                    combate.tentar_atacar()

                # Defesa (K ou X)
                if evento.key == pygame.K_k or evento.key == pygame.K_x:
                    combate.iniciar_defesa()

        if evento.type == pygame.KEYUP:
            if saude.esta_vivo():
                if (evento.key == pygame.K_SPACE or evento.key == pygame.K_UP) and vel_y < -4:
                    vel_y = -4
                
                # Soltar defesa
                if evento.key == pygame.K_k or evento.key == pygame.K_x:
                    combate.parar_defesa()

    # Atualizações enquanto vivo
    if saude.esta_vivo():
        saude.atualizar()

        teclas = pygame.key.get_pressed()
        vel_x = 0
        
        # Personagem anda mais devagar se estiver defendendo
        vel_atual = velocidade_movimento * 0.4 if combate.defendendo else velocidade_movimento

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            vel_x = -vel_atual
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            vel_x = vel_atual

        # Atualiza a direção do golpe/escudo
        combate.atualizar_direcao(vel_x)
        combate.atualizar(jogador_rect)

        # Buffers de salto
        if no_chao:
            coyote_timer = COYOTE_MAX
        elif coyote_timer > 0:
            coyote_timer -= 1

        if buffer_pulo_timer > 0:
            buffer_pulo_timer -= 1

        if buffer_pulo_timer > 0 and coyote_timer > 0:
            vel_y = forca_pulo
            coyote_timer = 0
            buffer_pulo_timer = 0
            no_chao = False

        # Gravidade
        vel_y += gravidade
        if vel_y > 15:
            vel_y = 15

        # Colisão Eixo X
        jogador_rect.x += vel_x
        for bloco in mapa.blocos:
            if jogador_rect.colliderect(bloco):
                if vel_x > 0:
                    jogador_rect.right = bloco.left
                elif vel_x < 0:
                    jogador_rect.left = bloco.right

        # Colisão Eixo Y
        jogador_rect.y += int(vel_y)
        no_chao = False
        for bloco in mapa.blocos:
            if jogador_rect.colliderect(bloco):
                if vel_y > 0:
                    jogador_rect.bottom = bloco.top
                    vel_y = 0
                    no_chao = True
                elif vel_y < 0:
                    jogador_rect.top = bloco.bottom
                    vel_y = 0

        # Dano com mitigação pelo escudo
        for espinho in mapa.espinhos:
            if jogador_rect.colliderect(espinho):
                dano_calculado = combate.calcular_dano_recebido(25)
                if saude.tomar_dano(dano_calculado):
                    vel_y = -7  # Pequeno recuo
                break

        # Coleta de kits médicos
        for kit in mapa.kits_medicos[:]:
            if jogador_rect.colliderect(kit):
                if saude.curar(25):
                    mapa.kits_medicos.remove(kit)

        # Coleta de moedas
        for moeda in mapa.moedas[:]:
            if jogador_rect.colliderect(moeda):
                mapa.moedas.remove(moeda)

    # Câmera
    camera_x = jogador_rect.centerx - LARGURA_TELA // 2
    camera_y = jogador_rect.centery - ALTURA_TELA // 2
    camera_x = max(0, min(camera_x, mapa.largura - LARGURA_TELA))
    camera_y = max(0, min(camera_y, mapa.altura - ALTURA_TELA))

    # Renderização de fundo
    if tem_imagem_fundo:
        fx = int(-camera_x * 0.25) % LARGURA_TELA
        fy = int(-camera_y * 0.25) % ALTURA_TELA
        tela.blit(imagem_fundo, (fx - LARGURA_TELA, fy - ALTURA_TELA))
        tela.blit(imagem_fundo, (fx, fy - ALTURA_TELA))
        tela.blit(imagem_fundo, (fx - LARGURA_TELA, fy))
        tela.blit(imagem_fundo, (fx, fy))
    else:
        tela.fill((30, 32, 40))

    # Desenho do mapa
    mapa.desenhar(tela, camera_x, camera_y, LARGURA_TELA, ALTURA_TELA)

    # Desenho do Jogador
    if saude.esta_vivo() and saude.deve_desenhar_jogador():
        jt = pygame.Rect(jogador_rect.x - camera_x, jogador_rect.y - camera_y, jogador_rect.width, jogador_rect.height)
        pygame.draw.rect(tela, (220, 50, 50), jt)
        
        # Desenha a espada/hitbox e o escudo por cima do jogador
        combate.desenhar(tela, camera_x, camera_y, jogador_rect)

    # HUD e Game Over
    saude.desenhar_hud(tela)
    if not saude.esta_vivo():
        saude.desenhar_game_over(tela, LARGURA_TELA, ALTURA_TELA)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()