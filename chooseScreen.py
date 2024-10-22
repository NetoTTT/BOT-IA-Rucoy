import tkinter as tk
from tkinter import ttk, messagebox
import pygetwindow as gw
import json
import time
import subprocess
import os
from PIL import ImageGrab

# Função para capturar a janela selecionada e salvar seus dados em um arquivo json
def selecionar_janela():
    janela_selecionada = combo_janelas.get()
    if janela_selecionada:
        # Fechar a janela de seleção
        root.destroy()

        # Traz a janela selecionada para o primeiro plano
        window = gw.getWindowsWithTitle(janela_selecionada)[0]
        window.activate()

        # Espera um pouco para a janela ser ativada
        time.sleep(0.5)

        # Salvar os dados da janela em um arquivo JSON
        dados_janela = {
            "left": window.left,
            "top": window.top,
            "width": window.width,
            "height": window.height,
            "title": window.title
        }
        with open("janela_selecionada.json", "w") as arquivo_json:
            json.dump(dados_janela, arquivo_json, indent=4)

        # Executar o monitor.py após a seleção da janela
        iniciar_monitor()

        # Encerrar o script chooseScreen.py
        os._exit(0)

    else:
        messagebox.showwarning("Erro", "Por favor, selecione uma janela.")

# Função para iniciar o monitor.py
def iniciar_monitor():
    # Iniciar o script monitor.py e continuar a execução
    subprocess.Popen(['python', 'monitor.py'])

# Função para listar as janelas abertas
def listar_janelas():
    janelas = gw.getAllTitles()
    return [janela for janela in janelas if janela]  # Filtrar janelas com títulos

# Função para selecionar uma área personalizada da tela
def selecionar_area_personalizada():
    # Fechar a janela de seleção
    root.destroy()

    # Criar uma nova janela para a seleção da área personalizada
    area_selector = tk.Tk()
    area_selector.attributes("-fullscreen", True)  # Deixar a janela em tela cheia
    area_selector.attributes("-alpha", 0.3)  # Tornar a janela transparente
    canvas = tk.Canvas(area_selector, cursor="cross")
    canvas.pack(fill="both", expand=True)

    coords = {}

    def iniciar_selecao(event):
        coords['x_start'], coords['y_start'] = event.x, event.y
        coords['rect'] = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='red', width=2)

    def arrastar_selecao(event):
        canvas.coords(coords['rect'], coords['x_start'], coords['y_start'], event.x, event.y)

    def finalizar_selecao(event):
        coords['x_end'], coords['y_end'] = event.x, event.y
        area_selector.destroy()  # Fechar a janela de seleção

        # Capturar a área selecionada
        left = min(coords['x_start'], coords['x_end'])
        top = min(coords['y_start'], coords['y_end'])
        right = max(coords['x_start'], coords['x_end'])
        bottom = max(coords['y_start'], coords['y_end'])

        # Salvar os dados da área selecionada em um arquivo JSON
        dados_area = {
            "left": left,
            "top": top,
            "width": right - left,
            "height": bottom - top,
            "title": "Área Personalizada"
        }
        with open("janela_selecionada.json", "w") as arquivo_json:
            json.dump(dados_area, arquivo_json, indent=4)

        # Iniciar o monitor.py após a seleção
        iniciar_monitor()

    # Associar eventos do mouse
    canvas.bind("<ButtonPress-1>", iniciar_selecao)
    canvas.bind("<B1-Motion>", arrastar_selecao)
    canvas.bind("<ButtonRelease-1>", finalizar_selecao)

    # Iniciar a interface gráfica
    area_selector.mainloop()

# Configuração da interface gráfica para seleção
root = tk.Tk()
root.title("Selecionar Janela para o Bot")

# Label
label = tk.Label(root, text="Escolha a janela onde deseja rodar o bot ou selecione uma área personalizada:")
label.pack(pady=10)

# Combobox para listar as janelas
janelas_abertas = listar_janelas()
combo_janelas = ttk.Combobox(root, values=janelas_abertas)
combo_janelas.pack(pady=10)

# Botão para confirmar a seleção de uma janela
botao_confirmar = tk.Button(root, text="Confirmar Janela", command=selecionar_janela)
botao_confirmar.pack(pady=10)

# Botão para selecionar uma área personalizada
botao_personalizado = tk.Button(root, text="Selecionar Área Personalizada", command=selecionar_area_personalizada)
botao_personalizado.pack(pady=10)

# Inicia a interface gráfica
root.mainloop()
