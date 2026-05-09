# 📊 Live Market Dashboard PRO

### Guide d'utilisation et de développement de la version avancée

---

## 🎯 Aperçu du Projet
Une application web professionnelle de trading en temps réel construite avec **Streamlit**, **YFinance** et **Plotly**. Elle permet de suivre les cours des cryptomonnaies, de réaliser des analyses techniques avec des bougies japonaises et des indicateurs (MA 50/200).

---

## 🛠 Installation & Configuration (Version 64-bit)

Pour éviter les erreurs de compilation (comme `curl_cffi` ou `pyarrow`), ce projet utilise **Python 64-bit**.

### 1. Créer l'environnement virtuel
```powershell
# Utiliser le chemin vers votre Python 64-bit
& "C:\Users\ANES\AppData\Local\Programs\Python\Python311\python.exe" -m venv venv64
```

### 2. Installer les dépendances
```powershell
.\venv64\Scripts\pip install streamlit pandas yfinance plotly
```

---

## 🚀 Lancer l'application
```powershell
.\venv64\Scripts\streamlit run app.py
```

---

## 💡 Fonctionnalités PRO

### 1. 🔍 Recherche Dynamique
Vous pouvez entrer n'importe quel ticker crypto dans la barre latérale (ex: `DOGE`, `ADA`, `BTC`). L'application convertit automatiquement le symbole pour interroger Yahoo Finance.

### 2. 📈 Graphiques de Trading
*   **Bougies Japonaises :** Visualisation OHLC interactive via Plotly.
*   **Périodes Variables :** Boutons rapides pour passer de 1 jour à 1 an de données.
*   **Moyennes Mobiles (MA) :** Activation dynamique des courbes MA 50 et MA 200 pour identifier les tendances.

### 3. 📊 Dashboard Multi-actifs
*   **Metrics Pro :** Affichage des 3 cryptos majeures (BTC, ETH, SOL) avec variation 24h.
*   **Top Cryptos :** Tableau extensible affichant le Top 7 du marché en un coup d'œil.

---

## 📂 Structure des Fichiers

*   `app.py` : L'interface utilisateur, le style CSS et la logique d'affichage.
*   `fetcher.py` : Le moteur de données utilisant l'API `yfinance`.
*   `requirements.txt` : Liste des bibliothèques nécessaires.

---

## 🛡️ Résolution des problèmes
*   **Erreur Protobuf :** Si Streamlit ne se lance pas, installez `pip install "protobuf<4"`.
*   **Erreur 32-bit :** Assurez-vous de bien utiliser `venv64` comme indiqué dans la section Installation.

---

## ✨ Prochaines étapes suggérées
*   Ajout d'indicateurs RSI et MACD.
*   Gestion d'un portefeuille utilisateur persistant.
*   Alertes de prix par notification sonore.
