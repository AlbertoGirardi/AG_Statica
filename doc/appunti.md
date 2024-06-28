26/06/2024


forza funzione di tempo, velocità e posizione 
scopo di equazioni differenziali -> funzione del tempo tale che soddisfa le condizioni

ordini delle equazioni differenziali -> 1 = c'è solo la derivata prima
sempre possibile scomporre una eq 2 ord -> 2 equ primo ordine

a sn incognite
a dx cose conosciute


METODO DI EULERO ESPLICIO

consideriamo punti di tempo discreti, troviamo valori discretui per le soluzioni di velocità e posizione

FLUSSO (velocità, accelerazione)

flusso * dt = variabile di stato

errore dipende in prima approssimazione da dt



matrice formata da vettori colonna contenenti il vettore u (posizione velocità) che è la variabile di stato

calcolo errore:



- consideriamo l'errore massimo lungo tutta la traiettoria (Norma a  infinito)
- errore RMS

aumento dell'errore -> lineare col tempo
se ci sono fenomeni oscillatori il metodo è particolarmente instabile


MOTO ARMONICO:

molla secondo il modello di hook
massa collegata solo alla molla

frequenza naturale (parametro con k e m)

-> soluzione analitica esatta




equazione omogenea: non ci sono forze esterne, spiega come il sistema reagisce alla perturbazione iniziale


MIGLIORAMENTO METODO DI EULERO SEMI IMPLICITO:
    prima si calcola la velocità 
    per aggiornare la posizione si usa la nuova velocità

solutori: ordine è la potenza del tempo rispetto al quale l'errore è proporzionale

metodo Runge–Kutta–Fehlberg corrector 4/5
- predizione con ordine 4
- corregge con metodo ordine 5

utilizzabile con scipy, necessario specificare lista dei tempi discreti al quale si vuole lavorare


implementare sistema dinamico con soluzione 


es. 2 evitare di avere velcità iniziale =/= 0

calcolare l'energia totale e registrarla e vedere se è costante oppure no

(metodi simplettici che conservano energia oppure altre quantità conservate)