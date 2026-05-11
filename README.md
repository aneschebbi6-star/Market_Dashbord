<p align="center">
  <img src="assets/banner.png" alt="Market Dashboard Pro Banner" width="100%">
</p>

# 🚀 Market Dashboard Pro

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/aneschebbi6-star/Market_Dashbord)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Market Dashboard Pro** est une plateforme de trading et d'analyse de crypto-monnaies haute performance. Conçue avec **Python** et **Streamlit**, elle offre une expérience utilisateur fluide et premium pour le suivi des actifs numériques en temps réel.

---

## ✨ Points Forts

- **🔐 Authentification de Grade Terminal** : Interface de connexion sécurisée avec un design _glassmorphism_ et arrière-plans animés.
- **📊 Analyse Technique Avancée** : Graphiques en chandeliers (Candlesticks) interactifs propulsés par Plotly, incluant des indicateurs comme MA50 et MA200.
- **⚡ Flux de Données Ultra-Rapide** : Intégration en temps réel pour BTC, ETH, SOL, et plus via yfinance et CoinGecko.
- **🔍 Recherche Dynamique** : Analysez instantanément n'importe quel ticker disponible sur le marché mondial.
- **🎨 UI/UX Premium** : Design moderne, sombre, avec des effets de flou cinétique et des micro-animations.

---

## 📸 Aperçu de l'Interface

<div align="center">
  <table>
    <tr>
      <td width="50%">
        <p align="center"><b>🔐 Connexion Sécurisée</b></p>
        <img src="assets/screenshots/login.png" alt="Login Interface" width="100%">
      </td>
      <td width="50%">
        <p align="center"><b>📊 Dashboard Principal</b></p>
        <img src="assets/screenshots/dashboard.png" alt="Main Dashboard" width="100%">
      </td>
    </tr>
  </table>
</div>

> [!TIP]
> Pour une expérience optimale, utilisez le navigateur Chrome en mode plein écran.

---

## 🛠️ Installation & Configuration

### Prérequis

- Python 3.11 ou supérieur
- Un gestionnaire de paquets (pip)

### Guide Étape par Étape

1.  **Cloner le dépôt**

    ```bash
    git clone https://github.com/aneschebbi6-star/Market_Dashbord.git
    cd Market_Dashbord
    ```

2.  **Configurer l'Environnement Virtuel**

    ```bash
    # Création de l'environnement
    python -m venv venv

    # Activation (Windows)
    venv\Scripts\activate

    # Activation (Linux/macOS)
    source venv/bin/activate
    ```

3.  **Installer les Dépendances**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Lancement Rapide

Pour démarrer le terminal de trading, exécutez :

```bash
streamlit run app.py
```

> **Astuce :** Si la commande `streamlit` n'est pas reconnue sous Windows, utilisez `python -m streamlit run app.py`.

### 🐳 Lancement via Dev Containers (Recommandé)
Ce projet est pré-configuré pour tourner dans un conteneur Docker isolé.
1. Installez l'extension **Dev Containers** dans VS Code.
2. Ouvrez la palette de commandes (`F1`) et choisissez **"Dev Containers: Reopen in Container"**.
3. L'environnement Python s'installe tout seul et l'app s'ouvre sur le port `8501`.

### 🔐 Authentification sécurisée

Ce projet utilise des identifiants configurables via :

- variables d'environnement : `DASHBOARD_USER` et `DASHBOARD_PASSWORD`
- ou fichier local `.env`
- ou Streamlit secrets : `.streamlit/secrets.toml`

> Ne pas laisser d'identifiants en clair dans le code source.

Exemple de configuration en `.env` :

```env
DASHBOARD_USER=trade_admin
DASHBOARD_PASSWORD=ProDash@2026
```

---

### 📰 Flux d'Actualités en Temps Réel (Optionnel)

Pour activer les actualités crypto en **temps réel** via NewsAPI :

1. Créez un compte gratuit sur [newsapi.org](https://newsapi.org/) (100 requêtes/jour)
2. Récupérez votre clé API
3. Ajoutez-la dans `.env` :

```env
NEWSAPI_KEY=votre_clé_api_ici
```

> **Sans clé API** : le système affichera des actualités de démonstration réalistes.

---

## 🧰 Stack Technique

- **Frontend & Logic** : [Streamlit](https://streamlit.io/) (Interface réactive)
- **Visualisation** : [Plotly](https://plotly.com/python/) (Graphiques financiers interactifs)
- **Data Processing** : [Pandas](https://pandas.pydata.org/) (Manipulation de séries temporelles)
- **Market Data** : [yfinance](https://github.com/ranaroussi/yfinance) / [CoinGecko API](https://www.coingecko.com/en/api)

---

## 📂 Architecture MVC (Modèle-Vue-Contrôleur)

Le projet a été refactorisé pour garantir un code modulaire et professionnel :

```text
Market_Dashbord/
├── app.py              # Point d'entrée principal (Orchestrateur)
├── fetcher.py          # ⚙️ Modèle : API et traitement des données
├── controllers/        # 🎮 Contrôleurs : Logique métier
│   └── auth.py         # Authentification sécurisée
├── views/              # 👁️ Vues : Rendu de l'interface utilisateur
│   ├── login.py        # Interface de connexion
│   ├── dashboard.py    # Composants du tableau de bord
│   └── sidebar.py      # Menu latéral de pilotage
├── styles/             # 🎨 Styles Globaux
│   └── theme.py        # Injection du CSS (Dark mode, Glassmorphism)
├── requirements.txt    # Dépendances du projet
├── assets/             # Ressources (Images, Logos)
└── README.md           # Documentation complète
```

---

## 🛣️ Roadmap (À venir)

- [ ] 🔔 Alertes de prix personnalisables par email.
- [ ] 🤖 Intégration de signaux de trading basés sur le sentiment (IA).
- [ ] 💼 Gestion de portefeuille (Portfolio Tracking).
- [ ] 🌓 Mode Clair/Sombre automatique.

---

## 🤝 Contribution

Les contributions font la force de la communauté open-source.

1. Forkez le projet.
2. Créez votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`).
3. Commit avec un message clair (`git commit -m 'Add some AmazingFeature'`).
4. Push sur la branche (`git push origin feature/AmazingFeature`).
5. Ouvrez une Pull Request.

---

## 👤 Auteur

**Anes Chebbi** - _Développeur Fullstack & Passionné de Finance_

- GitHub : [@aneschebbi6-star](https://github.com/aneschebbi6-star)
- LinkedIn : [Votre Profil](https://linkedin.com/in/votre-profil) (Optionnel)

---

<p align="center">Développé avec ❤️ pour la communauté trading.</p>
