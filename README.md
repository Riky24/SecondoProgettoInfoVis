# SecondoProgettoInfoVis
## Obiettivo
Il "Ledger", cioè il "libro mastro", di Bitcoin è costituito da una successione di blocchi, uniti in una catena: la blockchain. 
Occasionalmente, può succedere che due blocchi diversi vengano "minati", cioè aggiunti alla catena, quasi simultaneamente. 
I blocchi, che hanno la stessa posizione nella chain (chiamata "height", cioè altezza) vengono propagati dai miners che li hanno minati 
e dunque coesistono nella rete peer-to-peer di Bitcoin costituendo di fatto una biforcazione della blockchain. Il blocco dal quale partirà 
la catena più lunga è quello che determinerà la "main chain" e da cui continuirà la crescita della blockchain.
Lo scopo di questo progetto è visualizzare e rendere esplorabile l'albero dei blocchi. Si tratta di un albero molto particolare, composto da 
una lunghissima catena e da episodiche diramazioni (lunghe generalmente un blocco, talvolta due, raramente di più).

## dataSet.py
Questo script permette di generare una blockchain in formato JSON. 
La main function (creaJson(n)) riceve in ingreso un parametro n che rappresenta la profondità massima della chain da realizzare.
Il seguente script consente di generare chain di lunghezza arbitraria. Per i limiti imposti dalla ricorsione in Python il parametro n viene 
splittato in più iterazioni che consentono di gestire chain di profondità masima pari a 2000 blocchi. Nel generare una rappresentazione che 
rispecchiase la lunghezza effettiva della blockchain abbiamo riscontrato dei limiti nella gestione delle dimensioni dei file da parte dei 
browser (Chrome, Firefox), e per questo la rappresentazione risultante lavora con chain di altezza poco superiore a 2000 blocchi.
La creazione dell'albero dipende da due variabili globali P1 e P2, che rappresentano rispettivamente la probabilità di non generare una 
biforcazione e la probabilità di non tagliare la biforcazione. Nel caso base per questo progetto i valori delle probabilità usati sono P1 = 0.999 
e P2 = 0.1, considerando il caso reale osservato nelle blockchain. L'utilizzo di queste probabilità come parametri è stato preso in considerazione 
per generalizzare la visualizzazione e non limitare il progetto alle sole blockchain.
Il JSON prodotto al termine dell'esecuzione dello script contiene una lista di blocchi, ognuno con la seguente struttura:
{"hash", "prev_block", "height", "height_pred", "id"}, dove:
- "hash": il valore dell'hash del blocco corrente;
- "prev_block": hash del blocco precedente;
- "height": altezza del blocco nella chain;
- "height_pred": altezza del blocco precedente;
- "id": un id incrementale che identifica il blocco (usato per ordinare i blocchi).

## index.html
Questo script attraverso la libreria D3.js consente di rappresentare la blockchain generata del punto precedente in formato JSON.
La chain viene rappresentata a partire dal nodo ad altezza zero muovendosi da sinistra a destra e in modo discendente, fino ad 
un limite destro settabile tramite una variabile definita nel codice. Raggiunto tale limite la rappresentazione prosegue scendendo, di un'altezza 
definita anche essa tramite una variabile, da destra a sinistra. Analogamente si ottiene lo stesso comportamento una volta raggiunto il limite sinistro. 
La rappresentazione prosegue mantenedo questo andamento fino al termine dei blocchi.
Ogni blocco, prima di poter essere rappresentato, è sottoposto ad un'analisi che consente di determinare se quel blocco può appartenere ad una catena 
di blocchi consecutivi tra loro (senza biforcazioni nel mezzo). Questi blocchi possono essere raggruppati formando un nuovo blocco, definito nodo cluster. 
Quando si incontra una biforcazione il blocco in questione è gestito come una singola entità (non inclusa nel cluster).
All'interno della rappresentazione sono presenti quindi due diverse tipologie di blocchi:
- Cluster: Rappresentati da rettangoli di lunghezza variabile pari ad un numero di unità calcolato in funzione del numero di nodi contenuti in un cluster. 
           Un cluster è un insieme di blocchi consecutivi che cresce in scala logaritmica fino a che non si incontra una diramazione. 
           Una diramazione è riconosciuta quando il nodo che stiamo per inserire nel cluster presenta più di un nodo figlio. 
           A quel punto si inseriscono i nodi precedenti a questo nel cluster e si memorizza la dimensione del cluster calcolandone anche il log2 che 
           determinerà la lunghezza del nodo stesso. Il valore del logaritmo calcolato viene utilizzato rispettando la Steve’s power law relativa alla 
           rappresentazione delle lunghezze, quindi a tale valore viene applicato un’esponente pari a 1/√ (1)=1 che ne determinerà la lunghezza in termini di unità
           (un cluster con 2^2 blocchi produrrà un nodo lungo 2 unità, mentre con 2^5 blocchi si otterrà un nodo lungo 5 unità).
           Posizionando il puntatore al di sopra di un cluster è possibile visualizzare un pop-up che indica il numero, sotto forma di potenza di 2, di blocchi 
           in esso contenuti. 
- Blocco base: Rappresentato da rettagoli di lunghezza fissa pari ad una unità. E' questo il blocco incaricato della visualizzazione dei dati presenti nella blockchain, 
               infatti da ognuno di questi blocchi è possibile accedere alle informazioni a lui associate tramite pop-up attivato visitando con il mouse il blocco.
L'utilizzo dei cluster si è reso necessario al fine di snellire e rendere più navigabile la chain presentata. Infatti i cluster permettono di racchiudere 
le lunghe sequenze continue di blocchi in un unico nodo dal quale è possibile accedere ai nodi in esso contenuti tramite un click sull'elemento. Generando uno o 
più livelli sottostanti fino alla rappresentazione dei blocchi base.
La rappresentazione viene accompagnata da due tasti che permettono l'interazione con questo modello:
- Il tasto Home: permette all'utente di visualizzare il livello più alto della chain;
- Il tasto Back: permette all'utente di tornare al livello precedente.
Entrambi questi tasti sono mostrato solamente dopo aver acceduto ai livelli sottostanti il primo.
#### Problemi riscontrati
- Dato l'elevato numero di blocchi presenti nella rappresentazione l'utilizzo di un solo livello di clusterizzazione produceva un elevato numero di blocchi base 
  da rappresentare che rendevano difficile la navigazione. Per questo si è scelto di produrre livelli intermedi di clusterizzazione, a partire da un numero di 
  blocchi tale da appesantire la rappresentazione, applicando una separazione per potenze di 2. In questo modo la complessità rappresentativa e stata ripartita 
  su più cluster invece di utilizzarne solamente uno.
- Un ulteriore problema affrontato riguarda la suddivisione dei blocchi nei livelli di cluster intermedi. Come già anticipato la soluzione è stata basata 
  sull'utilizzo della potenza di 2 associata al cluster. L'obiettivo da perseguire è stato quello di rendere questi blocchi di uguale grandezza, per questo 
  è stato implementato un algoritmo che si occupa di dividere in due potenze di 2 il più possibile simili tra loro a partire dal valore dei blocchi contenuti nel 
  cluster (da 2^9 blocchi si dividono in 2^4 e 2^5). Il primo valore consente di generare il numero di cluster (2^4), mentre il secondo definisce il numero di 
  blocchi (2^5) contenuti in ognuno di essi. Questa startegia consente di garantire un equilibrio tra il numero di blocchi e il numero di cluster in ogni visualizzazione.
- Un' altra difficoltà affrontata in questo progetto riguarda la rappresentazione dei blocchi nel caso di biforcazioni. Prendendo in esame il caso peggiore, 
  si va incontro a problemi quali: sovrapposizione dei blocchi, intersezione degli archi tra i blocchi e gestione delle diramazioni in funzione della 
  catena principale. Il primo problema affrontato è stato quello del posizionamento dei nodi secondari rispetto alla catena principale. Questi nodi richiedono 
  di potersi evolvere indipendentemente dalla catena principale senza sovrapporsi e mantenendo un andamento simile per poter risultare comunque leggibili. Per questo
  l'approccio utilizzato è stato quello di realizzare per prima la catena principale e solo in seguito andando a ritroso nella catena e gestire la produzione 
  delle diramazioni. Nella gestione di questa problematica abbiamo riscontrato due fenomeni relativi alle diramazioni prodotte: La sovapposizioni dei blocchi di 
  catene contigue e l'intersezione degli archi di questi blocchi. La strategia applicata per evitare la sovrapposizione dei blocchi è stata quella di iterare un 
  controllo sulle coordinate x e y del blocco da rappresentare e delle posizioni adiacenti; fino a quando il controllo restituisce esito negativo la coordinata y 
  viene incrementata per aumentare l'altezza del nodo cercando di sfruttare le aree vuote nel grafo. Per quanto riguarda le intersezioni degli archi si è scelto di 
  anticipare il cambio direzione valutando la distanza entro cui non era più possibile rappresentare in maniera efficace un nuova diramazione. In tal senso un 
  nodo da cui si genera una diramazione cambierà direzione prima, rispetto ad altri nodi, per poter sfruttare al meglio lo spazio adiacente nella produzione dei 
  suoi figli. Per noi, aver scelto di utilizzare questa strategia ci ha consentito di raggiungere il trade off tra le due problematiche. Questa scelta non garantisce
  la soluzione ottima ai problemi nel casi limite.
- L'ultimo problema da affrontare ha riguardato gli aspetti cromatici della rappresentazione. Per rappresentare l'elevato numero di blocchi, è stato considerato 
  l’utilizzo di colori con tonalità pastello per evitare l’affaticamento dei coni.
#### Sviluppi futuri
Nella visualizzazione dei dati associati ai blocchi sono stati utilizzati valori fittizzi calcolati all'interno della funzione getValues() in index.html al fine 
di mantenere ridotta la dimensione del file JSON prodotto dallo script dataSet.py. Questo per garantire un maggior numero di blocchi rappresentabili. 
Per adeguare il contenuto del file JSON a casi di studio reali è necessario effettuare il mapping dei valori a partire dal file prodotto e gestire le limitazioni 
del browser (in termini di dimensioni del file).
Come gia emerso in precedenza occorre approfondire tutti i casi in cui non è possibile garantire l'ottimalità tra intersezione degli archi e sovrapposizione 
dei nodi, prendendo in considerazione ulteriori variabili e approfondendo le strategie per la gestione di tali problematiche.
