from machine import ADC, Pin
import time

#configuracao dos pinos
ldr_pino = ADC(Pin(34))
ldr_pino.atten(ADC.ATTN_11DB)
btn_pino = Pin(12,Pin.IN, Pin.PULL_UP)

#----------------
total_pecas = 0
peca_bloqueando = False
tempo_inicio_bloqueio = 0
alerta_parada_disparado= False

print("Contador de Producao Inicializado")