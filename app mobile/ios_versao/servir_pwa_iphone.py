import functools
import http.server
import socket
import socketserver
from pathlib import Path


def obter_ip_local() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def main() -> None:
    pasta_pwa = Path(__file__).resolve().parent / "app_pwa"
    if not (pasta_pwa / "index.html").exists():
        raise SystemExit("Pasta app_pwa não encontrada. Execute primeiro: python gerar_versao_ios.py")

    porta = 8080
    ip = obter_ip_local()
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(pasta_pwa))

    print("=" * 60)
    print("NumEsquece Lista · Instalador Local para iPhone (Safari PWA)")
    print("=" * 60)
    print(f"1. Conecte o iPhone na mesma rede Wi-Fi deste computador.")
    print(f"2. Abra o Safari no iPhone e acesse: http://{ip}:{porta}")
    print(f"3. Toque em Compartilhar (ícone seta para cima) -> 'Adicionar à Tela de Início'.")
    print("Dica: para cache 100% offline via Service Worker (Modo Avião),")
    print("hospede a pasta app_pwa/ em HTTPS (ex: GitHub Pages, Netlify ou Cloudflare).")
    print("Pressione Ctrl+C para encerrar.")
    print("=" * 60)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", porta), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")


if __name__ == "__main__":
    main()
