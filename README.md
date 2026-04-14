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

## Qualite et tests

```bash
flake8 src/ tests/ --max-line-length=120
pytest --cov=src --cov-report=term --cov-report=html:coverage-report -v
```

Le rapport de couverture HTML est genere dans `coverage-report/`.

## Pipeline CI (GitHub Actions)

Workflow : `.github/workflows/ci.yml`

Le pipeline execute automatiquement sur `push` et `pull_request` vers `main` :
- linting (`flake8`)
- tests (`pytest`)
- couverture (`pytest-cov`)
- upload de l'artefact `coverage-report`
- publication des resultats de tests sur PR via l'action Marketplace `EnricoMi/publish-unit-test-result-action@v2`
