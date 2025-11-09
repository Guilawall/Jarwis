# Assistente Jarwis reescrito

Este projeto implementa um protótipo do "Jarwis": um assistente de voz em português
que fica escutando em segundo plano, responde quando ouve o chamado "Jarwis" e
executa ações específicas:

- Responde "Senhor, o que deseja?" após ouvir o wake word.
- Realiza chamadas telefônicas para contatos salvos quando você diz
  **"Jarwis… ligar para (nome do contato)"**.
- Mantém uma lista persistente: é possível adicionar, remover, consultar todos os
  itens ou perguntar qual é o *n*-ésimo termo cadastrado.

O foco principal é o Android via Termux + Termux:API, mas o código também pode ser
executado em um computador com microfone.

## Comandos suportados

Depois do wake word, o Jarwis entende as frases abaixo (maiúsculas apenas para
ilustração):

| Frase | Ação |
| ----- | ---- |
| `Jarwis… ligar para Maria` | Procura "Maria" nos contatos e inicia uma chamada telefônica. |
| `Jarwis… adicionar café à lista` | Armazena a palavra "café" na lista persistente. |
| `Jarwis… retirar café da lista` | Remove "café" se existir, ou responde "Senhor, isso não tem na lista." |
| `Jarwis… o que tem na lista?` | Lê em voz alta todos os itens cadastrados. |
| `Jarwis… qual é o quinto termo da lista?` | Informa o item na posição solicitada (ordinais até vigésimo ou números). |

A lista fica salva em `~/.jarwis/lista.json`, permitindo que o conteúdo seja
mantido entre execuções.

## Instalação no Android (Termux)

1. Instale [Termux](https://f-droid.org/packages/com.termux/) e o complemento
   [Termux:API](https://f-droid.org/packages/com.termux.api/).
2. Abra o Termux, conceda acesso ao armazenamento e prepare os pacotes básicos:
   ```bash
   termux-setup-storage
   pkg update
   pkg install python clang fftw libffi ffmpeg termux-api git
   python -m pip install --upgrade pip
   ```
3. Clone este repositório (substitua pelo endereço correto se estiver usando um fork):
   ```bash
   git clone https://github.com/Guilawall/Jarwis.git
   cd Jarwis
   ```

  > **Baixou um ZIP pelo celular?** O Android costuma descompactar em uma
  > pasta com espaço, como `Sistema Jarwis`. Nesse caso:
  >
  > 1. Rode `ls` dentro da pasta recém-criada. Se o comando listar apenas
  >    `Sistema Jarwis`, significa que você ainda está um nível acima do
  >    projeto original.
  > 2. Entre nessa pasta com aspas: `cd "Sistema Jarwis"` e rode `ls` de
  >    novo. Este repositório agora traz um **atalho** lá dentro: um novo
  >    `README.md`, um `main.py` que aponta para o original e arquivos
  >    `requirements*.txt` que importam os do diretório pai.
  > 3. Mesmo assim, a recomendação é voltar para o diretório raiz usando
  >    `cd ..` ou renomear a pasta para evitar o espaço: `mv "Sistema Jarwis" Jarwis`
  >    e voltar para ela com `cd Jarwis` antes de continuar.

   Confirme que você está dentro da pasta correta e que os arquivos
   `main.py` e `requirements.txt` aparecem na listagem. Esses nomes são
   **exatamente** assim, com `requirements` no plural e a extensão `.txt`.

   ```bash
   pwd               # deve terminar com .../Jarwis
   ls                # precisa mostrar main.py e requirements.txt
   cat requirements.txt
   ```

   O arquivo `requirements.txt` precisa conter **apenas** a linha abaixo. Se aparecer
   qualquer outra coisa (por exemplo, um comando começando com `git`), recrie o
   arquivo com o comando mostrado em seguida antes de instalar as dependências.

   ```text
   SpeechRecognition>=3.10
   ```

   ```bash
   printf 'SpeechRecognition>=3.10\n' > requirements.txt
   pip install -r requirements.txt
   ```
4. Execute o assistente indicando o backend Termux. A primeira execução pedirá
   permissão de microfone no Android. Use `./main.py` para garantir que o Python
   procure o arquivo dentro da pasta atual:
   ```bash
   python ./main.py --input-backend termux --log-level INFO
      ```

O Jarwis criará o diretório `~/.jarwis/` para armazenar a lista e arquivos
temporários de áudio.

### Rodando automaticamente ao iniciar o Termux

O script `scripts/termux_service.sh` aplica `termux-wake-lock` e inicia o Jarwis
com o backend Termux. Para utilizá-lo com o aplicativo Termux:Boot:

```bash
mkdir -p ~/.termux/boot
cp scripts/termux_service.sh ~/.termux/boot/jarwis.sh
chmod +x ~/.termux/boot/jarwis.sh
```

Opcionalmente configure variáveis de ambiente antes de chamar o script para ajustar
wake word ou tempos de escuta (veja a seção "Configuração").

## Execução em computadores

Em sistemas Linux/macOS/Windows com microfone compatível com PyAudio:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-desktop.txt
python ./main.py --input-backend microphone
```

Se o PyAudio não estiver disponível, utilize o backend Termux.

## Configuração

As opções podem ser fornecidas pela linha de comando ou por variáveis de ambiente.
Se um parâmetro não for informado, o Jarwis usa os seguintes valores padrão:

| Variável / Flag | Padrão | Descrição |
| --------------- | ------ | --------- |
| `--wake-word` / `JARWIS_WAKE_WORD` | `jarwis` | Palavra de ativação (aceita variações como "jarvis"). |
| `--input-backend` / `JARWIS_INPUT_BACKEND` | `auto` | `termux`, `microphone` ou `auto` (prioriza Termux). |
| `--passive-seconds` / `JARWIS_PASSIVE_SECONDS` | `4.0` | Tempo para ouvir o wake word. |
| `--command-seconds` / `JARWIS_COMMAND_SECONDS` | `6.0` | Janela para entender o comando após o wake word. |
| `--language` / `JARWIS_LANGUAGE` | `pt-BR` | Idioma usado pelo serviço de transcrição. |
| `JARWIS_TERMUX_MIC` | `termux-microphone-record` | Comando utilizado para gravar áudio no Termux. |
| `JARWIS_TERMUX_TTS` | `termux-tts-speak` | Comando de síntese de voz. |
| `JARWIS_TERMUX_CONTACTS` | `termux-contact-list` | Comando usado para ler os contatos. |
| `JARWIS_TERMUX_CALL` | `termux-telephony-call` | Comando usado para iniciar chamadas telefônicas. |

## Dependências

- `SpeechRecognition>=3.10` – transcrição de áudio via Google Speech.
- - `pyaudio` (apenas em desktops) – necessário para capturar áudio em tempo real.

No Termux, todas as interações com o microfone, contatos, TTS e telefone passam
pelos binários do Termux:API.

## Dicas de uso

- A transcrição depende da internet (serviço Google). Para respostas mais rápidas,
  tente falar frases completas logo após ouvir "Senhor, o que deseja?".
- O comando de chamadas procura aproximações por nome. Se houver ambiguidade,
  renomeie os contatos para evitar confusões.
- Para limpar a lista manualmente, apague o arquivo `~/.jarwis/lista.json`.

Divirta-se com o seu novo Jarwis!
