from mobile_app.storage import ArmazenamentoLocal
from mobile_app.ui_desktop import NumEsqueceMobileApp


def main():
    armazenamento = ArmazenamentoLocal()
    aplicativo = NumEsqueceMobileApp(armazenamento=armazenamento)
    aplicativo.iniciar()


if __name__ == "__main__":
    main()
