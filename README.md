![CI](https://github.com/paulo54360/mon-projet-flask/actions/workflows/ci.yml/badge.svg)

# Mon projet Flask

Application Flask simple pour le TP2 d'integration continue.

## Lancer le projet

```bash
pip install -r requirements.txt
python src/app.py
```

Routes disponibles :
- `/`
- `/health`
- `/hello/<name>`
- `/add/<int:a>/<int:b>`

## Lancer les tests

```bash
pytest -v
```
