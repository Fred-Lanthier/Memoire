## Contexte
Mémoire en français sur la génération de trajectoires robotiques sans collision en
environnement dynamique par Flow Matching, avec un bouclier de sécurité SDF-CBF.
Dépôt : /home/flanthier/Documents/Memoire, sources dans memoire/chapters/.
Compilation : `make -C /home/flanthier/Documents/Memoire/memoire pdf`, puis vérifier
Document.log (le fichier est traité comme binaire par grep, utiliser `grep -a`).
État actuel : 208 pages, zéro erreur, zéro référence indéfinie.

## Exigences de rédaction et d'analyse (non négociables)

**Analyses extrêmement complètes, mais texte simple et fluide.** L'exhaustivité
appartient à la vérification, pas au nombre de phrases. Ouvrir chaque figure,
confronter chaque nombre à son fichier source, relire les annexes et le code avant de
conclure. C'est d'avoir tout vérifié qui donne le droit d'écrire court.

**Zéro phrase vide de sens.** Chaque phrase porte un fait, une raison ou une
conséquence. Si elle ne fait qu'annoncer, nuancer, nier ou décorer, elle saute.
Interdits explicites :
- les renversements mis en scène : « ce n'est pas X mais Y », « cette mesure ne
  justifie pas Z », « la comparaison nuance le motif ». I
  que le mémoire n'a jamais affirmé ;
- les phrases dont le seul rôle est de nier une lecture q
- les méta-phrases qui annoncent ce que la phrase suivante va dire ;
- répéter ce qu'un autre chapitre établit déjà.

**Une phrase vague cache presque toujours une affirmation
la reformuler : chercher ce qu'elle dissimule, vérifier contre les données ou le code,
puis écrire la version simple de ce qui est vrai. Rapport
proposer de la prose.

**Une réécriture ne dépasse jamais la longueur de ce qu'elle remplace.**

**Ne jamais attribuer au mémoire un motif de conception q

**Style LaTeX** : pas de tiret comme ponctuation, pas d'in
(écrire « de 4 à 10 cm »), pas de \paragraph{}, pas de \emph{}, \textit{} réservé aux
termes étrangers. Affirmations fortes conservées telles q
les erreurs mathématiques.

**Règle de fond sur les distances** : toute la boucle en
apprise. Le maillage exact est un instrument de vérificat
soustraire l'erreur du SDF de d_safe pour annoncer un dégagement physique. La
soustraction peut être nommée comme limite (§4.9 le fait correctement, sans chiffre),
jamais produire un nombre.