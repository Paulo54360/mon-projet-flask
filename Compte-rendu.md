# Compte-rendu TP3 - Qualite de code

## Contexte du projet

Projet Flask avec pipeline CI GitHub Actions, tests Pytest, couverture avec `pytest-cov`, analyse SonarCloud, hooks pre-commit, et outils qualite/securite (`black`, `ruff`, `bandit`, `semgrep`).

## Reponses aux 12 questions

### Question 1 - Difference linter vs formatter

Un **formatter** reecrit le code automatiquement pour appliquer un style coherent (espaces, retours a la ligne, etc.) sans changer la logique.
Un **linter** analyse le code pour detecter erreurs potentielles, mauvaises pratiques et incoherences.

- Exemple formatter Python : `black`
- Exemple linter Python : `ruff`

### Question 2 - Pourquoi `--check` dans la CI

On utilise `black --check` en CI pour **verifier** le formatage sans modifier le code du depot a distance.
Le formatage doit etre fait localement avant commit (developpeur ou hook), sinon la CI changerait du code "dans le dos" de l'auteur et casserait la tracabilite des commits.

### Question 3 - Avantages Ruff et interet de `pyproject.toml`

Ruff est tres rapide et couvre plusieurs familles de regles dans un seul outil. Dans ce projet, le lint est gere uniquement par Ruff.
Dans ce projet, `pyproject.toml` centralise la config (`line-length`, `target-version`, categories actives), ce qui rend les executions locales/CI coherentes et versionnees.

### Question 4 - Difference Bandit vs Semgrep

- **Bandit** : specialise Python securite, base sur des patterns de vulnerabilites Python frequentes.
- **Semgrep** : moteur multi-langage, regles communautaires + regles custom metier.

Dans ce projet :
- Bandit couvre bien les anti-patterns Python.
- Semgrep apporte les regles `auto` + une regle personnalisee (`.semgrep/custom-rules.yml`).

### Question 5 - Analyse statique vs tests unitaires

L'analyse statique inspecte le code **sans execution** pour detecter odeurs, erreurs probables et failles.
Les tests unitaires executent le code pour verifier des comportements attendus.

Elles sont complementaires :
- analyse statique => prevention en amont
- tests => validation fonctionnelle

### Question 6 - Interet des pre-commit hooks vs CI

Les hooks pre-commit donnent un feedback immediat avant commit (rapide, local, economise des runs CI).
La CI reste indispensable pour une verification centralisee, reproductible et non contournable sur PR.

Utiliser les deux permet de filtrer tot + garantir cote serveur.

### Question 7 - `git commit --no-verify`, probleme ?

Oui, c'est un risque : cette option contourne les hooks locaux.
Un code non conforme peut etre commite, mais la CI doit encore bloquer en remote.
En equipe, ce contournement doit rester exceptionnel (depannage), jamais une pratique normale.

### Question 8 - Definition d'un Quality Gate + 3 exemples

Un Quality Gate est un seuil minimum de qualite qui conditionne le passage du pipeline.

Exemples :
1. Couverture minimale >= 70% (`--cov-fail-under=70`)
2. Zero erreur lint bloquante (`ruff check`)
3. Zero issue securite critique (Bandit/Semgrep en mode echec)

### Question 9 - Ordre des verifications et importance

Ordre actuel dans `/.github/workflows/ci.yml` :
1. Installation dependances
2. Formatage (`black --check`)
3. Lint (`ruff check`)
4. Securite (`bandit`, puis `semgrep`)
5. Tests + couverture (quality gate 70%)
6. Rapport XML + scan SonarCloud

Cet ordre est pertinent : on echoue vite sur les checks peu couteux (style/lint/securite) avant de lancer les etapes plus lourdes (tests, Sonar).

### Question 10 - Tableau de bord SonarCloud du projet

Elements visibles/constates sur le projet :
- Projet lie a SonarCloud (`sonar.projectKey=Paulo54360_mon-projet-flask`)
- Analyse lancee depuis GitHub Actions
- Security Hotspot traite sur le pin SHA de l'action Sonar

Etat Quality Gate actuel :
- Echec observe tant que **Automatic Analysis** est active en parallele de l'analyse CI.
- Action a faire sur SonarCloud : desactiver `Automatic Analysis` pour n'utiliser que la CI.

### Question 11 - SonarCloud vs outils locaux

Bandit/Semgrep/Ruff sont excellents localement et en CI, mais SonarCloud apporte une vue centralisee :
- tableau de bord unique (bugs, smells, securite, couverture)
- historique des tendances qualite
- quality gate global projet/PR
- gouvernance equipe (visibilite, priorisation, suivi)

En entreprise, cette centralisation facilite le pilotage qualite a l'echelle.

### Question 12 - Regles Ruff ajoutees (partie 7.1)

Categories ajoutees dans `pyproject.toml` (activees via Ruff) :
- `C4` (famille de regles "comprehensions" dans Ruff)
- `SIM` (famille de regles "simplify" dans Ruff)

Liens documentation :
- https://docs.astral.sh/ruff/rules/

Pourquoi ces choix :
- `C4` force des constructions Python plus idiomatiques et lisibles.
- `SIM` reduit la complexite inutile et simplifie des structures conditionnelles.

Resultat sur le code actuel :
- aucune erreur supplementaire detectee apres activation (`ruff check src/ tests/` passe).

## Partie 7 - Recherche autonome realisee

### 7.1 Regles Ruff supplementaires

Ajout de `C4` et `SIM` dans `pyproject.toml`, verification `ruff` OK.

### 7.2 Regle Semgrep personnalisee

Fichier cree : `/.semgrep/custom-rules.yml`

Regle : `flask-no-print-in-production`
- but : interdire `print(...)` dans `src/**/*.py`
- severite : `ERROR`

Test :
- commande `semgrep --config .semgrep/custom-rules.yml src/`
- resultat : 0 finding sur l'etat actuel

Integration CI :
- step Semgrep mis a jour pour charger la config auto + custom :
  `semgrep --config auto --config .semgrep/custom-rules.yml --error src/`

## Verification checklist de rendu

- [x] Formatage black configure et verifie en CI
- [x] Ruff configure via `pyproject.toml`
- [x] Bandit et Semgrep integres au pipeline
- [x] Pre-commit hooks installes/configures (`.pre-commit-config.yaml`, execution visible lors des commits)
- [x] Quality Gate couverture minimum 70% (`--cov-fail-under=70`)
- [x] SonarCloud connecte (projet analyse), tableau de bord accessible
- [ ] Pipeline CI complet et vert (reste a desactiver Automatic Analysis SonarCloud pour lever l'echec)
- [x] PR mergee avec checks passes (historique git : merge PR visible)
- [x] Regles Ruff supplementaires activees (C4, SIM)
- [x] Compte-rendu avec reponses aux 12 questions

## Action finale recommandee avant rendu

Dans SonarCloud, desactiver **Automatic Analysis** sur le projet, puis relancer la CI pour obtenir un pipeline totalement vert.
