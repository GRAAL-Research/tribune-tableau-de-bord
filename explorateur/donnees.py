"""Lecture de la table consolidée, et ce qu'elle dit de sa propre complétude.

Aucune métrique n'est recalculée ici : la table vient de `scripts/resultats/consolider.py`,
qui la tire des fichiers de scores. Ce module la relit, la met en forme, et **rappelle ce
qu'elle ne couvre pas**.

Les chaînes destinées au lecteur portent leurs accents ; le code et les commentaires suivent
la convention du dépôt, qui les omet.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any

import pandas as pd


# **Le tableau de bord ne lit que des artefacts publies, jamais le banc.** Importer
# `tribune.benchmark.prompts` entrainait `tribune/__init__.py`, donc `datasets`, donc plusieurs
# centaines de megaoctets : un serveur web qui n'affiche que des chiffres n'a rien a faire d'un
# chargeur de corpus. Mesure du 15 septembre 2026 : le deploiement echouait sur
# « ModuleNotFoundError: No module named 'datasets' ». Les denominateurs viennent desormais du
# resume ecrit par `scripts/resultats/consolider.py`, au moment ou la table est produite.
RACINE = pathlib.Path(__file__).resolve().parent.parent
RESULTATS = RACINE / "resultats"
FLOTTE = RACINE / "tribune" / "benchmark" / "fleet_local.json"

# Les taches du banc dans l'ordre du protocole. Le tri alphabetique placerait `2a` avant `1h`
# sur une liste melee ; l'ordre du protocole est celui que le lecteur attend.
ORDRE_DES_TACHES = (
    "0a-short",
    "0a-long",
    "0b",
    "0c",
    "0d",
    "0e",
    "0f",
    "0gi-fr",
    "0gi-en",
    "0gii",
    "0giii",
    "0h",
    "0i",
    "0j",
    "0k",
    "0l",
    "0m",
    "0n",
    "1a",
    "1b",
    "1c",
    "1d",
    "1e",
    "1f",
    "1g",
    "1h",
    "1i",
    "1j",
    "2a",
    "2b",
)

# **C'est leur ecart que Tribune mesure**, pas leurs niveaux pris separement.
FAMILLES = {"socle": "Socle, français général", "quebec": "Français québécois"}

# Noms lisibles des metriques. Les clefs brutes -- `accuracy_hors_abstention`,
# `span_containment` -- sont celles du code de notation ; les afficher telles quelles oblige
# le lecteur a deviner ce qu'elles mesurent, et les traduire dans chaque page les ferait
# diverger. Une seule table, ici.
NOMS_DE_METRIQUES = {
    "abstention_rate": "Taux d'abstention",
    "accuracy": "Exactitude",
    "accuracy_hors_abstention": "Exactitude quand le modèle répond",
    "attribution_verified_share": "Part d'attributions vérifiées",
    "chance_level": "Niveau du hasard",
    "containment_verbosity": "Verbosité de la réponse",
    "definition_accuracy": "Exactitude de la définition",
    "detection_accuracy": "Exactitude du repérage",
    "human_ceiling": "Plafond humain",
    "macro_f1": "F1 macro",
    "majority_class_rate": "Part de la classe majoritaire",
    "mean_options": "Nombre moyen d'options",
    "num_answered": "Items avec une réponse",
    "num_definitions_scored": "Définitions notées",
    "num_detected": "Termes repérés",
    "num_items": "Items",
    "num_items_with_ceiling": "Items avec un plafond humain",
    "num_items_with_rules_choice": "Items avec un choix de règles",
    "num_no_term": "Items sans terme à repérer",
    "num_off_label": "Réponses hors étiquettes",
    "question_period_share": "Part de période de questions",
    "rules_baseline_accuracy": "Exactitude d'une base de règles",
    "span_containment": "Contenance de la référence",
}

# Ce que chaque métrique veut dire, pour l'infobulle. Une métrique dont personne ne sait
# quelle question elle pose se cite de travers.
SENS_DES_METRIQUES = {
    "accuracy": "Sur **tous** les items : une absence de réponse compte comme une erreur.",
    "accuracy_hors_abstention": (
        "Sur les seuls items où le modèle a répondu. Répond à « quand il répond, a-t-il "
        "raison ? », et se lit toujours avec le taux d'abstention à côté."
    ),
    "abstention_rate": "Part des items où le modèle n'a produit aucune réponse exploitable.",
    "macro_f1": "F1 moyenné par classe : une classe rare pèse autant qu'une classe fréquente.",
    "human_ceiling": "Ce qu'une personne obtient sur les mêmes items. Ce n'est pas un score de modèle.",
    "chance_level": "Ce qu'obtiendrait une réponse au hasard. Ce n'est pas un score de modèle.",
    "majority_class_rate": "Ce qu'obtiendrait qui répondrait toujours la classe la plus fréquente.",
    "rules_baseline_accuracy": "Ce qu'obtient une base de règles sans modèle de langue.",
    "containment_verbosity": "Rapport de longueur entre la réponse et la référence. 1,0 est idéal.",
}


# Ordre d'affichage des metriques, du plus decisif au plus accessoire. **Le tri alphabetique
# mettait « Contenance de la reference » avant « Exactitude »** : la mesure principale d'une
# tache se trouvait en troisieme colonne, et l'oeil la cherchait a chaque fois.
ORDRE_DES_METRIQUES = (
    "accuracy",
    "macro_f1",
    "detection_accuracy",
    "definition_accuracy",
    "span_containment",
    "accuracy_hors_abstention",
    "abstention_rate",
    "containment_verbosity",
    "human_ceiling",
    "chance_level",
    "majority_class_rate",
    "rules_baseline_accuracy",
    "attribution_verified_share",
    "question_period_share",
    "mean_options",
)

# Reperes qui bornent une metrique par le bas : en dessous, un modele ne fait pas mieux que
# repondre sans lire. C'est l'ancrage d'une echelle de couleur qui veut dire quelque chose.
PLANCHERS = {"chance_level", "majority_class_rate", "rules_baseline_accuracy"}


def rang_de_metrique(clef: str) -> int:
    """Rang d'affichage d'une metrique ; les inconnues passent en fin, par ordre alphabetique."""
    try:
        return ORDRE_DES_METRIQUES.index(clef)
    except ValueError:
        return len(ORDRE_DES_METRIQUES)


def metriques_ordonnees(clefs: list[str]) -> list[str]:
    """Trie des clefs de metriques par importance, puis par nom."""
    return sorted(clefs, key=lambda c: (rang_de_metrique(c), c))


def plancher_de_la_tache(table: pd.DataFrame, tache: str) -> float | None:
    """Le repere le plus haut qui borne cette tache par le bas, s'il y en a un.

    Sert d'ancrage a l'echelle de couleur : un degrade qui part du minimum observe est
    decoratif, un degrade qui part du hasard dit si le modele fait mieux que deviner.
    """
    reperes = table[(table["tache"] == tache) & (table["metrique"].isin(PLANCHERS))]
    return float(reperes["valeur"].max()) if not reperes.empty else None


def nom_de_metrique(clef: str) -> str:
    """Nom lisible d'une métrique, ou sa clef brute si elle n'est pas encore nommée."""
    return NOMS_DE_METRIQUES.get(clef, clef.replace("_", " "))


def recoltes() -> list[str]:
    """Noms des récoltes consolidées disponibles, la plus récente d'abord."""
    return sorted((c.stem for c in RESULTATS.glob("*.csv")), reverse=True)


def charger(recolte: str) -> pd.DataFrame:
    """Relit une récolte consolidée, triée dans l'ordre du protocole."""
    table = pd.read_csv(RESULTATS / f"{recolte}.csv")
    rang = {tache: index for index, tache in enumerate(ORDRE_DES_TACHES)}
    table["rang_tache"] = table["tache"].map(lambda t: rang.get(t, len(rang)))
    table["metrique_lisible"] = table["metrique"].map(nom_de_metrique)
    return table.sort_values(["rang_tache", "modele", "metrique"]).reset_index(drop=True)


def resume(recolte: str) -> dict[str, Any]:
    """Le résumé écrit par le consolidateur."""
    chemin = RESULTATS / f"{recolte}-resume.json"
    return dict(json.loads(chemin.read_text(encoding="utf-8"))) if chemin.exists() else {}


def flotte_servie(recolte: str) -> list[str]:
    """Modèles que la flotte déclarait servir quand la récolte a été consolidée.

    **Le dénominateur ne se devine pas depuis la table.** Une table de vingt-neuf modèles se
    lit comme une comparaison complète si rien ne dit combien le banc en vise. Le compte vient
    du résumé, qui l'a lu dans la flotte au moment de produire la table : il décrit donc l'état
    du banc à cette date, et non celui d'aujourd'hui.
    """
    return [str(nom) for nom in resume(recolte).get("flotte_servie", [])]


def taches_par_famille(recolte: str) -> dict[str, list[str]]:
    """Les tâches que le contrat d'invites déclarait, par famille."""
    inventaire = resume(recolte).get("taches_par_famille") or {}
    return {famille: [str(t) for t in taches] for famille, taches in inventaire.items()}


def couverture(table: pd.DataFrame, recolte: str) -> dict[str, Any]:
    """Ce que la récolte couvre, rapporté à ce que le banc vise.

    Trois questions distinctes, et les confondre est la façon la plus simple de lire une
    récolte partielle comme un résultat : combien de modèles ont **au moins une** tâche notée,
    combien en ont **toutes** celles qui existent, et quelle part des couples modèle-tâche du
    banc entier est notée.
    """
    contrat = taches_par_famille(recolte)
    flotte = flotte_servie(recolte)
    total_taches = sum(len(taches) for taches in contrat.values())
    taches_vues = sorted(set(table["tache"].unique()))
    par_modele = table.groupby("modele")["tache"].nunique()
    complets = par_modele[par_modele >= len(taches_vues)]
    par_famille = {
        famille: sorted(set(taches) & set(taches_vues)) for famille, taches in contrat.items()
    }
    return {
        "modeles_vus": int(par_modele.size),
        "modeles_flotte": len(flotte),
        "modeles_complets": int(complets.size),
        "taches_vues": len(taches_vues),
        "taches_banc": total_taches,
        "par_famille": {
            famille: {"vues": len(vues), "total": len(contrat[famille])}
            for famille, vues in par_famille.items()
        },
        "couples_notes": len(table.groupby(["modele", "tache"]).size()),
        "couples_banc": len(flotte) * total_taches,
        "mesures": len(table),
    }


def manquants(table: pd.DataFrame, recolte: str) -> list[str]:
    """Modèles de la flotte absents de cette récolte."""
    presents = set(table["modele"].unique())
    return [nom for nom in flotte_servie(recolte) if nom not in presents]


def tableau_large(table: pd.DataFrame, metrique: str) -> pd.DataFrame:
    """Croise modèles et tâches pour une métrique donnée.

    Les cases vides sont **vides**, jamais zéro : une tâche qui n'expose pas cette métrique et
    une tâche où le modèle aurait obtenu zéro ne se ressemblent pas, et les confondre est la
    façon la plus simple de publier un faux.
    """
    choix = table[table["metrique"] == metrique]
    if choix.empty:
        return pd.DataFrame()
    large = choix.pivot_table(
        index="modele", columns="tache", values="valeur", aggfunc="first", dropna=False
    )
    large = large[[t for t in ORDRE_DES_TACHES if t in large.columns]]
    large["moyenne"] = large.mean(axis=1, skipna=True)
    return large.sort_values("moyenne", ascending=False)


PREFIXE_BASELINE = "baseline-"


def est_une_baseline(nom: str) -> bool:
    """Vrai si cette ligne est une baseline et non un modèle de langue."""
    return str(nom).startswith(PREFIXE_BASELINE)


def carte_de_chaleur(table: pd.DataFrame, metrique: str = "accuracy") -> pd.DataFrame:
    """Modèles en lignes, tâches en colonnes : toute la récolte en une image."""
    return tableau_large(table, metrique).drop(columns=["moyenne"], errors="ignore")


def titres_des_taches(table: pd.DataFrame) -> dict[str, str]:
    """Titre lisible de chaque tâche, tel que le protocole la nomme."""
    paires = table[["tache", "titre"]].drop_duplicates()
    return dict(zip(paires["tache"], paires["titre"], strict=True))
