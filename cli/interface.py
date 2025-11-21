import os
import random
import src.granulador as grain

#Constantes
in_dir = "input_audio"
out_dir = "output_audio"

header = '''
     ____________________
    |                    |
    |   GrainTEX v.1.0   |  
    |____________________|
'''

#Funções

def rando():
    return random.randrange(0, 1000)

def lista_arq_input():
    arqs = [arq for arq in os.listdir(in_dir)]
    print(f"\nLista de arquivos em {in_dir}\n")
    for i, arq in enumerate(arqs):
        print(f"{i}. {arq}")
    sele = input("\nSelecione um dos arquivos acima:\n>>> ")
    try:
        return arqs[int(sele)]
    except:
        print("Não foi possível retornar o arquivo")

def menu():
    print(header)
    while True:
        print("\n1. Granulador A - iterador fixo (mono)")
        print("2. Granulador B - iterador caminhante (mono)")
        #print("3. Granulador C - multicanal")
        print("0. Sair")
        usr = input("\nEscolha uma opção.\n>>> ")
        
        match usr:
            case "1": 
                menu_granA()
            case "2": 
                menu_granB()
            #case "3": 
                #menu_granC()
            case "0":
                print("Processo encerrado.")
                break
            case _:
                print("Digite uma opção válida.")

def menu_granA():
    #Configurações padrão
    grao_ini = 0
    grao_dur = 44000
    audio_dur = 2
    fade = 100
    aleatorio = False
    reverso = False
    while True:
        print("\n--- Granulador A - Iterador Fixo ---")
        print("\n1. Executar granulação")
        print("2. Configurações")
        print("3. Voltar ao menu anterior")
        usr = input("\nEscolha uma opção.\n>>> ")
        match usr:
            case "1":
                audio = lista_arq_input()
                audio_dir = f"{in_dir}/{audio}"
                out = f"{out_dir}/gr{rando()}_{audio}"
                print("\nProcessando...")
                gr = grain.granulador(audio_dir, grao_ini, grao_dur, audio_dur, fade=fade, aleatorio=aleatorio, reverso=reverso)
                grain.grava_audio(out, gr)
                print(f"Processo completo.\nÁudio exportado em {out}")
            case "2":
                grao_ini = int(input("Início do grão em índice de amostra (tipo: int): "))
                grao_dur = int(input("Duração do grão em número de amostras (tipo: int): "))
                audio_dur = float(input("Duração do áudio em segundos (tipo: float): "))
                fade = int(input("Duração de fade entre grãos em amostras (padrão = 100): "))
                aleatorio = input("Saltos aleatórios? (s/n): ")
                if aleatorio == "s":
                    aleatorio = True
                else:
                    aleatorio = False
                reverso = input("Uso de som retrogradado? (s/n): ")
                if reverso == "s":
                    reverso = True
                else:
                    reverso = False
            case "3":
                break
            case _:
                print("Digite uma opção válida.")
                
def menu_granB():
    #Configurações padrão
    grao_ini = 0
    grao_fim = 10000
    pedaco_dur_min = 0.2
    pedaco_dur_max = 1
    fade = 100
    print("\n--- Granulador B - Iterador Caminhante ---")
    while True:
        print("\n1. Executar granulação")
        print("2. Configurações")
        print("3. Voltar ao menu anterior")
        usr = input("\nEscolha uma opção.\n>>> ")
        match usr:
            case "1":
                audio = lista_arq_input()
                audio_dir = f"{in_dir}/{audio}"
                out = f"{out_dir}/gr{rando()}_{audio}"
                print("\nProcessando...")
                gr = grain.regrain(audio_dir, grao_ini, grao_fim, pedaco_dur_min, pedaco_dur_max, fade)
                grain.grava_audio(out, gr)
                print(f"Processo completo.\nÁudio exportado em {out}")
            case "2":
                grao_ini = int(input("Limite mínimo do grão em índice de amostra (tipo: int): "))
                grao_dur = int(input("Limite máximo do grão em índice de amostra (tipo: int): "))
                pedaco_dur_min = float(input("Duração mínima do grao em segundos (tipo: float): "))
                pedaco_dur_max = float(input("Duração máxima do grao em segundos (tipo: float): "))
                fade = int(input("Duração de fade entre grãos em amostras (padrão = 100): "))
            case "3":
                break
            case _:
                print("Digite uma opção válida.")
                
#Menu não implementado, pois requer módulo de separação de canais de áudio
def menu_granC():
    #Configurações padrão
    grao_ini = 0
    grao_dur = 44000
    audio_dur = 2
    fade = 100
    print("\n--- Granulador C - Iterador Fixo Multicanal ---")
    while True:
        print("\n1. Executar granulação")
        print("2. Configurações")
        print("3. Voltar ao menu anterior")
        usr = input("\nEscolha uma opção.\n>>> ")
        match usr:
            case "1":
                audio = lista_arq_input()
                audio_dir = f"{in_dir}/{audio}" #A função recebe uma lista de arquivos para cada canal, não um único arquivo
                out = out_dir
                print("\nProcessando...")
                gr = grain.granulacao_multicanal(audio_dir, out, grao_ini, grao_dur, audio_dur)
                print(f"Processo completo.\nÁudio exportado em {out}")
            case "2":
                grao_ini = int(input("Início do grão em índice de amostra (tipo: int): "))
                grao_dur = int(input("Duração do grão em número de amostras (tipo: int): "))
                audio_dur = float(input("Duração do áudio em segundos (tipo: float): "))
                fade = int(input("Duração de fade entre grãos em amostras (padrão = 100): "))
            case "3":
                break
            case _:
                print("Digite uma opção válida.")
