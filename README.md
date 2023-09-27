# BOT Telegram para Gerenciamento de Caixas FTTN

Este bot Telegram foi criado para facilitar o gerenciamento de caixas FTTN em sua rede. Ele oferece várias funcionalidades para simplificar as operações de provisionamento, manutenção e monitoramento de caixas nas OLTs.

## Funcionalidades

Com este bot, você pode:

- Provisionar ONU Parks em OLTs.
- Remover caixas provisionadas.
- Verificar informações detalhadas das caixas na OLT.
- Atualizar o estado das caixas.
- Verificar os equipamentos conectados em uma caixa.
- Reiniciar caixas remotamente.

## Tecnologias Utilizadas

Este bot foi desenvolvido utilizando Python e Shell Script.

## Como Usar

1. Clone este repositório.
2. Crie um arquivo chamado .env na pasta conf e troque as informações.
```.env
TELEGRAM_TOKEN=TOKEN_DO_BOT
BASE_API_URL=https://http.cat/

# Configurações do canal
THEREAD_CHANNEL=True
DEBUG_MODE=True

CHANNEL_ID=ID_CHAT_PRODUÇÃO
DEBUG_CHANNEL_ID=ID_CHAT_DEV

THEREAD_CHANNEL_ID=ID_TOPICO_CASO_TENHA
DEBUG_THEREAD_CHANNEL_ID=ID_TOPICO_CASO_TENHA

USER_OLT = "USER_OLT"
PASS_OLT = "SENHA_OLT"
```
3. Execute o bot usando o python3 main.py.
4. Interaja com o bot via Telegram para realizar as operações desejadas.

## Contato

Para mais informações ou suporte, entre em contato com igor.couto.oliveira@gmail.com.

**Nota**: Certifique-se de que o uso deste bot esteja em conformidade com as políticas e regulamentações internas da sua empresa e com as leis aplicáveis.
