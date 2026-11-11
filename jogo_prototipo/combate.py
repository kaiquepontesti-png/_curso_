import pygame

class SistemaCombate:
    def __init__(self):
        # Direção: 1 = Direita, -1 = Esquerda
        self.direcao = 1
        
        # Estados
        self.atacando = False
        self.defendendo = False
        
        # Temporizadores de Ataque (em frames a 60 FPS)
        self.duracao_ataque = 12       # Tempo que a hitbox de ataque fica ativa (0.2s)
        self.cooldown_ataque = 25      # Intervalo mínimo entre ataques
        self.timer_ataque = 0
        self.timer_cooldown = 0
        
        # Dimensões da Hitbox de ataque
        self.alcance_ataque = 30
        self.altura_ataque = 20
        self.hitbox_ataque = None
        
        # Dano
        self.dano_ataque = 35
        self.reducao_defesa = 0.8      # 80% de redução de dano ao defender (0.0 = anula 100%)

    def atualizar_direcao(self, vel_x):
        """Atualiza o lado para onde o personagem está virado."""
        if vel_x > 0:
            self.direcao = 1
        elif vel_x < 0:
            self.direcao = -1

    def tentar_atacar(self):
        """Dispara o ataque se não estiver em cooldown nem defendendo."""
        if self.timer_cooldown <= 0 and not self.defendendo:
            self.atacando = True
            self.timer_ataque = self.duracao_ataque
            self.timer_cooldown = self.cooldown_ataque
            return True
        return False

    def iniciar_defesa(self):
        """Ativa o escudo (cancela o ataque se estiver atacando)."""
        if not self.atacando:
            self.defendendo = True

    def parar_defesa(self):
        """Desativa o escudo."""
        self.defendendo = False

    def atualizar(self, jogador_rect):
        """Atualiza a posição da hitbox de ataque e os contadores de tempo."""
        # Gerencia temporizadores
        if self.timer_ataque > 0:
            self.timer_ataque -= 1
            if self.timer_ataque <= 0:
                self.atacando = False
                self.hitbox_ataque = None

        if self.timer_cooldown > 0:
            self.timer_cooldown -= 1

        # Projeta a Hitbox de ataque à frente do jogador
        if self.atacando:
            if self.direcao == 1:
                # À direita do jogador
                x = jogador_rect.right
            else:
                # À esquerda do jogador
                x = jogador_rect.left - self.alcance_ataque
            
            y = jogador_rect.centery - (self.altura_ataque // 2)
            self.hitbox_ataque = pygame.Rect(x, y, self.alcance_ataque, self.altura_ataque)
        else:
            self.hitbox_ataque = None

    def calcular_dano_recebido(self, dano_base):
        """Calcula o dano final considerando se está com o escudo levantado."""
        if self.defendendo:
            dano_final = dano_base * (1.0 - self.reducao_defesa)
            return int(dano_final)
        return dano_base

    def desenhar(self, tela, camera_x, camera_y, jogador_rect):
        """Desenha visualmente o efeito do ataque e do escudo."""
        # Desenha a Hitbox de ataque (um corte laranja translúcido)
        if self.hitbox_ataque is not None:
            hx = self.hitbox_ataque.x - camera_x
            hy = self.hitbox_ataque.y - camera_y
            
            superficie_ataque = pygame.Surface((self.hitbox_ataque.width, self.hitbox_ataque.height), pygame.SRCALPHA)
            superficie_ataque.fill((255, 140, 0, 180))  # Laranja
            tela.blit(superficie_ataque, (hx, hy))
            pygame.draw.rect(tela, (255, 200, 50), (hx, hy, self.hitbox_ataque.width, self.hitbox_ataque.height), 2)

        # Desenha o escudo à frente do jogador se estiver defendendo
        if self.defendendo:
            jx = jogador_rect.x - camera_x
            jy = jogador_rect.y - camera_y

            # Posiciona o escudo no lado que o jogador está virado
            if self.direcao == 1:
                escudo_rect = pygame.Rect(jx + jogador_rect.width, jy + 2, 6, jogador_rect.height - 4)
            else:
                escudo_rect = pygame.Rect(jx - 6, jy + 2, 6, jogador_rect.height - 4)

            pygame.draw.rect(tela, (0, 191, 255), escudo_rect, border_radius=2)      # Azul ciano
            pygame.draw.rect(tela, (255, 255, 255), escudo_rect, 1, border_radius=2) # Brilho branco