import time
from machine import Pin, ADC


def detecta_peca(leitura_ldr, tempo_atual):
    global peca_em_transito, tempo_inicio_bloqueio, alerta_parada_disparado, total_pecas
    if leitura_ldr > LIMIAR_BLOQUEIO:
        if peca_em_transito == False:
            peca_em_transito = True
            tempo_inicio_bloqueio = tempo_atual
            alerta_parada_disparado = False
        else:
            # verifica tempo de bloqueio
            if not alerta_parada_disparado and time.ticks_diff(tempo_atual, tempo_inicio_bloqueio) >= TEMPO_PARADA_MS:
                print("Alerta: Micro-parada detectada!")
                alerta_parada_disparado = True

    elif leitura_ldr < LIMIAR_LIVRE:
        if peca_em_transito:
            total_pecas += 1
            print(f"Peca detectada! Total: {total_pecas}")
            peca_em_transito = False


def reseta_turno(leitura_btn):
    global ultimo_estado_btn, total_pecas, peca_em_transito, alerta_parada_disparado, tempo_inicio_bloqueio

    # detecta o momento em que botao é solto 
    if ultimo_estado_btn == 0 and leitura_btn == 1:
        total_pecas = 0
        peca_em_transito = False
        alerta_parada_disparado = False
        tempo_inicio_bloqueio = 0
        print('Turno resetado com sucesso. Contadores zerados.')
        

    # atualiza a memoria do ultimo estado 
    ultimo_estado_btn = leitura_btn

#configuracao dos pinos
ldr_pino = ADC(Pin(34))
ldr_pino.atten(ADC.ATTN_11DB)
btn_pino = Pin(12,Pin.IN, Pin.PULL_UP)

# constantes 
LIMIAR_BLOQUEIO = 1800     # valor para lux baixo
LIMIAR_LIVRE = 1000        # valor para  lux alto
TEMPO_PARADA_MS = 5000     # 5 segundos para alerta de micro-parada

#variaveis para ajudar a analisar o movimento da esteira 
total_pecas = 0
peca_em_transito = False
tempo_inicio_bloqueio = 0
alerta_parada_disparado= False

# debounce do botao
ultimo_estado_btn = 1
ultimo_tempo_btn = 0
reset_executado = False

print("Contador de Producao Inicializado")

while True:
    tempo_atual = time.ticks_ms()
    leitura_ldr = ldr_pino.read()
    leitura_btn = btn_pino.value()
    detecta_peca(leitura_ldr, tempo_atual)
    reseta_turno(leitura_btn)
    #tempo para estabilidade
    time.sleep_ms(10)  
