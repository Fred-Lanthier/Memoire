# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A master's thesis (mémoire de maîtrise) at Polytechnique Montréal, written in **French**, on collision-free robotic trajectory generation in dynamic environments using Flow Matching models. It uses the official Polytechnique bilingual LaTeX template (`MemoireThese.sty`). All thesis content must be written in French (the Abstract chapter is the English exception).

## Building

All build commands run from the `memoire/` directory:

```bash
cd memoire
make pdf        # Compile Document.tex → Document.pdf (pdflatex + bibtex, reruns as needed)
make clean      # Remove LaTeX auxiliary files (incl. chapters/*.aux)
make help       # List all targets
```

The Makefile handles the pdflatex/bibtex rerun loop automatically and prints any remaining undefined references/citations at the end — check that output after building. Compilation uses `-shell-escape` (required by the `svg` package, which also requires Inkscape installed).

The VS Code LaTeX Workshop config (`.vscode/settings.json`) builds via this same `make pdf` recipe on file change.

## Structure

- `memoire/Document.tex` — root document. Rarely needs editing; it sets the language (`\newcommand\Langue{french}`) and `\include`s the chapters in order. Don't restructure it.
- `memoire/0-Definitions_Etudiant.tex` — student metadata: title, author, jury, keywords, degree, deposit date.
- `memoire/chapters/` — one file per chapter, numbered by front-to-back order:
  - `5-Introduction.tex`, `6-Revue_litterature.tex` (literature review)
  - `7-Theme1.tex` (solution details), `7-Theme2.tex` (results), `7-Theme3.tex`
  - `8-Conclusion.tex`, `9-Annexes.tex`, plus dedication/acknowledgements/abstracts/acronyms (1–4)
- `memoire/Document.bib` — bibliography, formatted with `IEEEtran-francais.bst` (French IEEE style).
- `memoire/images/` — figures (searched via `\graphicspath`, along with `dia/` and `gnuplot/`); results figures live in `images/Results/`.
- `memoire/MemoireThese.sty` and `memoire/modules/` — Polytechnique template internals; do not modify.

## Conventions

- Acronyms use the `acronym` package (`\ac{...}`), defined in `chapters/4-Sigles_Abrev.tex`.
- Generated artifacts (`Document.pdf`, `.aux`, `.bbl`, `.lof`, `.lot`, etc.) are partly tracked in git despite `.gitignore`; expect them to show as modified after a build.
