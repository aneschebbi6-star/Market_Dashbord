# 🚀 Market Dashboard Pro

Une application de trading en temps réel haute performance développée avec **Python** et **Streamlit**. Ce tableau de bord permet de suivre dynamiquement les actifs cryptographiques avec une interface utilisateur soignée, un système d'authentification sécurisé et des indicateurs d'analyse technique avancés.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)

---

## 📸 Aperçu du Projet

> [!TIP]
> Ajoutez vos captures d'écran dans le dossier `assets/screenshots/` pour illustrer votre projet ici.

### 🔐 Interface de Connexion
*Une interface élégante avec effet glassmorphism pour sécuriser l'accès.*

![Login Screen](assets/screenshots/login.png)

### 📊 Tableau de Bord Principal
*Visualisation en temps réel des prix et indicateurs techniques.*

![Dashboard](assets/screenshots/dashboard.png)

---

## ✨ Fonctionnalités Clés

- **🔐 Authentification Sécurisée** : Système de login intégré pour protéger l'accès aux données sensibles.
- **📈 Graphiques Interactifs** : Chandeliers japonais (Candlesticks) avec support des moyennes mobiles (MA50, MA200).
- **⚡ Temps Réel** : Mise à jour dynamique des prix pour BTC, ETH, SOL et bien d'autres.
- **🔍 Recherche par Ticker** : Analysez n'importe quel actif disponible sur le marché.
- **🎨 Design Premium** : Interface moderne utilisant des effets de flou (backdrop-filter) et des dégradés harmonieux.

---

## 🛠️ Installation

### 1. Cloner le projet
```bash
git clone https://github.com/aneschebbi6-star/Market_Dashbord.git
cd Market_Dashbord
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

---

## 🚀 Utilisation

Pour lancer l'application, exécutez la commande suivante :

```bash
streamlit run app.py
```

**Identifiants par défaut :**
- **Utilisateur** : `Anes0123`
- **Mot de passe** : `chebbi@1`

---

## 🧰 Technologies Utilisées

- **Streamlit** : Framework principal pour l'interface utilisateur.
- **Plotly** : Bibliothèque pour les graphiques interactifs de haute qualité.
- **Pandas** : Manipulation et analyse de données financières.
- **YFinance / CoinGecko API** : Extraction des données de marché en temps réel.

---

## 📂 Structure du Projet

```text
Market_Dashbord/
├── app.py              # Point d'entrée principal (Streamlit UI)
├── fetcher.py          # Logique d'acquisition des données
├── requirements.txt    # Liste des dépendances
├── assets/             # Ressources statiques
│   └── screenshots/    # Captures d'écran du projet
└── README.md           # Documentation
```

---

## 🤝 Contribution

Les contributions, questions et suggestions sont les bienvenues ! N'hésitez pas à ouvrir une *issue* ou à soumettre une *pull request*.

---

### 👤 Auteur
**Anes Chebbi** - [GitHub](https://github.com/aneschebbi6-star)
