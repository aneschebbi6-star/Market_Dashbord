# 🛣️ Roadmap Détaillée : Market Dashboard Pro

Ce document détaille les futures améliorations prévues pour le projet **Market Dashboard Pro**, classées par catégories, avec les étapes de réalisation pas-à-pas pour chaque fonctionnalité.

---

## 1. 📈 Fonctionnalités Financières et Trading

### 1.1 Indicateurs Techniques Supplémentaires (RSI, MACD, Bandes de Bollinger)
**Objectif :** Offrir des outils d'analyse technique plus poussés aux traders.
*   **Étape 1 :** Ajouter la librairie `ta` (Technical Analysis) dans le fichier `requirements.txt`.
*   **Étape 2 :** Dans `fetcher.py`, modifier la fonction qui traite les données Pandas pour calculer le RSI (Relative Strength Index), le MACD et les Bandes de Bollinger sur les données historiques.
*   **Étape 3 :** Dans `views/dashboard.py`, ajouter des cases à cocher (`st.checkbox` ou `st.multiselect`) dans la barre latérale ou au-dessus du graphique pour permettre à l'utilisateur de sélectionner les indicateurs qu'il souhaite afficher.
*   **Étape 4 :** Mettre à jour la fonction de rendu Plotly pour ajouter les courbes supplémentaires sur le graphique en chandelier en fonction de la sélection de l'utilisateur.

### 1.2 Comparaison d'Actifs (Overlay Chart)
**Objectif :** Permettre de visualiser la corrélation entre deux cryptomonnaies.
*   **Étape 1 :** Dans `views/sidebar.py`, ajouter un second sélecteur de crypto (optionnel) intitulé "Comparer avec".
*   **Étape 2 :** Dans `app.py` et `fetcher.py`, si une deuxième crypto est sélectionnée, récupérer également ses données historiques pour la même période.
*   **Étape 3 :** Normaliser les prix en pourcentages (Base 100 au début de la période) pour que la comparaison visuelle soit pertinente.
*   **Étape 4 :** Créer une nouvelle figure Plotly dans `dashboard.py` qui trace les deux courbes de performance en pourcentage l'une sur l'autre.

### 1.3 Gestion de Portefeuille (Portfolio Tracking / Simulateur)
**Objectif :** Permettre à l'utilisateur de simuler des achats et suivre ses profits/pertes.
*   **Étape 1 :** Créer un système de stockage local simple (ex: un fichier `portfolio.json` ou utiliser `st.session_state` pour une session temporaire).
*   **Étape 2 :** Créer une nouvelle vue `views/portfolio.py`.
*   **Étape 3 :** Ajouter un formulaire (`st.form`) permettant de saisir : la crypto, la quantité achetée, et le prix d'achat.
*   **Étape 4 :** Développer la logique dans `controllers/portfolio_controller.py` pour sauvegarder ces données.
*   **Étape 5 :** Afficher un tableau (`st.dataframe`) récapitulatif du portefeuille avec le calcul en temps réel du PnL (Profit and Loss) en appelant `fetcher.py` pour les prix actuels.

---

## 2. 🤖 Intelligence Artificielle et Données Avancées

### 2.1 Analyse de Sentiment (News)
**Objectif :** Estimer si l'actualité du jour est positive ou négative pour une crypto.
*   **Étape 1 :** S'inscrire sur une API d'actualités gratuite (ex: *CryptoPanic API* ou *NewsAPI*) et ajouter la clé API dans un fichier `.env`.
*   **Étape 2 :** Créer une fonction dans `fetcher.py` pour récupérer les 10 derniers gros titres d'actualité concernant la crypto sélectionnée.
*   **Étape 3 :** Intégrer la librairie `VADER Sentiment Analysis` ou `TextBlob` (en Python) pour attribuer un score (de -1 à 1) à chaque titre.
*   **Étape 4 :** Dans `views/dashboard.py`, afficher une "Jauge de Sentiment" (Plotly Gauge) allant de "Bearish" (Rouge) à "Bullish" (Vert) basée sur la moyenne des scores.
*   **Étape 5 :** Lister les 3 actualités les plus impactantes sous la jauge.

### 2.2 Prévision de Tendance (Machine Learning avec Prophet)
**Objectif :** Donner une indication visuelle de la tendance future basée sur l'historique.
*   **Étape 1 :** Ajouter `prophet` au `requirements.txt`.
*   **Étape 2 :** Créer un fichier `controllers/ml_predictor.py` qui prend un DataFrame Pandas historique, le formate (colonnes 'ds' et 'y'), et entraîne un modèle Prophet rapide.
*   **Étape 3 :** Générer une prédiction sur les 7 prochains jours.
*   **Étape 4 :** Ajouter un bouton toggle "Afficher les prédictions (AI)" dans l'interface. S'il est activé, ajouter la zone de prévision sur le graphique principal Plotly.

---

## 3. 🎨 Expérience Utilisateur (UI/UX)

### 3.1 Exportation de Données CSV/Excel
**Objectif :** Permettre l'extraction de données pour analyse externe.
*   **Étape 1 :** Dans `views/dashboard.py`, après l'affichage du tableau de données brutes, utiliser la méthode `.to_csv()` de Pandas pour convertir les données en texte.
*   **Étape 2 :** Utiliser le composant natif `st.download_button` de Streamlit en lui passant le CSV généré.
*   **Étape 3 :** Styliser le bouton pour qu'il s'intègre bien au design glassmorphism du projet.

### 3.2 Système d'Alertes de Prix (Interface)
**Objectif :** Avertir l'utilisateur lorsque certains seuils sont atteints.
*   **Étape 1 :** Dans la sidebar, ajouter deux champs numériques "Alerte si prix >" et "Alerte si prix <".
*   **Étape 2 :** Stocker ces valeurs dans `st.session_state`.
*   **Étape 3 :** À chaque rafraîchissement des données (ou via un intervalle via le composant `st_autorefresh`), comparer le prix actuel avec les seuils.
*   **Étape 4 :** Déclencher une notification visuelle avec `st.toast()` et un effet sonore (optionnel) si le seuil est franchi.

---

## 4. ⚙️ Améliorations Techniques et Code

### 4.1 Optimisation des Performances (Caching)
**Objectif :** Accélérer l'application et réduire la charge sur les APIs gratuites.
*   **Étape 1 :** Inspecter `fetcher.py`. Identifier toutes les fonctions effectuant des requêtes web (`yfinance`, `requests`).
*   **Étape 2 :** Appliquer le décorateur `@st.cache_data(ttl=300)` au-dessus de ces fonctions (300 secondes = 5 minutes).
*   **Étape 3 :** Tester en changeant d'onglet dans Streamlit pour vérifier que les données se chargent instantanément grâce au cache.
*   **Étape 4 :** Ajouter un bouton discret "Rafraîchir les données" qui permet à l'utilisateur de forcer l'effacement du cache (`st.cache_data.clear()`).

### 4.2 Tests Unitaires (Qualité logicielle)
**Objectif :** Assurer la robustesse de l'application pour des déploiements professionnels.
*   **Étape 1 :** Créer un répertoire `tests/` à la racine du projet.
*   **Étape 2 :** Ajouter le framework `pytest` au `requirements.txt`.
*   **Étape 3 :** Créer `tests/test_auth.py` pour tester les fonctions de connexion (vérifier qu'un mauvais mot de passe est bien rejeté).
*   **Étape 4 :** Créer `tests/test_fetcher.py` pour tester que l'API renvoie bien un DataFrame non vide pour des tickers connus comme 'BTC-USD'.
*   **Étape 5 :** Documenter la commande `pytest` dans le `README.md` pour les futurs contributeurs.
