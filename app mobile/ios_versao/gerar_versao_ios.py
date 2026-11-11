import json
import os
import struct
import sys
import zlib
from pathlib import Path

PASTA_IOS = Path(__file__).resolve().parent
PASTA_RAIZ = PASTA_IOS.parent
if str(PASTA_RAIZ) not in sys.path:
    sys.path.insert(0, str(PASTA_RAIZ))

from mobile_app.ui_builder import gerar_html_mobile


def _png_chunk(tag: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(tag + data) & 0xFFFFFFFF
    return struct.pack("!I", len(data)) + tag + data + struct.pack("!I", crc)


def gerar_icone_neobrutalist_png(caminho_saida: Path, tamanho: int) -> None:
    """
    Gera um ícone PNG RGB opaco (sem canal alfa, exigido pela Apple para AppIcon iOS)
    no estilo Monocromático Clássico & Minimalista de Alto Contraste.
    """
    largura = tamanho
    altura = tamanho
    linhas_raw = bytearray()

    # Coordenadas normalizadas [0.0 .. 1.0] para desenhar bloco de notas / checklist
    borda_ext = 0.09
    card_l, card_t, card_r, card_b = 0.20, 0.17, 0.78, 0.81
    sombra_dx, sombra_dy = 0.045, 0.045
    esp = 0.045

    for y in range(altura):
        linhas_raw.append(0)  # filtro None
        ny = y / altura
        for x in range(largura):
            nx = x / largura

            # Sombra seca deslocada preta
            na_sombra = (
                (card_l + sombra_dx) <= nx <= (card_r + sombra_dx)
                and (card_t + sombra_dy) <= ny <= (card_b + sombra_dy)
            )
            # Card principal branco com borda preta grossa
            no_card_ext = card_l <= nx <= card_r and card_t <= ny <= card_b
            no_card_int = (
                (card_l + esp) <= nx <= (card_r - esp)
                and (card_t + esp) <= ny <= (card_b - esp)
            )

            # Cabeçalho preto no topo do bloco
            no_topo_bloco = (
                (card_l + esp) <= nx <= (card_r - esp)
                and (card_t + esp) <= ny <= (card_t + esp + 0.09)
            )

            # 3 linhas de checklist (caixinha + traço)
            em_item = False
            for row_y in (0.41, 0.55, 0.69):
                # Caixinha preenchida preta
                if 0.30 <= nx <= 0.37 and (row_y - 0.032) <= ny <= (row_y + 0.032):
                    em_item = True
                    break
                # Traço horizontal da linha
                if 0.42 <= nx <= 0.68 and (row_y - 0.018) <= ny <= (row_y + 0.018):
                    em_item = True
                    break

            # Borda externa sutil caso desejado? Deixar fundo branco sólido p/ ícone iOS limpo
            _ = borda_ext

            preto = False
            if no_card_ext:
                if not no_card_int or no_topo_bloco or em_item:
                    preto = True
                else:
                    preto = False
            elif na_sombra:
                preto = True

            if preto:
                linhas_raw.extend((0, 0, 0))
            else:
                linhas_raw.extend((255, 255, 255))

    ihdr = struct.pack("!IIBBBBB", largura, altura, 8, 2, 0, 0, 0)
    idat = zlib.compress(bytes(linhas_raw), level=6)

    png_bytes = (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", ihdr)
        + _png_chunk(b"IDAT", idat)
        + _png_chunk(b"IEND", b"")
    )
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    caminho_saida.write_bytes(png_bytes)


def gerar_versao_ios() -> None:
    caminho_bg = PASTA_RAIZ / "assets" / "bg-doodle.jpg"
    if not caminho_bg.exists():
        raise FileNotFoundError(f"Imagem de fundo não encontrada: {caminho_bg}")

    # 1. Gerar versão PWA iOS (instalável pelo Safari em Adicionar à Tela de Início)
    pasta_pwa = PASTA_IOS / "app_pwa"
    pasta_pwa.mkdir(parents=True, exist_ok=True)

    html_pwa = gerar_html_mobile(str(caminho_bg), plataforma="ios", modo_pwa=True)
    (pasta_pwa / "index.html").write_text(html_pwa, encoding="utf-8")

    manifest = {
        "name": "NumEsquece Lista",
        "short_name": "NumEsquece",
        "description": "Listas de compras offline com memória local para iOS.",
        "start_url": "./index.html",
        "scope": "./",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#FFFFFF",
        "theme_color": "#FFFFFF",
        "icons": [
            {"src": "icon-180.png", "sizes": "180x180", "type": "image/png"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ],
    }
    (pasta_pwa / "manifest.webmanifest").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    sw_js = """const CACHE_NAME = 'numesquece-ios-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon-180.png',
  './icon-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request).catch(() => caches.match('./index.html')))
  );
});
"""
    (pasta_pwa / "sw.js").write_text(sw_js, encoding="utf-8")

    gerar_icone_neobrutalist_png(pasta_pwa / "icon-180.png", 180)
    gerar_icone_neobrutalist_png(pasta_pwa / "icon-512.png", 512)

    # 2. Atualizar bundle offline e AppIcon do projeto nativo Xcode/Swift (.ipa)
    pasta_nativa = PASTA_IOS / "projeto_nativo_ipa"
    html_nativo = gerar_html_mobile(str(caminho_bg), plataforma="ios", modo_pwa=False)
    (pasta_nativa / "Resources").mkdir(parents=True, exist_ok=True)
    (pasta_nativa / "Resources" / "index.html").write_text(html_nativo, encoding="utf-8")

    iconset_dir = pasta_nativa / "Assets.xcassets" / "AppIcon.appiconset"
    gerar_icone_neobrutalist_png(iconset_dir / "icon-1024.png", 1024)

    print("✓ Versão iOS gerada com sucesso em:")
    print(f"  - PWA iOS: {pasta_pwa}")
    print(f"  - Projeto Nativo IPA: {pasta_nativa}")


if __name__ == "__main__":
    gerar_versao_ios()
