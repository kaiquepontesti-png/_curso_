import pygame

class SistemaSaude:
    def __init__(self, vida_maxima=100, tempo_imunidade_max=60):
        self.vida_maxima = vida_maxima
        self.vida_atual = vida_maxima
        self.tempo_invencivel = 0
        self.tempo_imunidade_max = tempo_imunidade_max

        # Fontes do HUD
        self.fonte_hud = pygame.font.SysFont("Arial", 16, bold=True)
        self.fonte_game_over = pygame.font.SysFont("Arial", 48, bold=True)
        self.fonte_sub = pygame.font.SysFont("Arial", 22)

    def tomar_dano(self, quantidade=25):
        """Aplica dano caso o jogador não esteja no período de invulnerabilidade."""
        if self.tempo_invencivel <= 0 and self.vida_atual > 0:
            self.vida_atual = max(0, self.vida_atual - quantidade)
            self.tempo_invencivel = self.tempo_imunidade_max
            return True  # Sofreu dano (útil para aplicar recuo)
        return False

    def curar(self, quantidade=25):
        """Restaura vida até o limite máximo."""
        if self.vida_atual > 0 and self.vida_atual < self.vida_maxima:
            self.vida_atual = min(self.vida_maxima, self.vida_atual + quantidade)
            return True
        return False

    def atualizar(self):
        """Atualiza a contagem dos frames de invulnerabilidade."""
        if self.tempo_invencivel > 0:
            self.tempo_invencivel -= 1

    def esta_vivo(self):
        return self.vida_atual > 0

    def deve_desenhar_jogador(self):
        """Efeito de piscar durante a imunidade."""
        if self.tempo_invencivel > 0 and (self.tempo_invencivel // 5) % 2 == 0:
            return False
        return True

    def reiniciar(self):
        self.vida_atual = self.vida_maxima
        self.tempo_invencivel = 0

    def desenhar_hud(self, tela):
        """Desenha a barra de vida fixa na tela."""
        largura_barra = 200
        altura_barra = 22
        proporcao = int((self.vida_atual / self.vida_maxima) * largura_barra)

        # Cor dinâmica: verde, amarelo ou vermelho
        if self.vida_atual > 50:
            cor_vida = (46, 204, 113)
        elif self.vida_atual > 25:
            cor_vida = (241, 196, 15)
        else:
            cor_vida = (231, 76, 60)

        # Fundo, barra preenchida e contorno
        pygame.draw.rect(tela, (40, 40, 40), (20, 20, largura_barra, altura_barra))
        pygame.draw.rect(tela, cor_vida, (20, 20, proporcao, altura_barra))
        pygame.draw.rect(tela, (255, 255, 255), (20, 20, largura_barra, altura_barra), 2)

        texto = self.fonte_hud.render(f"Sede: {self.vida_atual}/{self.vida_maxima}", True, (255, 255, 255))
        tela.blit(texto, (25, 23))

    def desenhar_game_over(self, tela, largura_tela, altura_tela):
        """Desenha tela translúcida de Game Over com aviso de reinício."""
        overlay = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        tela.blit(overlay, (0, 0))

        txt_go = self.fonte_game_over.render("GAME OVER", True, (231, 76, 60))
        txt_rst = self.fonte_sub.render("Pressione 'R' para Renascer", True, (255, 255, 255))

        rect_go = txt_go.get_rect(center=(largura_tela // 2, altura_tela // 2 - 25))
        rect_rst = txt_rst.get_rect(center=(largura_tela // 2, altura_tela // 2 + 30))

        tela.blit(txt_go, rect_go)
        tela.blit(txt_rst, rect_rst)