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


# MULTI BODY


vettore per le velocità = vettore forze applicate * matrice inerzia


da sistema di rif mobile a fisso,
punto sigma a è fisso, cambia solo la matrice di rotazione

calcolo velocità del punto
derivata matrice di rotazione per sapere velocità = matrice (t+pi/2)



accelerazione per baricentro

discorso simile per accelerazioen ma l'accelerzione totale è quella tangenziale + la centripeta (che la mantinee nel moto di rotazione)


vincoli: forze che esprimono sono tali da mantere una certa condizione cinematica

forza di una molla e dello smorzatore 



nel multibody ci sono anche forze non attive
ci sono anche forze non attive

mega matrice con le masse e momenti di inerzia


vincolo cerniera  
hr -> vettore delle forze reattive, per cerniera f in x, y e momento    

vettore di reazioni dei due corpi, matrice che rappresenta il vincolo per vettore delle direzioni del vincolo

vincolo cinematico -> funzione delle q -> sistema di equzioni da rispettare -> equazione vettoriale 
condizioni su accelerazioni e 


vincolo cerniera: i punti della cerniera devono essere coincidenti, e le loro velocità  uguali

matrice jacobiana legata all 'alra trasposta

da dimostrare che velocità del vettore normale è 



RISULTATO: DUE EQUAZIONI DIFFERENZIALI:

equazione sulla cinematica del corpo (come prima)

equazione del vincolo

-> q due punti accelerazioni totali -> trasformarlo nel vettore flusso