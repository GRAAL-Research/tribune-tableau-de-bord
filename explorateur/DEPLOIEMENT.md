# Déployer le tableau de bord sur Streamlit Community Cloud

Le dépôt `GRAAL-Research/Tribune` est **privé** : Streamlit peut en déployer un, mais il faut
l'y autoriser explicitement. Compter une quinzaine de minutes.

## 1. Créer les identifiants

Un compte par personne, jamais un compte partagé : révoquer l'accès de quelqu'un demanderait
sinon de changer le mot de passe de tout le monde.

```bash
python -m explorateur.empreinte --identifiant marie
```

La commande demande le mot de passe sans écho et rend la ligne à coller :

```
marie = "a1b2c3...$d4e5f6..."
```

Répéter pour chaque personne. **Le mot de passe en clair ne doit apparaître nulle part** : ni
dans le dépôt, ni dans un courriel, ni dans l'historique du shell. Le transmettre par le
gestionnaire de mots de passe de l'équipe, ou de vive voix.

## 2. Déployer

1. Aller sur [share.streamlit.io](https://share.streamlit.io) et se connecter avec le compte
   GitHub qui a accès à `GRAAL-Research/Tribune`.
2. **Authorize Streamlit** pour les dépôts privés, à la première connexion. Streamlit demande
   la portée `repo` ; c'est ce qui lui permet de cloner un dépôt privé.
3. « New app », puis :

   | champ | valeur |
   |---|---|
   | Repository | `GRAAL-Research/Tribune` |
   | Branch | `main` |
   | Main file path | `explorateur/app.py` |
   | Python version | 3.12 ou plus |

4. Avant de cliquer « Deploy », ouvrir **Advanced settings → Secrets** et y coller :

   ```toml
   [comptes]
   marie = "a1b2c3...$d4e5f6..."
   pierre = "..."
   ```

   **Ne pas déployer sans cette étape.** Sans comptes déclarés, l'application refuse l'accès
   et affiche comment la configurer : elle ne s'ouvre pas, mais personne ne peut s'en servir
   non plus.

5. Deploy. Le premier démarrage installe les dépendances et prend quelques minutes.

## 3. Ce que l'hébergeur installe

Streamlit lit le `requirements.txt` le plus proche du script déployé, donc
`explorateur/requirements.txt`, qui ne porte que `streamlit`, `pandas` et `matplotlib`.

Celui de la racine sert à la conversion des corpus et épingle `pyarrow` à une version précise ;
le donner à l'hébergeur ferait installer une pile entière pour un tableau de bord, et
échouerait sur une version de `pyarrow` qu'il n'a pas.

## 4. Vérifier avant de partager le lien

- ouvrir le lien dans une fenêtre de navigation privée : le mur doit apparaître ;
- essayer un mauvais mot de passe : le refus doit être le même message que pour un
  identifiant inconnu ;
- se connecter, et vérifier que la vue d'ensemble affiche des chiffres, donc que
  `resultats/*.csv` est bien arrivé avec le dépôt.

## Ce que ce déploiement suppose, et qu'il faut savoir

**Les résultats sont dans le dépôt.** `resultats/quebec-20260915.csv` fait 364 Ko et voyage
avec le clone : l'application n'a besoin d'aucune base de données. En contrepartie, publier de
nouveaux résultats demande un commit, et l'application se redéploie toute seule à chaque
poussée sur `main`.

**Le mur protège des résultats non publiés, pas des données personnelles.** Pas de second
facteur, pas de révocation de session, pas de journal d'accès. C'est le bon niveau pour des
résultats de recherche avant publication ; ce ne le serait pas pour autre chose.

**Streamlit Community Cloud est hébergé hors du Canada.** Les fichiers déployés sont les
résultats agrégés et la note de contexte ; aucun verbatim de corpus, aucune prédiction brute,
aucun poids de modèle n'y monte. Si cette contrainte devient bloquante, l'application tourne
telle quelle derrière n'importe quel serveur, le mur compris.
