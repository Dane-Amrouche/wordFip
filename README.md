Our project is a french academic project that aims to provide a simulation of the [WorldFIP](https://en.wikipedia.org/wiki/Factory_Instrumentation_Protocol) protocol over WiFi.

The following documentation is only avaiblable in french.

# Documentation
### Objectif du projet
**Émulation du réseau WorldFIP à l'aide du WiFi**

Implanter le protocole de FIP sur au moins deux RPi pour émuler le fonctionnement de l'arbitre de bus et d'un producteur et d'un consommateur d'objets. Lorsqu'un producteur a une nouvelle valeur, il allume une **LED1** pendant un temps équivalent à **1/10** de son temps de production. Quand un consommateur reçoit une valeur dépassant de **20%** la valeur précédente, il allume une **LED rouge** pendant un temps équivalent à **20%** de sa période de consommation. Sinon, il laisse allumée une **LED verte**.

### Liens intéressants

- (FR) [Cours](https://www.irit.fr/~Zoubir.Mammeri/Cours/Introduction_WorldFIP.pdf) sur le WorldFIP
- (EN) [Document](http://people.cs.pitt.edu/~mhanna/Master/ch2.pdf) semblerait-il issu d'une thèse détaillant un peu plus le protocole, notamment pour l'arbitre de bus
