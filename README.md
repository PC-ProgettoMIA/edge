# Edge System
Livello necessario al funzionamento dell'intero sistema poichè racchiude i sensori che acquisiscono le informazioni ambientali.
Siccome l'edge può avere poche risorse computazionali e di memoria a disposizione, tutto ciò che è sull'edge è stato pensato per essere leggero e minimale. 
Qui il digital twin permette di avere un livello di astrazione della casina, catturandone gli aspetti importanti e rappresentandone, in ogni istante, un gemello digitale con le informazioni aggiornate.
#### Software Info

![GitHub](https://img.shields.io/github/license/PC-ProgettoMIA/edge)
![GitHub language count](https://img.shields.io/github/languages/count/PC-ProgettoMIA/edge)
![GitHub top language](https://img.shields.io/github/languages/top/PC-ProgettoMIA/edge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/PC-ProgettoMIA/edge)
![GitHub issues](https://img.shields.io/github/issues/PC-ProgettoMIA/edge)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/PC-ProgettoMIA/edge)
![GitHub repo size](https://img.shields.io/github/repo-size/PC-ProgettoMIA/edge)
![GitHub contributors](https://img.shields.io/github/contributors/PC-ProgettoMIA/edge)

#### Software Progress
![GitHub issues](https://img.shields.io/github/issues/PC-ProgettoMIA/edge)
![GitHub closed issues](https://img.shields.io/github/issues-closed/PC-ProgettoMIA/edge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/PC-ProgettoMIA/edge)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/PC-ProgettoMIA/edge)
![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/PC-ProgettoMIA/edge/latest/develop)
![GitHub last commit](https://img.shields.io/github/last-commit/PC-ProgettoMIA/edge/develop)


## Requirements
Il software dell'edge può essere messo in esecuzione solo sulle casette realizzate per il _progetto MIA_.

## Deployment
Il deployment può essere effettuato in varie modalità in base ai comportamenti desiderati del sistema.

### Caso edge 
In assenza del cloud e della messa in funzione di una o più casette e un singolo fog, seguire i seguenti passaggi:
```bash
#Abilitare i permessi per l'esecuzione dello script.
chmod 755 edge.sh
#Esecuzione per l'avvio del servizio
./edge.sh
```

### Caso edge e fog
In assenza del cloud e della messa in funzione di una o più casette e un singolo fog, seguire i seguenti passaggi:
```bash
#Abilitare i permessi per l'esecuzione dello script.
chmod 755 edge-fog.sh
#Esecuzione per l'avvio del servizio
./edge-fog.sh
```

### Caso edge e cloud
In presenza del cloud, seguire i seguenti passaggi:
```bash
#Abilitare i permessi per l'esecuzione dello script.
chmod 755 edge-cloud.sh
#Esecuzione per l'avvio del servizio
./edge-cloud.sh
```

### Caso edge, fog e cloud
In presenza di tutte le componenti, seguire i seguenti passaggi:
```bash
#Abilitare i permessi per l'esecuzione dello script.
chmod 755 edge-fog.sh
#Esecuzione per l'avvio del servizio
./edge-fog.sh
```


# License
See the [License File](./LICENSE).

## Author and Copyright
Author:
- [Battistini Ylenia](https://github.com/yleniaBattistini)
- [Gnagnarella Enrico](https://github.com/enrignagna)
- [Scucchia Matteo](https://github.com/scumatteo)

Copyright (c) 2021.
