# BankDispute — Backend

API REST de BankDispute Intelligence, dédiée à la gestion des transactions bancaires et des alertes.

Le backend repose sur FastAPI et PostgreSQL. Il adopte une architecture en couches afin de séparer les responsabilités métier, la logique applicative, la persistance et l'exposition HTTP.

## Technologies

| Technologie | Utilisation |
|---|---|
| Python 3.15+ | Langage |
| FastAPI | API REST |
| Pydantic | Validation et schémas de données |
| SQLAlchemy 2 | ORM et persistance asynchrone |
| PostgreSQL 17 | Base de données relationnelle |
| Alembic | Gestion des migrations |
| Psycopg 3 | Connecteur PostgreSQL |
| Uvicorn | Serveur ASGI |
| Pytest | Tests automatisés |
| HTTPX | Tests des endpoints HTTP |
| Ruff | Linting et formatage |
| Mypy | Vérification statique des types |
| uv | Gestion des dépendances et de l'environnement |

## Fonctionnalités

### Transactions

- Création de transactions.
- Consultation des transactions.
- Recherche par identifiant.
- Suppression de transactions.
- Validation des données entrantes.
- Persistance dans PostgreSQL.

Les transactions utilisent notamment des attributs liés aux échanges de paiement : MTI, STAN, code réponse, canal, mode de saisie, commerçant et informations d'authentification.

### Alertes

Le backend dispose également d'un module dédié à la gestion des alertes, destiné à évoluer avec les fonctionnalités d'investigation.

### Documentation API

FastAPI génère automatiquement une documentation interactive :

- Swagger UI : `/docs`
- ReDoc : `/redoc`

## Architecture du projet

```text
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── health.py
│   │       ├── transactions.py
│   │       └── alerts.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── domain/
│   │   ├── entities/
│   │   └── value_objects/
│   │
│   ├── infrastructure/
│   │   └── ...
│   │
│   ├── main.py
│   └── ...
│
├── migrations/
├── tests/
├── .env
├── .env.test
├── pyproject.toml
├── uv.lock
├── run_tests.sh
└── launch_backend.sh
```

### Séparation des responsabilités

- `api/` : endpoints HTTP et exposition des ressources.
- `core/` : configuration et composants transverses.
- `domain/` : entités métier, règles métier et objets-valeurs.
- `infrastructure/` : implémentations techniques et accès aux données.
- `migrations/` : historique des évolutions du schéma PostgreSQL.
- `tests/` : tests automatisés.

Cette organisation permet de faire évoluer les règles métier sans les coupler directement aux mécanismes HTTP ou à la base de données.

## Installation

### Prérequis

- Python 3.15+
- [uv](https://docs.astral.sh/uv/)
- [Docker](https://www.docker.com/)
- Docker Compose

### 1. Démarrer PostgreSQL

Depuis la racine du projet :

```bash
docker compose up -d
```

Le service PostgreSQL utilise :

| Paramètre | Valeur |
|---|---|
| Image | PostgreSQL 17 |
| Conteneur | `bankdispute-postgres` |
| Port | `5432` |
| Base | `bankdispute` |
| Utilisateur | `bankdispute` |

Les données sont persistées dans un volume Docker nommé `postgres_data`.

### 2. Configurer les variables d'environnement

Créer `backend/.env` :

```env
APP_NAME=BankDispute API
APP_VERSION=1.0.0
API_V1_PREFIX=/api/v1
ENVIRONMENT=development

DATABASE_URL=postgresql+psycopg://bankdispute:bankdispute_dev@localhost:5432/bankdispute

CORS_ORIGINS=http://localhost:5173
```

Les paramètres de connexion et les origines autorisées sont configurables par variables d'environnement.

Ne jamais versionner les fichiers `.env` contenant des secrets.

### 3. Installer les dépendances

Depuis le dossier `backend` :

```bash
uv sync
```

### 4. Appliquer les migrations

```bash
uv run alembic upgrade head
```

Cette commande applique les migrations en attente et synchronise le schéma de la base de données.

### 5. Démarrer l'API

```bash
uv run uvicorn app.main:app --reload
```

L'API est accessible à l'adresse :

http://localhost:8000

Documentation interactive :

http://localhost:8000/docs

## Migrations de base de données

Alembic permet de versionner et de faire évoluer le schéma PostgreSQL.

Appliquer les migrations :

```bash
uv run alembic upgrade head
```

Créer une nouvelle migration :

```bash
uv run alembic revision --autogenerate -m "description"
```

Consulter la version actuelle :

```bash
uv run alembic current
```

## Tests automatisés

Les tests reposent sur Pytest et HTTPX.

Une base PostgreSQL distincte, `bankdispute_test`, est utilisée pour isoler les tests des données de développement.

### 1. Créer la base de test

```sql
CREATE DATABASE bankdispute_test;
```

### 2. Configurer `.env.test`

```env
TEST_DATABASE_URL=postgresql+psycopg://bankdispute:bankdispute_dev@localhost:5432/bankdispute_test
```

### 3. Lancer tous les tests

Depuis `backend/` :

```bash
./run_tests.sh
```

### 4. Lancer les tests d'un module

```bash
./run_tests.sh transaction
```

Cette commande exécute les tests de `tests/test_transaction.py`.

Les tests utilisent une base dédiée afin de préserver les données de développement et de garantir l'isolation des scénarios.

## Qualité du code

Le projet utilise Ruff et Mypy.

### Ruff — Linting

```bash
uv run ruff check .
```

### Ruff — Formatage

```bash
uv run ruff format .
```

### Mypy — Vérification des types

```bash
uv run mypy .
```

Ces outils permettent de détecter les problèmes de style, les erreurs potentielles et les incohérences de typage.

## Configuration Docker

Le fichier Compose situé à la racine du projet définit le service PostgreSQL.

Démarrer les services :

```bash
docker compose up -d
```

Afficher leur état :

```bash
docker compose ps
```

Consulter les logs PostgreSQL :

```bash
docker compose logs postgres
```

Arrêter les services :

```bash
docker compose down
```

## Statut du backend

Le backend est en développement actif.

Les prochaines évolutions concernent notamment l'enrichissement des alertes, les fonctionnalités d'investigation, l'analyse des anomalies transactionnelles et l'intégration progressive de capacités ML et IA.

---

**BankDispute Intelligence — Backend**