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

## Première famille matchée (sora_enemy fn_41_3B948, 104o x4)
Cascade de comparaisons retournant `p + offset` (offsets 32 + 44*i, testés en
ordre DÉCROISSANT 5..0). Transcrite littéralement en chaîne de `if` dans le même
ordre décroissant que l'assembleur -> match au premier essai.

Enseignement : quand l'assembleur teste les cas en ordre décroissant, écrire la
chaîne de `if` dans CE même ordre. Ne pas "normaliser" en ordre croissant ni en
`switch` : le compilateur produirait une table de saut ou un autre agencement.

Les fonctions SANS pile ni appel (pas de stwu/mflr) sont de loin les plus faciles :
aucun ordonnancement d'arguments à faire coïncider. Les privilégier.

## Stratégie qui marche : main -> motif -> automatisation
Les deux familles accesseurs décompilées à la main partageaient une forme
formulaire. Plutôt que d'en faire une troisième à la main, écrire un détecteur
(tools/bank_accessors.py) a matché les 455 restantes sans effort : 457 fonctions
d'un coup, toutes correctes au premier build.

Méthode à répéter : décompiler à la main jusqu'à reconnaître une forme récurrente,
puis mécaniser la reconnaissance. Chercher les motifs formulaires (accesseurs,
thunks, wrappers générés par macro/template) avant de s'attaquer aux fonctions
uniques.

## Où en est le gisement
- Familles feuilles (sans pile/vtable/reloc) : ~21, presque épuisées maintenant.
- Le reste des 853 familles est du C++ à vtables -> reconstruction de classe.
- Prochaines pistes de motifs formulaires à chercher : thunks de vtable,
  wrappers de setters, constructeurs triviaux répétés entre modules.

## Thunks d'appel virtuel : NON mécanisables en C (échec documenté)
Forme : `lwz r12,OFF1(r3) ; lwz r12,OFF2(r12) ; mtctr r12 ; bctr` (~1300 occurrences).

Tentatives en C via pointeur de fonction : la structure et la taille sont exactes,
mais la COULEUR DE REGISTRE diffère.
- intermédiaire en variable locale -> r4
- expression inlinée -> r4
- registres d'arguments occupés (params transmis au saut terminal) -> r11

La cible réutilise r12 pour les DEUX chargements : c'est le chemin de génération
des appels virtuels C++ de MWCC, qui écrase r12 parce que le pointeur de vtable
meurt immédiatement. Le C ne permet pas de forcer cette réutilisation.

Conclusion : ce motif exige de vraies méthodes virtuelles C++ (donc la classe et
sa vtable). À laisser de côté tant qu'on n'a pas les définitions de classes.

Enseignement général : quand la structure est exacte mais la couleur de registre
diverge, c'est le signe d'un idiome du compilateur qu'on n'atteint pas depuis le
langage utilisé — changer de langage (C -> C++) ou passer au motif suivant.

## Index circulaires (bank_wrapidx.py) — 440 fonctions
Forme : curseur stocké dans un champ, décalé par l'argument, ramené dans [0,N),
puis adresse de l'élément. Tous les constants (offset, décalage, N, taille
d'élément, base) se lisent dans les instructions.

Piège rencontré : mon désassembleur décodait `bc` sans tenir compte de BI, donc
affichait `beq` là où c'était `blt`. J'ai écrit `if (idx != 4)` au lieu de
`if (idx >= 4)` et 9 instructions sur 10 matchaient. Corrigé dans disasm.py.
Leçon : quand une seule instruction diverge et que c'est un branchement,
soupçonner d'abord le décodage de la condition.

## Bug qui coûtait 2400 fonctions : champs de srawi inversés
`srawi rA, rS, SH` encode la DESTINATION en rA (bits 20-16) et la SOURCE en rS
(bits 25-21) — l'inverse de l'intuition. Mon classifieur exigeait rS=3/rA=0 au
lieu de rS=0/rA=3, donc rejetait silencieusement TOUS les getters signés.

Symptôme : le générateur "marchait" (les fonctions bankées matchaient) mais
rendait beaucoup moins que le comptage ne le prévoyait. Quand un générateur
produit moins que le gisement mesuré, suspecter ses conditions de REJET avant de
conclure que le gisement est épuisé.

Formes bitfield gérées au final :
- lwz + rlwimi + stw           -> p->f = v
- lwz + rlwinm + srawi         -> return p->f (signé)
- lwz + srawi                  -> return p->f (signé, champ en tête de mot)
- lwz + rlwinm                 -> return p->f (non signé)
- lwz + rlwinm(SH=0, MB>ME) + stw -> p->f = 0 (masque inversé : le champ effacé
  est [ME+1 .. MB-1])

## Destructeurs "deleting" : NON écrivables à la main (échec documenté)
Forme (2357x en 92o + 1520x en 96o, ~2.3% du code) :
    if (this) { real_dtor(this, 0); if ((short)flag > 0) operator delete(this); }
    return this;
avec `__dl__FPv` = operator delete dans le DOL.

Transcrit en C, le résultat fait 88 octets au lieu de 92 : le compilateur garde
`this` dans r3 alors que la cible le recharge depuis r30, et il ordonne les
sauvegardes différemment. Deux variantes essayées, la seconde pire (2/23).

Raison de fond : cette fonction est SYNTHÉTISÉE par MWCC à partir de la classe
(c'est le "deleting destructor" que le compilateur émet à côté du destructeur
réel). Elle n'est pas écrite par le programmeur, donc pas reproductible en
l'écrivant à la main — il faut définir la classe C++ et laisser le compilateur
l'émettre.

## Constat sur le plafond de l'approche "motifs"
Les gisements restants les plus gros sont tous des constructions SYNTHÉTISÉES
par le compilateur C++ :
- destructeurs deleting (2357x + 1520x, ~2.3% du code)
- thunks d'appel virtuel (~1300x, r12 réutilisé)
Aucun n'est atteignable en écrivant du C. Ils exigent les définitions de classes
(membres aux bons offsets, méthodes virtuelles aux bons slots), c'est-à-dire le
travail de fond d'un projet de décompilation C++.

Ce qui reste mécanisable en C est essentiellement épuisé : accesseurs d'index,
champs de bits, index circulaires (~4300 fonctions matchées au total).

## Getters de globaux (bank_globals.py) — 726 fonctions
`lis+lfs+blr` -> return SYM ; `lis+addi+blr` -> return &SYM.
Les immédiats sont nuls dans le .rel : l'adresse arrive par une paire de
relocations, type 6 (ADDR16_HA) sur le lis et type 4 (ADDR16_LO) sur
l'instruction suivante, portant section et offset cible. ATTENTION : la
relocation est à instruction+2 (elle patche le demi-mot bas).
Mapping section REL -> nom : 1=.text 2=.ctors 3=.dtors 4=.rodata 5=.data 6=.bss.

64 unités sur 9 modules (ft_falco, ft_gamewatch, ft_link, ft_luigi, ft_mario,
ft_pit, ft_samus, ft_snake, ft_toonlink) ne matchaient pas et ont été retirées ;
le reste tient. Cause non élucidée — probablement un symbole cible différent de
celui déduit (plusieurs symboles à la même adresse, ou un alias). À revoir si on
veut ces 64.

Méthode de récupération après un lot partiellement cassé : identifier les RELs en
échec dans la sortie ninja, retirer sélectivement les unités de ces modules
(splits.txt + Object dans configure.py + fichiers src), rebuilder. Bien plus
rapide que de tout jeter.

## 9 modules qui refusent les getters de globaux (non élucidé)
ft_falco, ft_gamewatch, ft_link, ft_luigi, ft_mario, ft_pit, ft_samus, ft_snake,
ft_toonlink rejettent systématiquement ces unités.

Diagnostic poussé : le .text produit est BYTE-IDENTIQUE à la cible (vérifié
instruction par instruction sur ft_mario). Le build rapporte "126 files OK" avec
seulement ft_mario.rel en écart. L'écart est donc dans la table de relocations du
REL, pas dans le code — probablement parce que le symbole déduit de
(section, offset) n'est pas celui qu'utilisait l'original (alias, ou plusieurs
symboles à la même adresse dont le linker choisit un autre).

Écartés via une liste SKIP dans bank_globals.py. ~164 unités en jeu.

Enseignement : un .text identique ne garantit pas un REL identique. Quand le code
matche mais que le module échoue, regarder du côté des relocations et des
symboles référencés, pas du code généré.

## Hygiène : entrées orphelines
Des grinds interrompus laissent des entrées dans splits.txt sans Object
correspondant dans configure.py (warning "Missing configuration for ..."). Elles
ne cassent pas le build mais polluent. Nettoyage : chercher les chemins présents
dans un splits.txt et absents de configure.py, et les retirer.

## Sauts cross-module (555x) : bloqués par les noms mangés C++
Forme : mélange d'arguments puis `b` vers un autre module. La cible se résout via
la relocation type 10 (REL24) qui donne module_id + offset, puis le symbols.txt
du module cible.

Exemple résolu : sora_melee .text+0xD4104 =
`addObserverSub__41soEventObserver<22soAnimCmdEventObserver>FlP22soAnimCmdEventObserverSc`

Le nom contient `<` et `>` : ce n'est pas un identifiant C valide, donc impossible
à déclarer en extern depuis un fichier C. Il faudrait écrire l'unité en C++ et
reconstruire le template pour que le compilateur produise ce mangling — donc
retour au problème des classes.

Enseignement : vérifier la VALIDITÉ du nom de symbole cible avant d'investir dans
un motif à appel externe. Les symboles de templates C++ sont hors de portée du C.
