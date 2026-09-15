# Tribune : tableau de bord des résultats

Application Streamlit qui donne à voir les résultats du banc **Tribune**, qui mesure l'écart de
performance des grands modèles de langue sur le **français québécois**. Partenariat entre
Cohere, Mila et l'Université Laval.

L'accès passe par un identifiant et un mot de passe : voir
[`explorateur/DEPLOIEMENT.md`](explorateur/DEPLOIEMENT.md).

## Ce que ce dépôt contient, et ce qu'il ne contient pas

**Il ne porte que des scores agrégés.** Une ligne par modèle, tâche et métrique.

Il ne porte **ni les items posés aux modèles, ni leurs réponses, ni aucun extrait de corpus, ni
aucun poids**. Ceux-là vivent dans le dépôt de recherche, qui est privé : les corpus
parlementaires dont le banc est tiré sont sous des licences qui n'en permettent pas la
rediffusion, et les réponses des modèles n'ont pas à être publiées avant l'article.

Les illustrations des fiches de tâches sont celles de la note de contexte du projet : des
exemples fabriqués pour expliquer ce qu'une tâche demande, pas des items du lot.

```
explorateur/          l'application
  fiches-taches.json  ce que chaque tâche demande, extrait de la note de contexte
resultats/            les scores consolidés, une ligne par modèle, tâche et métrique
```

## Faire tourner l'application en local

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m explorateur.empreinte --identifiant vous   # crée un compte
mkdir -p .streamlit && $EDITOR .streamlit/secrets.toml          # y coller le résultat
.venv/bin/streamlit run explorateur/app.py
```

## L'état de la mesure

Le tableau de bord le dit lui-même à chaque page, et c'est voulu : **la comparaison est
incomplète**. Une récolte partielle se lit comme un résultat complet si rien ne dit ce qui
manque.

## Mettre à jour les résultats

Les scores sont produits dans le dépôt de recherche, par `scripts/resultats/consolider.py`, puis
copiés ici. L'application se redéploie d'elle-même à chaque poussée sur `main`.
