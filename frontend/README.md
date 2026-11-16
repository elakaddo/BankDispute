# BankDispute — Frontend

Interface web de BankDispute Intelligence, une plateforme d'investigation des transactions bancaires et d'assistance à l'analyse des alertes.

Le frontend permet aux analystes de consulter les transactions, d'effectuer des recherches et de naviguer entre les différents modules de la plateforme.

## Technologies

| Technologie | Utilisation |
|---|---|
| React 19 | Bibliothèque UI |
| TypeScript | Typage statique |
| Vite | Serveur de développement et build |
| React Router | Navigation et routage |
| TanStack Query | Gestion des données serveur et du cache |
| TanStack Table | Gestion des tableaux |
| Lucide React | Icônes |
| CSS | Styles et responsive design |

## Fonctionnalités

### Transactions

- Consultation des transactions enregistrées.
- Recherche par identifiant.
- Filtrage par canal et code réponse.
- Tri croissant et décroissant par date et montant.
- Pagination de 10 transactions par page.
- Consultation des détails d'une transaction dans une fenêtre modale.
- Actualisation des données depuis l'API.

### Navigation

L'application est organisée autour de plusieurs modules :

| Module | Description |
|---|---|
| Supervision | Vue générale de la plateforme |
| Transactions | Consultation et recherche des transactions |
| Alertes | Consultation des alertes |
| Investigations | Espace d'investigation |
| Assistant IA | Futur espace d'assistance intelligente |

Les modules sont progressivement développés.

## Architecture du projet

```text
frontend/
├── public/
├── src/
│   ├── api/
│   │   ├── client.ts
│   │   ├── transactions.ts
│   │   └── alerts.ts
│   │
│   ├── components/
│   │   └── layout/
│   │       └── AppShell.tsx
│   │
│   ├── features/
│   │   ├── transactions/
│   │   │   ├── TransactionsPage.tsx
│   │   │   └── TransactionsStyle.css
│   │   ├── alerts/
│   │   └── investigation/
│   │
│   ├── styles/
│   │   ├── variables.css
│   │   ├── global.css
│   │   └── legacy-theme.css
│   │
│   ├── App.tsx
│   └── main.tsx
│
├── .env
├── package.json
└── vite.config.ts
```

### Organisation

- `api/` : communication avec le backend et fonctions d'accès aux données.
- `components/` : composants partagés entre plusieurs fonctionnalités.
- `features/` : organisation du code par fonctionnalité métier.
- `styles/` : variables CSS et styles globaux.
- `App.tsx` : configuration des routes.
- `main.tsx` : point d'entrée React.

Les styles spécifiques à une fonctionnalité sont conservés dans son propre dossier.

## Installation

### Prérequis

- Node.js
- npm

### 1. Installer les dépendances

Depuis le dossier `frontend` :

```bash
npm install
```

### 2. Configurer l'environnement

Créer un fichier `.env` :

```env
VITE_API_URL=http://localhost:8000/api/v1
```

Cette variable définit l'URL de base utilisée pour communiquer avec l'API.

### 3. Démarrer le serveur de développement

```bash
npm run dev
```

L'application est accessible à l'adresse :

http://localhost:5173

## Scripts disponibles

| Commande | Description |
|---|---|
| `npm run dev` | Démarre le serveur Vite |
| `npm run build` | Vérifie les types TypeScript et génère le build |
| `npm run lint` | Analyse le code avec ESLint |
| `npm run preview` | Prévisualise le build de production |

## Communication avec le backend

Les appels HTTP sont centralisés dans `src/api/`.

Les fonctions métier sont séparées par ressource :

- `transactions.ts` : opérations liées aux transactions.
- `alerts.ts` : opérations liées aux alertes.
- `client.ts` : configuration et exécution des requêtes HTTP.

TanStack Query assure notamment :

- La récupération des données.
- La gestion des états de chargement et d'erreur.
- La mise en cache.
- La réactualisation des données.

## Build de production

```bash
npm run build
```

Les fichiers générés sont placés dans le dossier `dist/`.

## Statut

Le frontend est en cours de développement. Les fonctionnalités sont ajoutées progressivement en fonction de l'évolution du backend et des besoins métier.

---

**BankDispute Intelligence — Frontend**