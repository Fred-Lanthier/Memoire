# Règles de Rédaction et de Style du Mémoire

## Contexte
Mémoire de maîtrise en génie informatique / robotique sur la génération de trajectoires robotiques sans collision en environnement statique par *Flow Matching*, sécurisées par un bouclier de sécurité réactif SDF-CBF et un frein réflexe à 1 kHz.
- **Dépôt** : `/home/flanthier/Documents/Memoire`
- **Sources** : `memoire/chapters/`
- **Compilation** : `make -C /home/flanthier/Documents/Memoire/memoire pdf` ou `pdflatex -interaction=nonstopmode -shell-escape Document.tex`

---

## 1. Principes d'Écriture (Non Négociables)

### **Simplicité, Limpidité et Fluidité (Refus du "AI Speak" et du théâtralisme)**
- Le style doit être fluide, direct, naturel et sobre.
- Interdiction absolue d'effets théâtraux, d'envolées lyriques ou de métaphorique administrative (ex. *« L'interprétation s'incline devant... »*, *« ultime réserve méthodologique »*, *« cadre contrôlé d'une grande rigueur »*).
- Écrire court, simple et factuel. L'exhaustivité appartient à la vérification préalable des données, pas à la surcharge des phrases.

### **Rigueur et Vérité Technique Explicite**
- Ne jamais masquer un problème ou une anomalie sous une formule vague ou dramatique (ex. interdiction absolue d'écrire *« dérive de protocole non identifiée »* ou *« cause inconnue »*).
- Toujours expliciter la cause géométrique, physique ou algorithmique réelle (ex. le décalage de $5\text{ cm}$ du cube + pose initiale de pince constante $\implies$ politique générative hors distribution OOD $\implies$ arbitrage CBF priorisant la sécurité $\implies 14$ échecs de préhension).
- Distinguer strictement le rôle du **frein réflexe à 1 kHz** (qui gère la queue de latence du bouclier QP $> 20\text{ ms}$) de la **saturation du budget de sélection des $K$ points** (qui a causé l'unique franchissement de marge sur le croissant, la marge statique $d_{\mathrm{safe}} = 15\text{ mm}$ évitant tout contact physique).

### **Zéro Phrase Vide de Sens**
- Chaque phrase porte un fait précis, une raison technique ou une conséquence mesurée. Si elle ne fait qu'annoncer, nuancer la prose, ou répéter ce qu'un autre chapitre établit déjà, elle doit être supprimée.
- Interdiction des méta-phrases d'annonce (ex. *« Quatre réserves bornent ces conclusions et seront reprises en conclusion... »*).
- Interdiction des mises en scène négatives (ex. *« ce n'est pas X mais Y »*, *« cette mesure ne justifie pas Z »*).

---

## 2. Règles de Formatage et de Typos LaTeX

### **Mise en Forme Inline (Typographie)**
- **Zéro `\textbf{}` et zéro `\emph{}` dans le texte** : Le gras et l'emphase visuelle ne doivent jamais être utilisés dans le corps de texte (donne un aspect artificiel et "généré par IA").
- **`\textit{}` strictement réservé** aux seuls termes étrangers (ex. *Flow Matching*, *in-distribution*, *out-of-distribution*). Aucun mot français ne doit être mis en italique pour créer de l'emphase.
- **Interdiction des parenthèses `(...)` dans la prose** : Remplacer les incises entre parenthèses par des tournures fluides intégrées naturellement dans la phrase.

### **Ponctuation et Structure LaTeX**
- Pas de tirets courts comme ponctuation d'incise (utiliser des virgules ou des propositions subordonnées).
- Pas de tirets dans les intervalles numériques : écrire « de 4 à 10 cm » et non « 4-10 cm ».
- Pas d'utilisation de `\paragraph{}` dans le texte des chapitres.

---

## 3. Règles de Fond sur les Mesures et la Géométrie

### **Distances et Validation Géométrique**
- Toute la boucle de filtrage en temps réel repose sur le champ de distance signée (SDF) appris par polynômes de Bernstein.
- Le maillage géométrique exact est uniquement un instrument de vérification *a posteriori* appliqué cycle par cycle sur 100 % des épisodes.
- Ne jamais soustraire l'erreur d'apprentissage du SDF de la marge statique $d_{\mathrm{safe}}$ pour calculer un dégagement physique fictif. La marge $d_{\mathrm{safe}} = 15\text{ mm}$ absorbe l'erreur en régime établi.

### **Concision des Réécritures**
- Une réécriture de correction ou de clarification ne doit jamais dépasser la longueur du paragraphe qu'elle remplace.
- Préférer la condensation factuelle à l'extension explicative.