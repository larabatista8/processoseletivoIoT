## Relatório do Candidato

---

### Identificação do Candidato

- **Nome completo:** Larissa Batista
- **GitHub:** https://github.com/larabatista8/processoseletivoIoT/

---

## Visão Geral da Solução

O projeto tem o objetivo de monitorar uma esteira de produção industrial, através da contagem de peças e detecção de anomalias. O sistema identifica a passagem de objetos por meio de um sensor de luminosidade. Dessa forma, quando a luz é interrompida uma peça é detectada e se a interrupção durar mais do que o tempo limite, o sistema informa que houve uma micro-parada. O usuário  interage com o sistema por meio de um botão físico, o qual é utilizado para resetar os contadores e iniciar um novo turno de produção.

---

## Arquitetura do Sistema Embarcado

Fluxo principal: O código é executado dentro de um laço while, de forma continua. A cada iteração o sistema lê os valores do sensor analógico e do botão e repassa os valores para as funções responsáveis por detectar uma nova peça e por resetar o turno.

Estado e temporização: o sistema gerencia o tempo usando  as funções time.ticks_ms() e time.ticks_diff(), enquanto o estado da esteira é controlado por variáveis globais que memorizam se a peça está passando ou se um alerta já foi emitido.

Interação: O LDR controla as mudanças de estado da esteira, enquanto o botão tem a capacidade de sobrescrever as variáveis de estado e zerar o sistema a qualquer momento.

---

## Componentes Utilizados na Simulação

Placa ESP32 DevKit V4: Microcontrolador principal responsável por processar a lógica, ler os pinos e enviar os dados pela interface serial.

Sensor Fotoresistor (LDR):Atua como o sensor de presença da esteira, medindo a variação de luz.

Botão de Pressão: Responsável por receber o comando manual do usuário para resetar o turno.

---

## Decisões Técnicas Relevantes

1. Ao resetar o turno, a variável tempo_inicio_bloqueio também é zerada, impedindo falsos positivos de micro-parada imediatamente após o reset.
2. A lógica foi separada em funções dedicadas (detecta_peca e reseta_turno), a fim de deixar o loop principal limpo e facilitando a manutenção.
3. A lógica do botão foi programada para agir durante a mudança de estado. Sendo assim, em vez de acionar o reset enquanto o botão estiver pressionado, o código detecta a transição, disparando a ação apenas uma vez no momento em que o botão é solto.

---

## Resultados Obtidos

1. O sistema identifica corretamente a entrada e saída de peças e incrementa o contador.
2. O alerta de micro-parada é acionado após 5 segundos de bloqueio contínuo.
3. O botao de reset limpa todas as variáveis corretamente.

---
## Comentários Adicionais (Opcional)

Durante a execução dos testes automatizados, foram enfrentados problemas  de timeout no caso de teste 3.

Primeiramente a falha ocorreu devido ao envio repetitivo da mensagem de confirmação de reset na porta serial enquanto o botão estava sendo pressionado. Para solucionar a falha, reestruturou-se a função aplicando o conceito de detecção por borda de descida, garantindo que a instrução de reset seja executada exatamente uma única vez por clique, independentemente da duração do pressionamento. 

A segunda causa de timeout foi causada por uma falha de sincronismo entre o firmware e o script de teste. Originalmente o código registrava o reset e imprimia a mensagem de confirmação no exato momento em que o botão era pressionado, enquanto o arquivo de teste aguardava 200 milissegundos e só começava a monitorar a porta serial após o botão ser solto, perdendo a leitura da mensagem que já havia sido enviada. Dessa forma, foi necessário alterar  novamente a lógica na função de reset e executar a ação na borda de subida, como consequência,  o disparo da mensagem no microcontrolador foi sincronizado com o instante em que o arquivo de teste inicia a escuta. 

---


