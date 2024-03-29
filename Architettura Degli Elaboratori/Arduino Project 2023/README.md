## Analizzatore di Telecomandi

Questo progetto si propone di sviluppare un analizzatore di telecomandi, concentrando l'attenzione sull'identificazione del tasto premuto su un telecomando. Il processo è suddiviso in diverse fasi:

### Panoramica
Il progetto si concentra sull'analisi dei segnali provenienti dai telecomandi, utilizzati per controllare dispositivi elettronici, con l'obiettivo di identificare il tasto premuto.

### Obiettivi
1. Identificare i segnali dei telecomandi e filtrare i disturbi esterni.
2. Decifrare il pacchetto ricevuto seguendo il protocollo appropriato.
3. Salvare il valore del tasto premuto sul telecomando.

### Tappe Intermedie
1. Analisi del Problema
2. Statechart
3. Consolidamento dei Componenti
4. Sintesi
5. Implementazione & Verifica

### Funzionalità Chiave
- Il dispositivo deve essere in grado di riconoscere e decodificare i segnali provenienti dai telecomandi.
- Deve identificare il protocollo del telecomando per decodificare correttamente il valore del tasto premuto.
- Deve salvare il valore del tasto premuto in memoria.

### Componenti Principali
1. **Ricevitore IR**: Per rilevare i segnali infrarossi modulati.
2. **Timer**: Per misurare la durata degli impulsi e gestire il tempo tra gli eventi.
3. **Detettore di Protocollo**: Per identificare il protocollo del telecomando.
4. **Decodificatore**: Per estrarre e ottenere il valore del tasto premuto.
5. **Gestore di Memoria**: Per salvare e gestire i dati ottenuti.

### Implementazione & Verifica
- Integrazione dei componenti in un ambiente Arduino.
- Traduzione del flusso logico in codice C eseguibile.
- Verifica del corretto funzionamento tramite simulatore e debugging.

Questo progetto offre una solida base per lo sviluppo di un analizzatore di telecomandi, con una dettagliata analisi del problema, la definizione dei componenti necessari e una chiara strategia di implementazione e verifica.
