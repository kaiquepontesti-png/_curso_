import pygame

TILE_SIZE = 32

DADOS_MAPA = [
    # Topo / Terraço
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X           M                          M                             M         X",
    "X       XXXXXXXXX                  XXXXXXXXX                     XXXXXXXXX     X",
    "X                                                                              X",
    "X  P M             M            M             M               M             M  X",
    "XXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXX   XXXXXXXXXXXXX",
    "X                       X                              X                       X",
    "X       XXXXX           X           XXXXX              X           XXXXX       X",
    "X                       X                              X                       X",
    "X               XXXXX   X      M               XXXXX   X   M           XXXXX   X",
    "X                       X   XXXXXXXX                   X XXXXX                 X",
    "XXXXX   XXXXXXXXXXXXXXXXX               XXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXX",
    "X                       X                              X                       X",
    "X          M            X              M               X              M        X",
    "X       XXXXXXX         X           XXXXXXX            X           XXXXXXX     X",
    "X                       X                              X                       X",
    "X   XXXXX               X      XXXXX                   X      XXXXX            X",
    "XXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXX",
    "X                       X                              X                       X",
    "X              M        X              M               X              M        X",
    "X           XXXXX       X           XXXXX              X           XXXXX       X",
    "X                       X                              X                       X",
    "X    XXXXX      SSSS    X      XXXXX                   X      XXXXX            X",
    "XXXXX   XXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXX",
    "X                       X                              X                       X",
    "X         M             X              M               X              M        X",
    "X      XXXXXX           X           XXXXXX             X           XXXXXX      X",
    "X                       X                              X                       X",
    "X              XXXXX    X              XXXXX           X              XXXXX    X",
    "XXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXX",
    "X                       X                              X                       X",
    "X   XXXXX               X      XXXXX        H          X      XXXXX            X",
    "X               M       X              M   XXXX        X              M        X",
    "X            XXXXXX     X           XXXXXX             X           XXXXXX      X",
    "X                       X                              X                       X",
    "XXXXX   XXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXX",
    "X                       X                              X                       X",
    "X          M            X              M               X              M        X",
    "X       XXXXX           X           XXXXX              X           XXXXX       X",
    "X                       X                              X                       X",
    "X   XXXX       SSSSS    X      XXXX                    X      XXXX             X",
    "XXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXX",
    "X                       X                              X                       X",
    "X               M       X              M               X              M        X",
    "X            XXXXX      X           XXXXX              X           XXXXX       X",
    "X                       X                              X                       X",
    "X    XXXXX              X      XXXXX                   X      XXXXX            X",
    "XXXXX   XXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXX",
    "X                       X                              X                       X",
    "X          M            X              M               X              M        X",
    "X       XXXXXX          X           XXXXXX             X           XXXXXX      X",
    "X                       X                              X                       X",
    "X              XXXXX    X              XXXXX           X              XXXXX    X",
    "XXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXX",
    "X                       X                              X                       X",
    "X   XXXXX               X      XXXXX                   X      XXXXX            X",
    "X               M       X              M               X              M        X",
    "X            XXXXX      X           XXXXX              X           XXXXX       X",
    "X                       X                              X                       X",
    "XXXXX   XXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXX",
    "X                       X                              X                       X",
    "X          M            X              M               X              M        X",
    "X       XXXXXX  SSSS    X           XXXXXX     H       X           XXXXXX      X",
    "X                       X                     XXXX     X                       X",
    "X                       X                              X                       X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

class Mapa:
    def __init__(self):
        self.tile_size = TILE_SIZE
        self.largura = len(DADOS_MAPA[0]) * self.tile_size
        self.altura = len(DADOS_MAPA) * self.tile_size

        self.blocos = []
        self.espinhos = []
        self.moedas = []
        self.kits_medicos = []
        self.pos_inicial_jogador = (64, 128)

        self._processar_dados()

    def _processar_dados(self):
        for linha_idx, linha in enumerate(DADOS_MAPA):
            for col_idx, caractere in enumerate(linha):
                pos_x = col_idx * self.tile_size
                pos_y = linha_idx * self.tile_size

                if caractere == "X":
                    self.blocos.append(pygame.Rect(pos_x, pos_y, self.tile_size, self.tile_size))
                elif caractere == "P":
                    self.pos_inicial_jogador = (pos_x, pos_y)
                elif caractere == "M":
                    self.moedas.append(pygame.Rect(pos_x + 8, pos_y + 8, 16, 16))
                elif caractere == "S":
                    self.espinhos.append(pygame.Rect(pos_x, pos_y + 16, self.tile_size, 16))
                elif caractere == "H":
                    self.kits_medicos.append(pygame.Rect(pos_x + 6, pos_y + 6, 20, 20))

    def desenhar(self, tela, camera_x, camera_y, largura_tela, altura_tela):
        # Blocos
        for bloco in self.blocos:
            bx = bloco.x - camera_x
            by = bloco.y - camera_y
            if -self.tile_size < bx < largura_tela and -self.tile_size < by < altura_tela:
                pygame.draw.rect(tela, (65, 70, 80), (bx, by, bloco.width, bloco.height))
                pygame.draw.rect(tela, (115, 125, 135), (bx, by, self.tile_size, 4))

        # Espinhos
        for esp in self.espinhos:
            ex = esp.x - camera_x
            ey = esp.y - camera_y
            if -self.tile_size < ex < largura_tela and -self.tile_size < ey < altura_tela:
                pontos = [(ex, ey + 16), (ex + 16, ey), (ex + 32, ey + 16)]
                pygame.draw.polygon(tela, (180, 50, 50), pontos)
                pygame.draw.polygon(tela, (230, 90, 90), pontos, 2)

        # Kits Médicos
        for kit in self.kits_medicos:
            kx = kit.x - camera_x
            ky = kit.y - camera_y
            if -32 < kx < largura_tela and -32 < ky < altura_tela:
                pygame.draw.rect(tela, (240, 240, 240), (kx, ky, 20, 20), border_radius=3)
                pygame.draw.rect(tela, (46, 204, 113), (kx + 8, ky + 3, 4, 14))
                pygame.draw.rect(tela, (46, 204, 113), (kx + 3, ky + 8, 14, 4))

        # Moedas
        for moeda in self.moedas:
            cx = moeda.centerx - camera_x
            cy = moeda.centery - camera_y
            if -16 < cx < largura_tela + 16 and -16 < cy < altura_tela + 16:
                pygame.draw.circle(tela, (255, 215, 0), (cx, cy), 8)