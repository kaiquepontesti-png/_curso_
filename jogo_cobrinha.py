import tkinter as tk
import random

# --- CONFIGURAÇÕES DA GRADE DO JOGO ---
LARGURA = 600
ALTURA = 600
TAMANHO_BLOCO = 20

# --- VARIÁVEIS DE CONTROLE DO JOGO ---
jogo_ativo = False
jogo_pausado = False
id_loop_jogo = None  
frame_pause = None

# --- ESTADO INICIAL DA COBRINHA ---
cobra = []
direcao = 'Right'
direcao_pendente = None
comida = [200, 200]

def gerar_comida():
    """Gera uma posição aleatória alinhada à grade para a comida, fora do corpo da cobra."""
    while True:
        x = random.randint(0, (LARGURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
        y = random.randint(0, (ALTURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
        posicao = [x, y]
        if posicao not in cobra:
            return posicao

def iniciar_jogo():
    global jogo_ativo, jogo_pausado, cobra, direcao, direcao_pendente, comida
    
    # Esconde o menu principal completamente
    menu.place_forget()  
    
    # Reseta o estado da cobrinha
    cobra = [[100, 100], [80, 100], [60, 100]]
    direcao = 'Right'
    direcao_pendente = None
    comida = gerar_comida()
    
    jogo_ativo = True
    jogo_pausado = False
    
    # Limpa desenhos anteriores do Canvas
    cana.delete("all")
    
    # Inicia o motor do jogo
    loop_principal_jogo()

def loop_principal_jogo():
    global id_loop_jogo, comida, jogo_ativo, direcao, direcao_pendente

    if jogo_ativo and not jogo_pausado:
        # Garante que só uma mudança de direção válida entra em vigor por tick.
        if direcao_pendente is not None:
            opostos = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
            if direcao_pendente != opostos.get(direcao):
                direcao = direcao_pendente
            direcao_pendente = None

        # 1. Calcula a nova posição da cabeça
        cabeca_x, cabeca_y = cobra[0]
        if direcao == 'Up': 
            cabeca_y -= TAMANHO_BLOCO
        elif direcao == 'Down': 
            cabeca_y += TAMANHO_BLOCO
        elif direcao == 'Left': 
            cabeca_x -= TAMANHO_BLOCO
        elif direcao == 'Right': 
            cabeca_x += TAMANHO_BLOCO

        nova_cabeca = [cabeca_x, cabeca_y]

        # 2. Verificação de Fim de Jogo: Colisão com as paredes ou com o próprio corpo
        if (cabeca_x < 0 or cabeca_x >= LARGURA or 
            cabeca_y < 0 or cabeca_y >= ALTURA or 
            nova_cabeca in cobra):
            
            jogo_ativo = False
            cana.create_text(
                200, 150, 
                text="FIM DE JOGO", 
                fill="white", 
                font=("Arial", 24, "bold")
            )
            # Cria um botão de voltar para o menu na tela de Game Over
            global btn_voltar_gameover
            btn_voltar_gameover = tk.Button(jogo, text="Voltar ao Menu", font=("Arial", 12), command=voltar_ao_menu)
            btn_voltar_gameover.place(relx=0.5, rely=0.6, anchor="center")
            return

        # 3. Adiciona a nova cabeça na frente da cobra
        cobra.insert(0, nova_cabeca)

        # 4. Lógica da comida e do crescimento
        if nova_cabeca == comida:
            comida = gerar_comida()
        else:
            cobra.pop()

        # 5. Redesenha a tela
        cana.delete("all")
        
        # Desenha a comida
        cana.create_rectangle(
            comida[0], comida[1], 
            comida[0] + TAMANHO_BLOCO, comida[1] + TAMANHO_BLOCO, 
            fill="blue", outline="black"
        )
        
        # Desenha a cobra
        for x, y in cobra:
            cana.create_rectangle(
                x, y, 
                x + TAMANHO_BLOCO, y + TAMANHO_BLOCO, 
                fill="green", outline="black"
            )

        # 6. Agenda o próximo ciclo (velocidade da cobra)
        id_loop_jogo = jogo.after(180, loop_principal_jogo)

# --- FUNÇÃO PARA GERENCIAR O PAUSE E O TECLADO ---
def gerenciar_teclado(event):
    global jogo_ativo, jogo_pausado, frame_pause, direcao, direcao_pendente
    
    # Se apertar as setas direcionais e o jogo estiver rodando ativamente
    if jogo_ativo and not jogo_pausado:
        nova_direcao = event.keysym
        opostos = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        if nova_direcao in opostos:
            # Armazena a próxima direção válida e ignora reversões imediatas.
            # Isso evita que múltiplas teclas apertadas quase ao mesmo tempo
            # mudem a cobra para uma direção impossível no próximo frame.
            if nova_direcao == opostos.get(direcao):
                return
            if direcao_pendente is not None and nova_direcao == opostos.get(direcao_pendente):
                return
            direcao_pendente = nova_direcao
            return  # Sai da função para não acionar o sistema de pause pelas setas

    # Se o jogo não está ativo (Menu ou Game Over), ignora os comandos de pausa
    if not jogo_ativo:
        return

    # Tecla P -> Pausa o jogo
    if (event.keysym in ['p', 'P']) and not jogo_pausado:
        jogo_pausado = True
        
        # Para o motor do jogo imediatamente
        if id_loop_jogo:
            jogo.after_cancel(id_loop_jogo)
        
        # Cria o Frame de Pause centralizado na tela
        frame_pause = tk.Frame(jogo, bg="#dcdcdc", bd=3, relief="solid")
        frame_pause.place(relx=0.5, rely=0.5, anchor="center")
        
        lbl_pause = tk.Label(frame_pause, text="JOGO PAUSADO", font=("Arial", 20, "bold"), bg="#dcdcdc")
        lbl_pause.pack(pady=10, padx=20)
        
        lbl_instrucao = tk.Label(frame_pause, text="Aperte ESPAÇO para despausar", font=("Arial", 11, "italic"), bg="#dcdcdc")
        lbl_instrucao.pack(pady=5, padx=20)
        
        btn_retornar = tk.Button(frame_pause, text="Retornar ao Menu", font=("Arial", 11), command=voltar_ao_menu)
        btn_retornar.pack(pady=15)

    # Tecla Espaço -> Despausa o jogo
    elif event.keysym == 'space' and jogo_pausado:
        jogo_pausado = False
        
        if frame_pause:
            frame_pause.destroy()
            frame_pause = None
            
        loop_principal_jogo()

def voltar_ao_menu():
    global jogo_ativo, jogo_pausado, frame_pause, direcao_pendente
    jogo_ativo = False
    jogo_pausado = False
    direcao_pendente = None
    
    # Cancela qualquer timer ativo do jogo
    if id_loop_jogo:
        jogo.after_cancel(id_loop_jogo)
        
    # Remove a caixinha de pause se ela existir
    if frame_pause:
        frame_pause.destroy()
        frame_pause = None
        
    # Remove o botão de voltar do Game Over se ele existir na tela
    if 'btn_voltar_gameover' in globals():
        try:
            btn_voltar_gameover.destroy()
        except:
            pass
        
    cana.delete("all")  # Limpa o Canvas
    menu.place(x=0, y=0)  # Traz o menu principal de volta para a tela

def sair_jogo():
    jogo.destroy()

# --- CONFIGURAÇÃO DA JANELA PRINCIPAL ---
jogo = tk.Tk()
jogo.title("Jogo da Cobrinha Definitivo")
jogo.geometry(f"{LARGURA}x{ALTURA}")

# 1. CANVAS DO JOGO
cana = tk.Canvas(jogo, width=LARGURA, height=ALTURA, bg="black", highlightthickness=0)
cana.pack(fill="both", expand=True)

# 2. FRAME DO MENU PRINCIPAL
menu = tk.Frame(jogo, width=LARGURA, height=ALTURA, bg="#f0f0f0")
menu.place(x=0, y=0)

titulo = tk.Label(menu, text="SNAKE GAME", font=("Arial", 24, "bold"), bg="#f0f0f0")
titulo.place(relx=0.5, rely=0.3, anchor="center")

btn_iniciar = tk.Button(menu, text="Iniciar Jogo", font=("Arial", 14), width=15, command=iniciar_jogo)
btn_iniciar.place(relx=0.5, rely=0.5, anchor="center")

btn_sair = tk.Button(menu, text="Sair", font=("Arial", 14), width=15, command=sair_jogo)
btn_sair.place(relx=0.5, rely=0.65, anchor="center")

jogo.bind("<KeyPress>", gerenciar_teclado)

jogo.mainloop()