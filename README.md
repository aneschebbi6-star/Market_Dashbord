<p align="center">
  <img src="assets/banner.png" alt="Market Dashboard Pro Banner" width="100%">
</p>

# 🚀 Market Dashboard Pro

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/aneschebbi6-star/Market_Dashbord)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Market Dashboard Pro** est une plateforme **haute performance** de trading et d'analyse de crypto-monnaies. Conçue avec **Python**, **Streamlit** et des APIs financières modernes, elle offre une expérience utilisateur fluide et premium pour le suivi des actifs numériques en temps réel.

✨ **Parfait pour** : traders, analystes crypto, investisseurs passionnés et passionnés de finance décentralisée.

---

## 📑 Table des Matières

- [Caractéristiques Principales](#-caractéristiques-principales)
- [Galerie de l'Interface](#-galerie-de-linterface)
- [Installation & Configuration](#-installation--configuration)
- [Lancement Rapide](#-lancement-rapide)
- [Stack Technique](#-stack-technique)
- [Architecture MVC](#-architecture-mvc-modèle-vue-contrôleur)
- [Configuration Avancée](#️-configuration-avancée)
- [Troubleshooting](#-troubleshooting--faq)
- [Fonctionnalités Détaillées](#-fonctionnalités-détaillées)
- [Roadmap](#-roadmap-à-venir)
- [Contribution](#-contribution)
- [Licence](#-licence)
- [Auteur](#-auteur)

---

## ✨ Caractéristiques Principales

- **📊 Analyse Technique Avancée** : Graphiques en chandeliers (Candlesticks) interactifs propulsés par Plotly, incluant des indicateurs techniques comme MA50, MA200 et bien d'autres.
- **⚡ Flux de Données Ultra-Rapide** : Intégration en temps réel pour BTC, ETH, SOL, et plus de 5000 actifs via yfinance et CoinGecko API.
- **🔍 Recherche Dynamique** : Analysez instantanément n'importe quel ticker disponible sur le marché mondial.
- **🎨 UI/UX Premium** : Design moderne et élégant avec thème sombre, glassmorphism, effets cinétiques et micro-animations fluides.
- **📰 Actualités en Temps Réel** : Suivi des nouvelles crypto et finances avec intégration NewsAPI (optionnelle).
- **📈 Comparaison Multi-Actifs** : Comparez les performances de plusieurs actifs côte à côte.

---

## 📸 Galerie de l'Interface

### 📊 Tableau de Bord Principal
<div align="center">
  <img src="assets/screenshots/dashboard.png" alt="Main Dashboard" width="65%">
</div>

### 📈 Analyse Graphique Avancée
<div align="center">
  <img src="assets/screenshots/chart.png" alt="Advanced Charts" width="65%">
</div>

### 🔄 Comparaison Multi-Actifs
<div align="center">
  <img src="assets/screenshots/compari.png" alt="Asset Comparison" width="65%">
</div>

### 😊 Analyse du Sentiment
<div align="center">
  <img src="assets/screenshots/analyse_sentiment.png" alt="Sentiment Analysis" width="65%">
</div>

### 🏪 Vue Détaillée du Marché
<div align="center">
  <img src="assets/screenshots/det_marche.png" alt="Market Details" width="65%">
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

### Méthode 1️⃣ : Installation Locale Standard

Pour démarrer le dashboard, exécutez :

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement sur `http://localhost:8501` 🌐

> **Astuce** : Si la commande `streamlit` n'est pas reconnue sous Windows, utilisez :
> ```bash
> python -m streamlit run app.py
> ```

### Méthode 2️⃣ : Dev Containers (Recommandé pour VS Code)

Ce projet est **pré-configuré** pour tourner dans un conteneur Docker isolé, garantissant un environnement cohérent.

**Prérequis** :
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installé
- Extension [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) dans VS Code

**Étapes** :
1. Ouvrez le projet dans VS Code
2. Appuyez sur `Ctrl + Shift + P` (ou `Cmd + Shift + P` sur Mac)
3. Tapez et sélectionnez : **"Dev Containers: Reopen in Container"**
4. Attendez la construction du conteneur (2-3 min)
5. L'environnement Python s'installe automatiquement
6. L'app s'ouvre sur le port `8501` 🚀

**Avantages du Dev Container** :
- ✅ Pas de dépendances locales
- ✅ Environnement 100% reproductible
- ✅ Idéal pour la collaboration d'équipe
- ✅ Isolation complète du système

---

### 📰 Actualités en Temps Réel (Optionnel)

Pour activer l'intégration des actualités crypto via **NewsAPI** :

1. **Créez un compte gratuit** sur [newsapi.org](https://newsapi.org/) (limite : 100 requêtes/jour en gratuit)
2. **Récupérez votre clé API** depuis le tableau de bord
3. **Créez un fichier `.env`** à la racine du projet :
    ```env
    NEWSAPI_KEY=votre_clé_api_ici
    ```
4. Relancez l'application - les actualités s'afficheront automatiquement

> **💡 Note** : Sans clé API, le système affichera des actualités de démonstration réalistes pour vous permettre de tester l'interface.

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
├── views/              # 👁️ Vues : Rendu de l'interface utilisateur
│   ├── dashboard.py    # Composants du tableau de bord
│   └── sidebar.py      # Menu latéral de pilotage
├── styles/             # 🎨 Styles Globaux
│   └── theme.py        # Injection du CSS (Dark mode, Glassmorphism)
├── requirements.txt    # Dépendances du projet
├── assets/             # Ressources (Images, Logos)
└── README.md           # Documentation complète
```

---

## ⚙️ Configuration Avancée

### Variables d'Environnement

Créez un fichier `.env` à la racine du projet pour personnaliser votre installation :

```env
# NewsAPI (optionnel - pour les actualités)
NEWSAPI_KEY=votre_clé_ici

# Configuration Streamlit (optionnel)
STREAMLIT_SERVER_PORT=8501
STREAMLIT_LOGGER_LEVEL=info
```

---

## 🔧 Troubleshooting & FAQ

| Problème | Solution |
|----------|----------|
| ❌ `ModuleNotFoundError: No module named 'streamlit'` | Assurez-vous d'avoir activé le venv : `venv\Scripts\activate` puis `pip install -r requirements.txt` |
| ❌ `streamlit: command not found` (Windows) | Utilisez `python -m streamlit run app.py` au lieu de `streamlit run app.py` |
| ❌ Les données n'apparaissent pas | Vérifiez votre connexion Internet et les limites d'API (yfinance, CoinGecko) |
| ❌ Port 8501 déjà utilisé | Changez le port : `streamlit run app.py --server.port 8502` |
| ⏱️ L'application est lente | Réduisez la période d'historique ou fermez d'autres applications gourmandes en ressources |

---

## 📊 Fonctionnalités Détaillées

### 1️⃣ Tableau de Bord Interactif
- Vue d'ensemble du marché crypto en temps réel
- Indicateurs clés (Market Cap, Volume 24h, Dominance BTC)
- Changements de prix en pourcentage sur différentes périodes

### 2️⃣ Analyse Technique Avancée
- Graphiques candlestick haute résolution
- Moyennes mobiles (MA 20, 50, 200)
- Support des intégrales temporelles : 1m, 5m, 15m, 1h, 4h, 1j, 1w
- Indicateurs techniques personnalisables

### 3️⃣ Recherche Globale
- Recherche par ticker ou nom de projet
- Filtrage instantané sur 5000+ cryptomonnaies
- Informations détaillées : prix, volume, cap, tendance

### 4️⃣ Comparaison Multi-Actifs
- Comparez jusqu'à 5 actifs simultanément
- Graphiques de performance normalisés
- Export des données comparatives

---

## 🛣️ Roadmap (À venir)

- [ ] 🔔 Alertes de prix personnalisables par email et notifications push
- [ ] 🤖 Intégration d'IA : Signaux de trading basés sur analyse du sentiment
- [ ] 💼 Gestion de portefeuille complète (Portfolio Tracking & Performance)
- [ ] 🌓 Mode Clair/Sombre automatique selon les préférences utilisateur
- [ ] 📱 Application mobile (React Native)
- [ ] 💾 Sauvegarde des watchlists et préférences utilisateur
- [ ] 📊 Export de rapports (PDF, Excel)
- [ ] 🔐 Authentification utilisateur sécurisée

---

## 🤝 Contribution

Les contributions font la force de la communauté open-source. Toute aide est la bienvenue !

### 📝 Processus de Contribution

1. **Forkez le projet** via le bouton Fork sur GitHub
2. **Créez votre branche de fonctionnalité**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Committez vos modifications** avec un message clair
   ```bash
   git commit -m 'Add: Amazing feature description'
   ```
4. **Poussez sur votre branche**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Ouvrez une Pull Request** avec une description détaillée

### 📋 Directives de Contribution

- Testez votre code avant de soumettre une PR
- Respectez le style de code existant (PEP 8 pour Python)
- Mettez à jour la documentation si nécessaire
- Décrivez clairement les changements et leur motivation

---

## 📄 Licence

Ce projet est sous la licence **MIT**. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👤 Auteur

**Anes Chebbi** - _Développeur Fullstack & Passionné de Finance_

- **GitHub** : [@aneschebbi6-star](https://github.com/aneschebbi6-star)
- **LinkedIn** : [Anes Chebbi](https://www.linkedin.com/in/anes-chebbi-9995b1316/)
- **Portfolio** : [Consultez mes projets](https://github.com/aneschebbi6-star?tab=repositories)

---

## 🙏 Remerciements

Merci à :
- [Streamlit](https://streamlit.io/) pour le framework web interactif
- [Plotly](https://plotly.com/) pour les graphiques professionnels
- [yfinance](https://github.com/ranaroussi/yfinance) pour l'accès aux données financières
- [CoinGecko API](https://www.coingecko.com/en/api) pour les données crypto
- La communauté open-source pour l'inspiration

---

<p align="center">
  <strong>Développé avec ❤️ pour la communauté trading</strong><br>
  <sub>⭐ Si ce projet vous a aidé, n'hésitez pas à laisser une étoile sur GitHub !</sub>
</p>
