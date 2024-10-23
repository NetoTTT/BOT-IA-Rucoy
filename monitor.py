import json
import pygetwindow as gw
import cv2
import numpy as np
from PIL import ImageGrab
import subprocess  # Importar subprocess para executar outro script
import os  # Importar os para encerrar o processo
import sys  # Importar sys para encerramento mais suave
import keyboard  # Biblioteca para detectar pressionamento de teclas
from ultralytics import YOLO
from collections import defaultdict

# Função para ler os dados da janela do arquivo .json
def carregar_dados_janela():
    with open("janela_selecionada.json", "r") as arquivo_json:
        dados_janela = json.load(arquivo_json)
    return dados_janela

# Função para capturar a tela da janela selecionada
def capturar_tela_janela(janela):
    left = janela['left']
    top = janela['top']
    width = janela['width']
    height = janela['height']
    
    # Captura a área da janela selecionada usando PIL (ImageGrab)
    img = ImageGrab.grab(bbox=(left, top, left + width, top + height))
    
    # Converte a imagem para o formato OpenCV (numpy array)
    img_np = np.array(img)
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    
    return img_cv

# Função para capturar e salvar com nomes numerados
def salvar_captura_numerada(tela):
    # Criar a pasta 'imgLabel' se não existir
    if not os.path.exists('imgLabel'):
        os.makedirs('imgLabel')

    # Verificar quantos arquivos já existem na pasta 'imgLabel'
    arquivos_existentes = os.listdir('imgLabel')

    # Filtrar para pegar apenas arquivos PNG
    arquivos_png = [f for f in arquivos_existentes if f.endswith('.png')]

    # Obter o próximo número para o arquivo
    proximo_numero = len(arquivos_png) + 1

    # Gerar o nome do arquivo baseado no número
    nome_arquivo = f'imgLabel/{proximo_numero}.png'

    # Salvar a captura com o nome gerado
    cv2.imwrite(nome_arquivo, tela)
    print(f"Captura salva como '{nome_arquivo}'.")

# Carregar dados da janela
janela_selecionada = carregar_dados_janela()

# Inicializar o modelo YOLO
model = YOLO("best.pt")  # ou o caminho para seu modelo treinado
track_history = defaultdict(lambda: [])
seguir = True
deixar_rastro = False

# Loop principal para capturar e exibir a tela
while True:
    # Captura a tela da janela
    tela = capturar_tela_janela(janela_selecionada)

    # Se 'seguir' for True, usa o rastreamento do modelo
    if seguir:
        results = model.track(tela, persist=True)
    else:
        results = model(tela)

    # Processar os resultados do modelo
    for result in results:
        # Visualiza os resultados no quadro
        tela = result.plot()

        if seguir and deixar_rastro:
            try:
                # Obtém as caixas e IDs de rastreamento
                boxes = result.boxes.xywh.cpu()
                track_ids = result.boxes.id.int().cpu().tolist()

                # Plotar as trilhas
                for box, track_id in zip(boxes, track_ids):
                    x, y, w, h = box
                    track = track_history[track_id]
                    track.append((float(x), float(y)))  # ponto central x, y
                    if len(track) > 30:  # manter 90 rastros para 90 quadros
                        track.pop(0)

                    # Desenhar as linhas de rastreamento
                    points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                    cv2.polylines(tela, [points], isClosed=False, color=(230, 0, 0), thickness=5)
            except:
                pass

    # Exibir a imagem capturada em uma janela OpenCV
    cv2.imshow("Captura da Janela", tela)

    # Verificar a tecla pressionada
    key = cv2.waitKey(1) & 0xFF

    # Pressione 'q' para sair do loop
    if key == ord('q'):
        break
    
    # Pressione 't' para abrir o chooseScreen.py
    if key == ord('t'):
        # Inicia o script chooseScreen.py
        subprocess.Popen(['python', 'chooseScreen.py'])
        # Aguarda um segundo para garantir que o script seja iniciado
        cv2.destroyAllWindows()
        sys.exit()

    # Pressione 'c' para capturar a tela e salvar com nome numerado
    if key == ord('c'):
        salvar_captura_numerada(tela)  # Salvar a captura com nome numerado

# Libera a janela OpenCV
cv2.destroyAllWindows()
print("desligando")
