# Facturation & Client Management App

## Installation

1. Clone the repository.
2. Create a Python virtual environment and activate it.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure PostgreSQL connection in `.env`.
5. Run database migrations:
   ```bash
   flask db upgrade
   ```
6. Launch the app:
   ```bash
   flask run
   ```

## Configuration PostgreSQL

Set your database URI in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/yourdb
```

## Project Structure

- `app/` - Main application package
  - `models/` - SQLAlchemy models
  - `routes/` - Flask routes
  - `services/` - Business logic
  - `templates/` - Jinja2 HTML templates
  - `static/` - CSS, JS, images
  - `config.py` - App configuration
- `migrations/` - Alembic migrations
- `.env` - Environment variables
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

## Ready for local production use

---

## Fonctionnalités principales

- Authentification sécurisée (login/logout, rôles admin/user, accès restreint, mot de passe hashé)
- Dashboard : chiffre d'affaires (jour/semaine/mois/année), nombre de factures, dernières factures, prochain RDV Google Agenda (client, type, date, heure), rafraîchissement auto JS
- Facturation : création, sélection client/type RDV, prix auto, date, numéro auto, PDF, envoi mail, liste, tri, filtre, recherche, statuts (brouillon/envoyée/payée)
- Clients : CRUD, statut RDV (honoré/reporté/pas venu), historique RDV, accès factures
- Mailing : envoi individuel/groupé (CCI), filtres (statut RDV/type RDV), historique envois
- Utilisateurs (admin) : CRUD, rôles, actif/inactif
- Paramètres : infos entreprise (SIRET, nom/prénom, adresse, téléphone, email, logo), paramètres e-mail (SMTP/IMAP, test), types de RDV CRUD (nom, prix, durée, lien Google Agenda)
- Base de données PostgreSQL : toutes tables, relations, clés étrangères, index
- Migrations Flask-Migrate

---

Pour plus de détails, voir SETUP.md
