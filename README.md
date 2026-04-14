![CI](https://github.com/paulo54360/mon-projet-flask/actions/workflows/ci.yml/badge.svg)

# Mon projet Flask

Application Flask realisee pour le TP2 d'integration continue (Usine Logicielle), avec pipeline GitHub Actions complet.

## Fonctionnalites API

Routes disponibles :
- `/` : message de bienvenue
- `/health` : etat de sante de l'API
- `/hello/<name>` : message personnalise
- `/add/<a>/<b>` : addition de deux entiers (positifs ou negatifs)
- `/about` : informations sur l'application

## Installation et lancement local

```bash
pip install -r requirements.txt
python src/app.py
```

## Pre-commit (qualite avant commit)

Installation des hooks :

```bash
pre-commit install
```

Execution manuelle sur tout le projet :

```bash
pre-commit run --all-files
```

Les hooks verifies ici :
- qualite des fichiers YAML
- suppression des espaces/trailing whitespace
- fin de fichier correcte
- linting `flake8`

## Docker (build local)

Construire l'image :

```bash
docker build -t mon-projet-flask:local .
```

Lancer le conteneur :

```bash
docker run --rm -p 5000:5000 mon-projet-flask:local
```

## Qualite et tests

```bash
flake8 src/ tests/ --max-line-length=120
pytest --cov=src --cov-report=term --cov-report=html:coverage-report -v
```

Le rapport de couverture HTML est genere dans `coverage-report/`.

## Pipeline CI (GitHub Actions)

Workflow : `.github/workflows/ci.yml`

Le pipeline execute automatiquement sur `push` et `pull_request` vers `main` :
- pre-commit hooks
- linting (`flake8`)
- build de verification (`python -m compileall src`)
- build Docker (`docker build`)
- tests (`pytest`)
- couverture (`pytest-cov`)
- upload de l'artefact `coverage-report`
- publication des resultats de tests sur PR via l'action Marketplace `EnricoMi/publish-unit-test-result-action@v2`

## Notions du cours couvertes dans ce TP

Ce projet applique les notions presentes dans le cours "Integration Continue Course.pdf" :

- **CI (integration frequente)** : verification automatique a chaque `push` et `pull_request` sur `main`.
- **Pipeline par etapes** : checkout -> install -> lint -> build -> test -> report.
- **Fail fast** : le lint est execute avant les tests pour echouer rapidement en cas de probleme de qualite.
- **Runner GitHub-hosted** : execution sur `ubuntu-latest`.
- **Actions reutilisables (Marketplace)** : `actions/checkout`, `actions/setup-python`, `actions/cache`, `actions/upload-artifact`, `EnricoMi/publish-unit-test-result-action`.
- **Versionning des actions** : actions epinglees avec version (`@v4`, `@v5`, `@v2`) comme recommande.
- **Pre-hook qualite** : hooks `pre-commit` executes localement avant commit et verifies aussi dans la CI.
- **Tests automatises avec pytest** : tests de routes Flask, fixture `client`, assertions explicites.
- **Parametrization pytest** : test `@pytest.mark.parametrize` sur la route `/add`.
- **Build Docker** : image construite en CI pour valider la phase build du pipeline.
- **Couverture de code** : `pytest-cov` + rapport terminal et HTML.
- **Artefacts** : publication du dossier `coverage-report` dans GitHub Actions.
- **Cache des dependances** : cache pip base sur le hash de `requirements.txt`.
- **Qualite de code** : linting `flake8` dans le pipeline.
- **Badge CI** : indicateur d'etat du pipeline en tete du README.
- **Protection de branche (processus GitHub)** : merge via PR avec checks CI requis.

## Liens utiles (cours)

- Documentation GitHub Actions : [https://docs.github.com/actions](https://docs.github.com/actions)
- Marketplace GitHub Actions : [https://github.com/marketplace?type=actions](https://github.com/marketplace?type=actions)
- Documentation pytest : [https://docs.pytest.org](https://docs.pytest.org)
