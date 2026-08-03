# Prompt pour Claude Opus 5 : rédaction du Chapitre 5 (Résultats)

## Mission

Rédiger les sections restantes du Chapitre 5 de mon mémoire de maîtrise, à
partir des données d'une campagne d'ablation terminée. Le chapitre est déjà
structuré et partiellement écrit : tu complètes, tu ne restructures pas.

## Contexte

Mémoire de maîtrise à Polytechnique Montréal, **en français**, sur la génération
de trajectoires robotiques sans collision en environnement dynamique par
Flow Matching, avec un filtre de sécurité SDF-CBF.

- Mémoire : `~/Documents/Memoire/`, chapitre à écrire : `memoire/chapters/7-Theme3.tex`
- Chapitre 4 (méthode, à citer sans le modifier) : `memoire/chapters/7-Theme2.tex`
- Annexes : `memoire/chapters/9-Annexes.tex`
- Compilation : `cd memoire && make pdf` (vérifie les références indéfinies
  affichées en fin de sortie)
- Le fichier `CLAUDE.md` du dépôt donne les conventions du projet, lis-le.

## Les données

**Va les chercher toi-même, ne me demande pas de chiffres.**

- Campagne alimentation : `/data/ablation_results/feeding_v3/` (9 cellules)
- Campagne saisie-dépôt et xArm7 : `/data/ablation_results/pickplace_v3/`
- Étude de sensibilité xArm7 (cube aligné sur le Panda) :
  `/data/ablation_results/xarm7_aligned/`
- Calibration de la borne de poursuite : `epsilon_calibration_all26.json`
- Perception tardive, banc alimentation : `feeding_v3/perception_lateness.json`

Chaque essai contient `outcome.json` (succès, `min_h`, `failure_kinds`, détails,
et les champs récents `n_target_clouds`, `max_target_gap_s`,
`min_window_path_rad`, `speared`, `delivered`, `food_y_max`), `reset.txt` et
`diagnostics.bag`.

Outils, tous dans `~/Github/src/vision_processing/` :

```bash
python3 ablation_campaign/aggregate.py <dossier_campagne>
python3 ablation_campaign/perception_lateness.py <dossier> --bench feeding --out <json>
python3 scripts/plot_cbf_diagnostics.py <bag> --csv --real-robot {feeding|pickplace|xarm7}
```

**IGNORE ces dossiers**, ils sont en quarantaine et documentés comme tels :
`feeding_QUARANTINE_nan_barrier_run1`, `xarm7_QUARANTINE_param_leak_run1`,
tout répertoire `_INVALIDE_*` ou `_ARTEFACTS_*`, et la cellule orpheline
`A2_softmin_value` (ablation retirée du plan, ne pas la réintroduire).

## Sections à rédiger

Elles portent toutes la mention « À compléter » ou un TODO dans le fichier.

1. `subsec:res_ab` — **tableau maître** avec et sans filtre. C'est la réponse à
   la question centrale du mémoire, toutes les autres sections y renvoient.
   Remplir aussi les `N` du Tableau `tab:res_scenarios`.
2. `subsec:res_pp_deep` — étude détaillée saisie-dépôt : une figure composite au
   maximum, un paragraphe.
3. `subsec:res_abl_persistance` — carte persistante contre nuage instantané (A8)
4. `subsec:res_abl_metrique` — métrique de tâche contre euclidienne (A1)
5. `subsec:res_abl_clearance` — dégagement postural (A3). **Ses trois
   prédictions sont écrites d'avance dans les commentaires de la matrice
   `ablation_campaign/matrix.yaml`. Confronte-les telles quelles et rapporte
   l'échec s'il y a lieu.**
6. `subsec:res_abl_reparation` — réparation de la commande filtrée (A5, A6)
7. `sec:res_xarm` — généralisation inter-embodiment, Tableau `tab:res_xarm`
8. `sec:res_echecs` — cas d'échec et limites
9. `sec:res_discussion` — synthèse transversale

Il y a aussi, dans le fichier, des TODO de cohérence de configuration à trancher
(0,25 contre 0,3 rad/s, 12 Hz contre 10 Hz, `tau_safe` 0,08 contre 0,2 s) et une
figure `fig:vel_nominal_joints` encore commentée.

## Contraintes de style, non négociables

- **Français.** Espaces insécables et virgule décimale (`0{,}5`), notation
  française des nombres.
- **Aucun tiret comme ponctuation** : ni `---`, ni `—`, ni `-` isolé. Pas de
  plages avec tiret non plus : écrire « de 4 à 10 cm », jamais « 4-10 cm ».
  Utiliser parenthèses, virgules ou deux-points.
- **Pas de `\paragraph{}` ni de `\emph{}`.** Employer `\subsection*{}` et des
  phrases d'accroche. `\textit{}` uniquement pour les termes étrangers.
- **Pas de sous-sous-sections** dans la revue de littérature ni dans 7-Theme2,
  sauf pour le frein réflexe.
- Les affirmations fortes restent **assertives**. Ne pas ajouter de prudence
  rhétorique là où le résultat est établi ; ne nuancer que si c'est une erreur
  réelle.
- Acronymes via `\ac{...}` (définis dans `chapters/4-Sigles_Abrev.tex`).
- Figures : SVG produits par `thesis_style.py`, palette Okabe-Ito, en français,
  sans titre interne.

## Honnêteté scientifique, à respecter impérativement

Ces réserves sont **mesurées**, pas hypothétiques. Le texte doit les porter.

1. **L'artefact du `h` publié.** Le nœud publie parfois un `h` faux, alternant
   d'un cycle à l'autre, pendant que la géométrie ne bouge pas. Vérifié contre
   `h_real` (maillages exacts, cinématique directe indépendante) : un épisode
   rapportait −20,28 mm avec 17,3 mm de dégagement réel, un autre −10,33 mm avec
   **1,25 m** de dégagement réel. **Aucun chiffre d'une colonne `h*` ne doit
   être publié pour un épisode où `h` passe sous zéro sans avoir été vérifié au
   `h_real`.** La cause reste inconnue.
2. **Dérive au fil de la cellule.** Le taux de succès baisse entre la première
   et la seconde moitié de chaque cellule du banc alimentation (20 à 40 points)
   et s'effondre sur xArm7. Le pick-place Panda est stable. Les colonnes de
   succès et de temps de complétion de ces cellules sont donc biaisées vers le
   bas ; `h*` n'est pas affecté. À mentionner dans les limites.
3. **Colonne collisions.** Le juge à maillages exacts est trop lent à l'échelle
   de la campagne. Le critère de collision est approximé par la barrière `h`.
   **Le texte doit le dire explicitement**, plutôt que de laisser croire à une
   mesure sur maillages.
4. **La sphère de S5 est purement virtuelle**, sans modèle de collision. Un
   franchissement y est une violation de barrière, jamais un contact physique.
   Ne pas décrire S5 comme un scénario de contact.
5. **La cellule sans bol** utilise un critère de complétion différent (livraison
   à y ≥ 0,40 m au lieu de l'extraction au-dessus du rebord). Son taux de succès
   **ne se compare pas** à celui des cellules avec bol. Elle sert de référence
   de transparence du filtre.
6. **xArm7** : le cube est 5 cm plus près que pour le Panda, pour compenser une
   portée plus courte. Une étude de sensibilité avec le cube aligné existe dans
   `xarm7_aligned/` et doit être citée si le taux de succès est commenté.
7. **Graines 31 et 32 retirées** (elles déclenchaient l'artefact), remplacées
   par 5 et 6. Deux essais sur trente ne sont donc pas appariés entre les
   cellules anciennes et récentes.

## Méthode de travail attendue

1. Lis d'abord `7-Theme3.tex` en entier, puis les sections du Chapitre 4 qu'il
   cite. Le chapitre annonce des promesses précises ; ton travail est de les
   tenir, pas d'en inventer d'autres.
2. Agrège les données toi-même avant d'écrire une seule phrase.
3. Pour chaque ablation, respecte le gabarit déjà en place : la décision de
   conception validée, le résultat agrégé, le constat. Une page chacune.
4. Vérifie tes chiffres deux fois. Si une donnée manque, dis-le au lieu de
   l'estimer.
5. Compile après chaque section (`make pdf`) et vérifie l'absence de référence
   indéfinie.

## Hors périmètre

Ne rédige pas d'ablation soft-min contre valeur exacte : elle a été retirée du
plan, le soft-min existant pour rendre le gradient analytique traitable et non
comme alternative de conception. La promesse correspondante a déjà été retirée
du Chapitre 4.
