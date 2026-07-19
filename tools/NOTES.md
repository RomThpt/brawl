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
