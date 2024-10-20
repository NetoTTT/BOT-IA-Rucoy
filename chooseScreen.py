import tkinter as tk
from tkinter import ttk, messagebox
import pygetwindow as gw
import json
import time
import subprocess  # Importar subprocess para executar outro script
import os  # Importar os para encerrar o processo

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

# Configuração da interface gráfica para seleção
root = tk.Tk()
root.title("Selecionar Janela para o Bot")

# Label
label = tk.Label(root, text="Escolha a janela onde deseja rodar o bot:")
label.pack(pady=10)

# Combobox para listar as janelas
janelas_abertas = listar_janelas()
combo_janelas = ttk.Combobox(root, values=janelas_abertas)
combo_janelas.pack(pady=10)

# Botão para confirmar a seleção
botao_confirmar = tk.Button(root, text="Confirmar", command=selecionar_janela)
botao_confirmar.pack(pady=10)

# Inicia a interface gráfica
root.mainloop()
