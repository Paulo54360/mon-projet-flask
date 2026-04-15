# Compte-rendu TP4 - Securite

## Contexte

Ce TP ajoute une couche securite au pipeline CI existant (TP3) avec : scan CVE des dependances, gestion des secrets, detection de secrets dans l'historique Git, et automatisation des mises a jour.

## Reponses aux questions

### Question 1 - CVE et score CVSS

Une CVE (Common Vulnerabilities and Exposures) est un identifiant unique public qui reference une faille de securite connue.

Le score CVSS (Common Vulnerability Scoring System) mesure la severite d'une faille de 0.0 a 10.0 selon son impact et sa facilitie d'exploitation (faible, moyen, eleve, critique).

Exemple observe pendant le TP :

- package : `flask==2.0.0`
- vulnerabilite : `PYSEC-2023-62` (equivalent advisory connu sur Flask)
- impact : risque de fuite/exposition de donnees de session dans certains contextes
- version corrigee : `2.2.5` minimum (ou `2.3.2` selon advisory)

### Question 2 - Pourquoi scanner les dependances

Scanner uniquement notre code ne suffit pas, car une application depend surtout de bibliotheques externes.

Une faille dans une dependance peut compromettre l'application meme si notre code est propre. C'est exactement le role de `pip-audit` : verifier les CVE connues sur les paquets installes et bloquer la CI si une version vulnerable est detectee.

Dans le projet :

- `pip-audit -r requirements.txt` retourne "No known vulnerabilities found"
- la simulation `flask==2.0.0` detecte immediatement 2 vulnerabilites.

### Question 3 - Dependabot vs scan manuel

`pip-audit` est un scan ponctuel : il donne une photo de l'etat des dependances au moment ou on l'execute.

Dependabot apporte l'automatisation continue :

- detection reguliere des nouvelles versions/correctifs
- creation automatique de PR de mise a jour
- reduction du temps entre publication d'un correctif et son integration

On configure aussi `github-actions` pour mettre a jour les actions CI elles-memes, car elles peuvent aussi contenir des vulnerabilites de securite.

### Question 4 - Secrets dans le code

On ne doit jamais mettre un secret en dur dans le code source, car il devient visible dans :

- l'historique Git
- les forks/clones
- les logs/outils d'analyse

Un secret commite peut rester exploitable meme apres suppression apparente dans un commit suivant.

Stockages securises recommandes :

1. GitHub Secrets (CI/CD)
2. Secret Manager cloud (ex: GCP Secret Manager, AWS Secrets Manager, Azure Key Vault)
3. Variables d'environnement (avec gestion via infra ou `.env` non versionne)

Dans ce projet :

- CI : secret `API_KEY` teste pendant la demonstration, puis step retire comme demande dans l'enonce TP
- Flask : `SECRET_KEY` chargee via variable d'environnement (`os.environ.get(...)`).

### Question 5 - Secret commite puis supprime

Non, le secret n'est pas en securite.

S'il a ete commite une fois, il reste present dans l'historique Git et peut etre retrouve (clone, fork, cache CI, outils d'analyse d'historique).

Actions correctives a faire :

1. revoquer/rotater immediatement la cle exposee (obligatoire)
2. nettoyer l'historique Git si necessaire (BFG/git filter-repo) selon la politique projet
3. ajouter des controles automatiques (GitLeaks en CI + hooks)

Dans le TP, une fuite simulee (`config_test.py`) est bien detectee par GitLeaks en local.

### Question 6 - Pourquoi GitLeaks au debut

GitLeaks est place au tout debut pour appliquer le principe "fail fast" sur le risque le plus critique : l'exposition de secrets.

Si un secret est detecte, on arrete le pipeline immediatement sans depenser du temps sur lint/tests/scans suivants. Cela reduit le temps de feedback et limite l'exposition.

### Question 7 - OWASP Top 10 et couverture pipeline

Trois risques OWASP Top 10 et prise en charge par le pipeline :

1. **A06 - Vulnerable and Outdated Components**
  - Adresse par `pip-audit` (CVE dependances) + Dependabot (mises a jour automatiques)
2. **A02 - Cryptographic Failures** (exposition de secrets/cles)
  - Partiellement adresse par GitLeaks (detection de secrets commites)
3. **A03 - Injection**
  - Partiellement adresse par Bandit/Semgrep (patterns dangereux)

Limite : le pipeline ne couvre pas tout OWASP (ex: logique d'authentification/metiers), d'ou l'importance des revues de code et tests de securite complementaires.

### Question 8 - Ordre complet du pipeline final

Ordre du pipeline final dans `ci.yml` :

1. `actions/checkout@v4` avec `fetch-depth: 0`
  - recupere tout l'historique pour scanner les commits
2. `GitLeaks`
  - detecte secrets exposes dans code/historique
3. `setup-python` + `cache pip` + `pip install -r requirements.txt`
  - prepare l'environnement de build
4. `black --check`
  - detecte ecarts de formatage
5. `ruff check`
  - detecte erreurs statiques/qualite
6. `pip-audit -r requirements.txt`
  - detecte CVE dans dependances
7. `bandit -r src/ -ll`
  - detecte anti-patterns securite Python
8. `semgrep --config auto --config .semgrep/custom-rules.yml --error src/`
  - detecte patterns dangereux + regle custom projet
9. `pytest --cov ... --cov-fail-under=70`
  - valide comportement et quality gate couverture
10. generation `coverage.xml` + scan SonarCloud
  - centralise indicateurs qualite/securite
11. upload artefact `coverage-report`
  - conserve rapport de couverture

### Question 9 - Shift Left vs audit traditionnel

Audit traditionnel : verification securite tardive (souvent en fin de cycle), avec corrections couteuses.

Shift Left : controles securite integres tot (commit/CI), feedback rapide et continu.

Avantages observes ici :

- detection immediate des secrets/CVE avant merge
- reduction du cout de correction
- meilleure hygiene de securite dans le flux quotidien des devs
- standardisation des controles sur toutes les PR

### Question 10 - Optimisations performance pipeline

Si le pipeline devient trop long, optimisations possibles :

1. **Parallelliser des jobs** (qualite vs tests vs scans non dependants)
2. **Conserver le fail fast** (GitLeaks/pip-audit/lint avant etapes lourdes)
3. **Optimiser le cache** (`pip`, caches outils) et epingler versions
4. **Limiter les scans couteux** selon contexte (ex: uniquement sur PR, nightly complet sur main)
5. **Eviter les doublons** (regrouper commandes pytest quand possible)
6. **Utiliser matrix selective** seulement quand necessaire (versions Python multiples)

### Question 11 - CVE Flask/extension (recherche autonome)

Advisory etudie :

- identifiant : `GHSA-68rp-wp8r-4726` (associe CVE-2026-27205)
- package affecte : `Flask`
- score CVSS : `2.3 (Low)`
- impact : absence du header `Vary: Cookie` dans certains cas d'acces session, pouvant faciliter des problemes de cache de contenu utilisateur
- version corrigee : `Flask 3.1.3`
- lien : [https://github.com/pallets/flask/security/advisories/GHSA-68rp-wp8r-4726](https://github.com/pallets/flask/security/advisories/GHSA-68rp-wp8r-4726)

Comment ce TP aide a prevenir :

- `pip-audit` aurait signale la version vulnerable en CI
- Dependabot aurait propose une PR de mise a jour vers une version corrigee

Bonne pratique Flask ajoutee dans l'application :

- ajout de headers de securite (`Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`)
- verification par test automatique (`test_security_headers_are_present`)

## Checklist de rendu TP4

- [x] pip-audit integre dans le pipeline CI
- [x] Dependabot configure (`.github/dependabot.yml`)
- [x] Un secret GitHub cree et utilise pendant la demonstration CI
- [x] GitLeaks integre dans la CI (tout debut du pipeline)
- [x] `.gitignore` mis a jour pour les fichiers generes
- [x] Pipeline complet vert (securite + qualite + tests)
- [ ] PR mergee avec tous les checks passes
- [x] Compte-rendu avec les reponses aux 11 questions
