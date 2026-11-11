# BankDispute Intelligence

**Plateforme intelligente d'investigation des transactions bancaires et de détection des anomalies.**

BankDispute Intelligence est un projet personnel à la croisée du développement logiciel, de la monétique et de l'intelligence artificielle.

L'objectif est de faciliter l'investigation des transactions bancaires, l'analyse des refus de paiement et l'identification de comportements suspects, grâce à une plateforme qui intégrera progressivement des capacités d'analyse intelligente et d'assistance par IA.

## Technologies

### Backend — En développement

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/Alembic-Migrations-555555?style=for-the-badge" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" />
</p>

- API REST avec FastAPI.
- Architecture en couches et séparation des responsabilités.
- Persistance asynchrone avec SQLAlchemy et PostgreSQL.
- Gestion des migrations avec Alembic.
- Validation des données avec Pydantic.
- Tests API avec Pytest et HTTPX.

### Frontend — Prochaine étape

<p align="left">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" />
</p>

Interface d'investigation et de visualisation des transactions.

### Intelligence artificielle & Machine Learning — À venir

<p align="left">
  <img src="https://img.shields.io/badge/AI%20%26%20ML-En%20cours-8A2BE2?style=for-the-badge" />
</p>

- Détection d'anomalies transactionnelles.
- Analyse intelligente des refus de paiement.
- RAG sur la documentation monétique.
- Agents IA pour assister les investigations.

## Fonctionnalités actuelles

- Création et consultation des transactions.
- Recherche d'une transaction par identifiant.
- Suppression des transactions.
- Validation des données entrantes.
- Documentation interactive de l'API avec Swagger.
- Tests automatisés sur une base dédiée.

## Démarrage du projet

### Prérequis

- Python
- [uv](https://docs.astral.sh/uv/)
- [Docker](https://www.docker.com/)

### 1. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd BankDispute
```

### 2. Démarrer PostgreSQL

```bash
docker compose up -d
```

### 3. Configurer l'environnement

Créer `backend/.env` :

```env
DATABASE_URL=postgresql+psycopg://bankdispute:bankdispute_dev@localhost:5432/bankdispute
ENVIRONMENT=development
```

### 4. Installer les dépendances

```bash
cd backend
uv sync
```

### 5. Appliquer les migrations

```bash
uv run alembic upgrade head
```

### 6. Lancer l'API

```bash
uv run uvicorn app.main:app --reload
```

Documentation interactive : http://127.0.0.1:8000/docs

## Tests

Les tests automatisés utilisent **Pytest et HTTPX**.

Une base PostgreSQL distincte (`bankdispute_test`) est utilisée pour isoler les tests de l'environnement de développement.

Ce choix permet de tester le comportement réel de SQLAlchemy et de PostgreSQL : requêtes, transactions, contraintes et persistance, sans modifier les données de développement.

Créer la base de test :

```sql
CREATE DATABASE bankdispute_test;
```

Créer `backend/.env.test` :

```env
TEST_DATABASE_URL=postgresql+psycopg://bankdispute:bankdispute_dev@localhost:5432/bankdispute_test
```

Lancer tous les tests :

```bash
./run_tests.sh
```

Lancer uniquement les tests des transactions :

```bash
./run_tests.sh transaction
```

Chaque test dispose d'une base réinitialisée afin de garantir son indépendance et sa reproductibilité.

## Statut du projet

| Module | Statut |
|---|---|
| Backend & API REST | En développement |
| Base de données | Opérationnelle |
| Tests automatisés | En développement |
| Frontend | Prochaine étape |
| Machine Learning | À venir |
| RAG & Agents IA | À venir |

## Domaine métier

Le projet s'appuie sur des données synthétiques et un profil ISO 8583 simulé pour explorer les problématiques de paiement, d'investigation et de détection de fraude.

Aucune donnée bancaire réelle n'est utilisée.

---

**BankDispute Intelligence — Projet personnel de développement logiciel, monétique et intelligence artificielle.**