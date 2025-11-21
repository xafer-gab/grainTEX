# GrainTEX
Utilitário de síntese granular com suporte multicanal e controle preciso da faixa de amostragem, incluindo opções de randomização, retrogradação e congelamento de banda temporal (freeze).

### Instalação
1. Clone ou faça download dos arquivos do repositório.
2. Instale as dependências de <code>requirements.txt</code>.

### Uso
GrainTEX pode ser utilizado diretamente pelo menu interativo no terminal com a execução do script <code>main.py</code>. Os arquivos de áudio serão automaticamente listados desde que se encontrem no diretório <code>input_audio</code>.

A configuração padrão de saída é de 44kHz (mono). os arquivos gerados são gravados no diretório <code>output_audio</code>. Alguns exemplos de sons de trompete podem ser ouvidos e usados como teste. 

Alternativamente, o utilitário pode ser usado diretamente por meio de chamadas das funções do arquivo <code>src/granulador.py</code>, em específico no caso de processamento de áudio multicanal (as pistas devem estar separadas em arquivos mono).

### Contexto 
Este utilitário foi produzido durante a composição de *Astrolábio* (2024), obra octofônica estreada na XV Bienal de Música Eletroacústica de São Paulo (03/10/2024).
