import numpy as np
import librosa
import soundfile as sf
import random


def crossfade(audio1, audio2, fade, so_fade=False):
    try:
        fade_in = np.linspace(0, 1, fade)
        fade_out = fade_in[::-1]

        fade_audio1 = audio1[-fade:].copy()
        fade_audio2 = audio2[:fade].copy()

        fade_audio1 *= fade_out
        fade_audio2 *= fade_in

        fade_combinado = fade_audio1 + fade_audio2

        if so_fade:
            return fade_combinado
        else:
            trecho_audio1 = audio1[:-fade]
            trecho_audio2 = audio2[fade:]
            audio_final = np.concatenate((trecho_audio1, fade_combinado, trecho_audio2))
            return audio_final

    except:
        print("Erro de fade nos objetos", audio1, audio2)
        return np.empty(0)


def crossfade_concatenado(entrada_lista_arrays, duracao_chunks, fade=100):
    output_audio = np.empty(0)
    fades = []

    for i in range(len(duracao_chunks) - 1):
        trecho_fade = crossfade(entrada_lista_arrays[i], entrada_lista_arrays[i+1], fade, so_fade=True)
        fades.append(trecho_fade)

    for i in range(len(entrada_lista_arrays)):
        output_audio = np.append(output_audio, entrada_lista_arrays[i][fade:-fade])
        if i < len(fades):
            output_audio = np.append(output_audio, fades[i])

    return output_audio


def inverte_audio(audio):
    reverso = np.empty(0)
    index_array = len(audio)
    contador = index_array - 1
    for i in range(index_array):
        reverso = np.append(reverso, audio[contador])
        contador -= 1
    return reverso


def granulador(path, inicio, grao, tempo_loop, fade=100, aleatorio=False, reverso=False):
    audio, sr = librosa.load(path, sr=None)
    tempo = int(tempo_loop * sr)
    grao += fade

    if aleatorio:
        min_ = inicio
        max_ = len(audio) - grao

        saida_bruta = np.empty(0)
        pedacos_dur = 0
        pedacos_num = 0

        while pedacos_dur < tempo:
            inicio_aleatorio = random.randrange(min_, max_)
            fim_aleatorio = inicio_aleatorio + grao
            granulado = audio[inicio_aleatorio:fim_aleatorio]

            if reverso:
                reverter = random.randrange(0, 1)
                if reverter == 1:
                    granulado[::-1]

            saida_bruta = np.append(saida_bruta, granulado)
            pedacos_dur += grao
            pedacos_num += 1

        audio_saida = np.empty(0)
        fatia_fim = grao

        for i in range(pedacos_num - 1):
            trecho1 = saida_bruta[fatia_fim - grao:fatia_fim]
            trecho2 = saida_bruta[fatia_fim:fatia_fim + grao]
            fragmento_fade = crossfade(trecho1, trecho2, fade, so_fade=True)
            trechos_unidos = np.concatenate((trecho1[fade:-fade], fragmento_fade))
            audio_saida = np.append(audio_saida, trechos_unidos)
            fatia_fim += grao

        return audio_saida

    else:
        saida_bruta = np.empty(0)
        pedacos_dur = 0
        pedacos_num = 0

        while pedacos_dur < tempo:
            granulado = audio[inicio:inicio + grao]
            saida_bruta = np.append(saida_bruta, granulado)
            pedacos_dur += grao
            pedacos_num += 1

        audio_saida = np.empty(0)
        fatia_fim = grao

        for i in range(pedacos_num - 1):
            trecho1 = saida_bruta[fatia_fim - grao:fatia_fim]
            trecho2 = saida_bruta[fatia_fim:fatia_fim + grao]
            fragmento_fade = crossfade(trecho1, trecho2, fade, so_fade=True)
            trechos_unidos = np.concatenate((trecho1[fade:-fade], fragmento_fade))
            audio_saida = np.append(audio_saida, trechos_unidos)
            fatia_fim += grao

        return audio_saida


def granulacao_multicanal(paths, dir_saida, inicio, grao, tempo_loop, fade=100):
    numeral = 1
    r_titulo = random.randrange(0, 1000)
    print(f"O granulador irá criar {len(paths)} canais e exportá-los como <{r_titulo}.wav>")
    for audios in paths:
        som, sample_rate = librosa.load(audios, sr=None)
        print(f'\nRealizando a granulação do canal {numeral}')
        faz_canal = granulador(audios, inicio, grao, tempo_loop, fade=fade, aleatorio=True, reverso=True)
        sf.write(f"{dir_saida}/C{numeral}_{r_titulo}.wav", faz_canal, sample_rate)
        print(f"O canal {numeral} foi gravado.")
        numeral += 1


def regrain(audio_path, grao_sr_min, grao_sr_max, chunk_dur_min, chunk_dur_max, fade=100):
    audio, sr = librosa.load(audio_path, sr=None)
    tempo_total = len(audio)
    audios_chunk = []
    audios_chunk_dur = []

    sr_usado = 0
    while tempo_total > sr_usado:
        grao_sr = random.randrange(grao_sr_min, grao_sr_max)

        if type(chunk_dur_min) == int:
            chunk_dur = random.randrange(chunk_dur_min, int(chunk_dur_max))
            audios_chunk_dur.append(chunk_dur * sr)

        elif type(chunk_dur_min) == float:
            chunk_dur = random.uniform(chunk_dur_min, float(chunk_dur_max))
            audios_chunk_dur.append(int(chunk_dur * sr))

        chunk = granulador(audio_path, sr_usado, grao_sr, chunk_dur, fade=fade, reverso=True)
        audios_chunk.append(chunk)

        tempo_total -= int(grao_sr * chunk_dur)
        sr_usado += int(grao_sr * chunk_dur)

        print("Samples restantes para processar:", tempo_total)

    return crossfade_concatenado(audios_chunk, audios_chunk_dur, fade)


def grava_audio(nome, arquivo, sr=44000):
    sf.write(nome, arquivo, sr)
