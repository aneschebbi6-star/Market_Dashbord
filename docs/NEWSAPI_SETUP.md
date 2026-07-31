# 📰 Configuration NewsAPI - Guide Complet

## Obtenir une Clé API NewsAPI Gratuite

### Étape 1 : Créer un compte
1. Allez sur [https://newsapi.org/](https://newsapi.org/)
2. Cliquez sur **"Get API Key"** (en haut à droite)
3. Remplissez le formulaire d'inscription :
   - Email
   - Prénom/Nom
   - Type d'accès : choisissez **"Developer"** (gratuit)

### Étape 2 : Confirmer votre email
- Vous recevrez un email de confirmation
- Cliquez sur le lien pour activer votre compte

### Étape 3 : Récupérer votre clé API
1. Connectez-vous à votre compte
2. Allez à **"Dashboard"** ou **"Account"**
3. Vous verrez votre clé API (format : longue chaîne de caractères)
4. Copiez-la

### Étape 4 : Configurer Market Dashboard Pro

**Option A : Via le fichier `.env` (recommandé)**

1. Ouvrez le fichier `.env` à la racine du projet
2. Cherchez la ligne `NEWSAPI_KEY=`
3. Remplacez par : `NEWSAPI_KEY=votre_clé_copiée`
4. Sauvegardez le fichier

**Exemple:**
```env
NEWSAPI_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

### Étape 5 : Redémarrer l'application

Stoppez et relancez Streamlit pour charger la nouvelle configuration :

```bash
streamlit run app.py
```

---

## Vérifier la Configuration

Une fois la clé API configurée, vous verrez dans les logs :
```
✓ Real-time news loaded for bitcoin from NewsAPI
```

### Limites du plan gratuit NewsAPI
- **100 requêtes/jour** (suffisant pour le développement)
- Accès à toutes les sources de news
- 1 mois d'historique d'articles

> Pour plus de requêtes, contactez NewsAPI pour un plan payant.

---

## Dépannage

### Problème : "NEWSAPI_KEY not configured"
- ✅ Vérifiez que vous avez copié/collé correctement la clé dans `.env`
- ✅ Assurez-vous qu'il n'y a pas d'espaces avant/après la clé
- ✅ Redémarrez l'application

### Problème : "NEWSAPI quota exceeded"
- L'application a dépassé 100 requêtes/jour
- Attendez jusqu'à minuit UTC pour réinitialiser le quota
- Ou utilisez le plan Premium de NewsAPI

### Problème : Aucune actualité trouvée
- Vérifiez que votre clé API est correcte
- Vérifiez votre connexion Internet
- Le système basculera automatiquement sur les données de démo

---

## Mode Fallback (Données de Démo)

Si NewsAPI n'est pas configurée ou indisponible, l'application affichera automatiquement des actualités de démonstration réalistes. C'est normal et l'application continuera à fonctionner !

