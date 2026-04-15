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
- linting `ruff`

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
black --check src/ tests/
ruff check src/ tests/
pytest --cov=src --cov-report=term --cov-report=html:coverage-report -v
```

Le rapport de couverture HTML est genere dans `coverage-report/`.

## Securite

Ce projet integre les verifications de securite suivantes :
- **GitLeaks** : detection de secrets dans le code et l'historique Git
- **pip-audit** : scan des CVE dans les dependances Python
- **Bandit** : analyse de securite du code Python
- **Semgrep** : detection de patterns dangereux
- **Dependabot** : mises a jour automatiques des dependances et actions GitHub

## Pipeline CI (GitHub Actions)

Workflow : `.github/workflows/ci.yml`

Le pipeline execute automatiquement sur `push` et `pull_request` vers `main` :
- detection de secrets (GitLeaks)
- verification formatage (`black`)
- linting (`ruff`)
- scan dependances (`pip-audit`)
- securite applicative (`bandit` + `semgrep`)
- tests (`pytest`) + couverture (`pytest-cov`, seuil 70%)
- upload de l'artefact `coverage-report`
- scan SonarCloud

## Notions du cours couvertes dans ce TP

Ce projet applique les notions presentes dans le cours "Integration Continue Course.pdf" :

- **CI (integration frequente)** : verification automatique a chaque `push` et `pull_request` sur `main`.
- **Pipeline par etapes** : checkout -> scans securite -> qualite -> tests -> report.
- **Fail fast** : GitLeaks et les verifications qualite/sécurité echouent avant les tests lourds.
- **Runner GitHub-hosted** : execution sur `ubuntu-latest`.
- **Actions reutilisables (Marketplace)** : `actions/checkout`, `actions/setup-python`, `actions/cache`, `actions/upload-artifact`, `gitleaks/gitleaks-action`, `SonarSource/sonarqube-scan-action`.
- **Versionning des actions** : actions epinglees avec version (`@v4`, `@v5`, `@v2`) comme recommande.
- **Pre-hook qualite** : hooks `pre-commit` executes localement avant commit et verifies aussi dans la CI.
- **Tests automatises avec pytest** : tests de routes Flask, fixture `client`, assertions explicites.
- **Parametrization pytest** : test `@pytest.mark.parametrize` sur la route `/add`.
- **Couverture de code** : `pytest-cov` + rapport terminal et HTML.
- **Artefacts** : publication du dossier `coverage-report` dans GitHub Actions.
- **Cache des dependances** : cache pip base sur le hash de `requirements.txt`.
- **Qualite de code** : linting `ruff` et formatage `black` dans le pipeline.
- **Securite CI/CD** : scans GitLeaks, pip-audit, Bandit, Semgrep et suivi SonarCloud.
- **Badge CI** : indicateur d'etat du pipeline en tete du README.
- **Protection de branche (processus GitHub)** : merge via PR avec checks CI requis.

## Liens utiles (cours)

- Documentation GitHub Actions : [https://docs.github.com/actions](https://docs.github.com/actions)
- Marketplace GitHub Actions : [https://github.com/marketplace?type=actions](https://github.com/marketplace?type=actions)
- Documentation pytest : [https://docs.pytest.org](https://docs.pytest.org)
