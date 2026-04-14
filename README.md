# TP2 - Integration Continue avec GitHub Actions (Flask)

![CI](https://github.com/VOTRE-USER/mon-projet-flask/actions/workflows/ci.yml/badge.svg)

Ce projet implemente le TP2 d'Usine Logicielle (M1 DevOps) avec :
- une API Flask simple ;
- des tests automatises avec `pytest` ;
- un pipeline GitHub Actions complet (lint, tests, couverture, artefact, cache).

## 1) Prerequis

- Python 3.12+ installe
- Compte GitHub
- Git installe

## 2) Structure du projet

```text
mon-projet-flask/
├── .github/workflows/ci.yml
├── src/
│   ├── __init__.py
│   └── app.py
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── .gitignore
├── README.md
└── requirements.txt
```

## 3) Installation et lancement local

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/app.py
```

Tester les routes :
- `GET /`
- `GET /health`
- `GET /hello/Alice`
- `GET /add/3/5`
- `GET /about`

## 4) Lancer les verifications en local

```bash
flake8 src/ tests/ --max-line-length=120
pytest --cov=src --cov-report=term --cov-report=html:coverage-report -v
```

## 5) Etapes Git/GitHub a suivre (pas a pas)

### Etape A - Creation et premier push

```bash
git init
git add .
git commit -m "feat: initialisation projet Flask + tests + CI"
git branch -M main
git remote add origin https://github.com/VOTRE-USER/mon-projet-flask.git
git push -u origin main
```

### Etape B - Verifier la CI

1. Ouvrir GitHub > onglet **Actions**.
2. Verifier que le workflow `CI Pipeline` tourne.
3. Telecharger l'artefact `coverage-report` a la fin du run.

### Etape C - Protection de la branche main

1. Ouvrir `Settings > Branches > Add branch protection rule`.
2. `Branch name pattern` : `main`.
3. Cocher :
   - `Require a pull request before merging`
   - `Require status checks to pass before merging`
4. Selectionner le check du workflow CI.

### Etape D - Flux de travail quotidien

```bash
git checkout -b feature/ma-fonctionnalite
# coder + tester localement
flake8 src/ tests/ --max-line-length=120
pytest -v
git add .
git commit -m "feat: ma fonctionnalite"
git push -u origin feature/ma-fonctionnalite
```

Ensuite :
1. Ouvrir une Pull Request vers `main`.
2. Attendre CI verte.
3. Merger la PR.

## 6) Reponses au compte-rendu (Q1 a Q10)

### Q1 - Structure de `ci.yml`
- `on` : definit les evenements declencheurs (`push`, `pull_request`).
- `jobs` : liste les taches a executer.
- `runs-on` : definit l'environnement d'execution (runner).
- `steps` : sequence des actions/commandes.
- `uses` : reutilise une action existante (Marketplace ou officielle).

### Q2 - Role de la fixture `client`
La fixture prepare un client de test Flask isole pour chaque test.  
`app.test_client()` simule des requetes HTTP sans demarrer un vrai serveur, ce qui rend les tests plus rapides, stables et simples a automatiser en CI.

### Q3 - Pourquoi tester localement avant push
Tester localement permet de detecter les regressions plus vite et d'eviter des runs CI inutiles.  
Si un test echoue en CI, le pipeline passe en rouge et (avec protection) le merge vers `main` est bloque.

### Q4 - Qu'est-ce qu'un artefact GitHub Actions
Un artefact est un fichier (ou dossier) produit par un workflow et conserve apres le run.  
Exemples :
1. rapport de couverture HTML ;
2. binaire/package de build ;
3. rapport de tests (`junit.xml`).

### Q5 - Couverture de code
La couverture mesure la part du code executee par les tests.  
`100%` n'est pas toujours souhaitable si cela force des tests artificiels peu utiles ; la qualite des assertions et la pertinence fonctionnelle comptent plus qu'un score maximal.

### Q6 - Role du linter et ordre dans pipeline
Le linter detecte les problemes de style/qualite statique (PEP8, imports, etc.).  
Le lancer avant les tests permet d'echouer rapidement ("fail fast") et d'economiser du temps de CI.

### Q7 - Fonctionnement du cache GitHub Actions
Le cache reutilise des donnees entre runs (ici le cache `pip`) grace a une cle.  
Si `requirements.txt` change, le hash change, donc un nouveau cache est cree (ancien cache potentiellement reutilisable via `restore-keys` partiel).

### Q8 - GitHub-hosted vs self-hosted runners
- **GitHub-hosted** : simple, pret a l'emploi, maintenance minimale, mais moins personnalisable.
- **Self-hosted** : controle total (reseau interne, outils specifiques), potentiellement moins cher a grande echelle, mais maintenance/securite a votre charge.
- **Quand utiliser** : GitHub-hosted pour la majorite des projets ; self-hosted pour contraintes reseau, securite stricte, ou besoins d'infrastructure specifiques.

### Q9 - Workflow developpeur avec `main` protegee
1. Creer une branche feature.
2. Developper et tester localement.
3. Pousser la branche et ouvrir une PR.
4. CI s'execute automatiquement.
5. Corriger jusqu'a CI verte.
6. Revue/approbation.
7. Merge vers `main`.

### Q10 - Recherche autonome (exemple d'action Marketplace)
Action proposee : `EnricoMi/publish-unit-test-result-action`  
Lien : https://github.com/marketplace/actions/publish-test-results  
Role : publier un resume lisible des resultats de tests dans la PR.  
Resultat attendu : visibilite immediate des tests passes/echoues sans ouvrir tous les logs.

Exemple d'ajout YAML :
```yaml
- name: Publier les resultats de tests
  uses: EnricoMi/publish-unit-test-result-action@v2
  if: always()
  with:
    files: test-results.xml
```

## 7) Checklist de validation TP

- [x] Application Flask avec au moins 5 routes (`/`, `/health`, `/hello/<name>`, `/add/<int:a>/<int:b>`, `/about`)
- [x] Pipeline CI complet (lint + tests + couverture + artefacts + cache)
- [x] Au moins 7 tests qui passent (via parametrization et tests de routes)
- [x] Badge CI dans le README (a personnaliser avec votre user GitHub)
- [ ] Branche `main` protegee sur GitHub
- [ ] PR creee et mergee avec CI verte
- [ ] Action Marketplace integree et testee
