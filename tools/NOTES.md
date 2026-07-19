# Notes de décompilation (acquis vérifiés)

## Allocation des locales par MWCC (mwcceppc GC/3.0a5.2)
Les variables locales sont assignées aux slots de pile en **ordre de déclaration
INVERSE** : la dernière déclarée obtient l'offset le plus bas.

Vérifié sur ft_captain fn_100_BCF4 : dix `short` déclarés `v8..v26` ont produit
les slots 26,24,22,20,18,16,14,12,10,8 dans cet ordre. En permutant l'ordre de
déclaration selon cette règle, l'agencement de pile de la cible a été reproduit
exactement (sth r0,24(r1) / addi r3,r1,26 / addi r4,r1,24 conformes).

Conséquence pratique : pour viser un agencement connu, lister les variables dans
l'ordre décroissant des offsets voulus.

## Ce qui reste dur
Après un agencement correct, la divergence résiduelle est l'ORDONNANCEMENT des
instructions de mise en place d'arguments (la cible charge r3 puis r4, une source
C naïve fait l'inverse). C'est ce qui demande des permutations successives de la
source — le vrai coût de chaque fonction.

## Nature du code restant
Les grosses fonctions dupliquées (voir tools/find_dupes.py) sont majoritairement
du C++ à dispatch virtuel : `lwz r12,off(r3); lwz r12,slot(r12); mtctr r12; bctrl`.
Les matcher exige de reconstruire la classe et sa vtable, pas seulement la logique.
Seules 31 familles (0.147% du code) sont exemptes de vtable ET d'appel externe.
