"""Tableau de bord des résultats de Tribune : le banc, ses tâches, et ce qui est mesuré.

Lancé en local par ``streamlit run explorateur/app.py``. L'accès passe par un identifiant et
un mot de passe déclarés dans les secrets ; voir `explorateur/auth.py`.

**Ce que ce tableau de bord n'est pas.** Il ne recalcule aucune métrique et ne rend aucun
verdict : il donne à voir une table consolidée, et rappelle ce qu'elle ne couvre pas. Un
tableau de vingt-neuf modèles qui ne dirait pas qu'il en manque onze se lirait comme une
comparaison complète.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from explorateur import donnees, textes
from explorateur.auth import exiger_une_connexion


st.set_page_config(page_title="Tribune", page_icon="TR", layout="wide")

NOTE_PDF = donnees.RACINE / "rapport" / "litterature" / "contexte-modeles-et-taches.pdf"
FICHES = pathlib.Path(__file__).resolve().parent / "fiches-taches.json"

langue = st.session_state.get("langue", "fr")
identifiant = exiger_une_connexion(langue)


def _t(clef: str) -> str:
    """Raccourci de traduction, dans la langue choisie."""
    return textes.t(clef, langue)


def _fiches() -> dict[str, dict[str, str]]:
    """Les fiches de tâches extraites de la note de contexte."""
    if not FICHES.exists():
        return {}
    return dict(json.loads(FICHES.read_text(encoding="utf-8")))


def _texte_des_cases(large: pd.DataFrame, manquant: str) -> pd.DataFrame:
    """Rend un tableau de nombres en texte, case vide comprise.

    **`st.dataframe` ignore le `na_rep` d'un Styler.** Le rendu passe par Arrow, qui écrit son
    propre marqueur de valeur absente : les cases vides s'affichaient « None », ce qui se lit
    comme une panne plutôt que comme « la tâche n'expose pas cette métrique ». Le formatage se
    fait donc ici, avant l'affichage, et non dans une mise en forme que le rendu peut écarter.
    """
    return large.map(lambda valeur: manquant if pd.isna(valeur) else f"{valeur:.1f}")


def _ligne_de_couverture(part: dict[str, Any]) -> str:
    """La couverture en une ligne, pour tenir au-dessus du contenu de chaque page."""
    return (
        f"**{part['modeles_vus']} / {part['modeles_flotte']}** {_t('modeles_vus').lower()} · "
        f"**{part['taches_vues']} / {part['taches_banc']}** {_t('taches_notees').lower()} · "
        f"**{100 * part['couples_notes'] / max(part['couples_banc'], 1):.0f} %** "
        f"{_t('part_du_banc').lower()}"
    )


def _couverture(table: pd.DataFrame, recolte: str) -> None:
    """Ce que la récolte couvre, et surtout ce qu'elle ne couvre pas.

    **Les deux mises en garde sont sur toutes les pages de résultats, et nommées comme telles.**
    Elles étaient repliées ailleurs que sur le classement, et l'une des deux s'affichait en
    bleu, qui se lit comme une information neutre : les deux disent pourtant la même chose,
    que ces chiffres ne portent pas ce qu'ils semblent porter. Une personne qui arrive par un
    lien direct sur « Par tâche » doit les voir là aussi.
    """
    part = donnees.couverture(table, recolte)
    st.caption(_ligne_de_couverture(part))
    with st.expander(_t("couverture_et_reserves"), expanded=True):
        for famille, compte in part["par_famille"].items():
            nom = donnees.FAMILLES.get(famille, famille)
            if compte["vues"] == 0:
                st.markdown(f"- {_t('socle_pas_lance').format(total=compte['total'])}")
                continue
            st.progress(
                compte["vues"] / max(compte["total"], 1),
                text=f"{nom} : {compte['vues']} / {compte['total']}",
            )
        absents = donnees.manquants(table, recolte)
        if absents:
            st.warning(
                f"**{_t('avertissement')} 1 / 2 — {_t('incomplet_titre')}**  \n"
                + _t("incomplet").format(n=len(absents), noms=", ".join(absents)),
                icon=":material/warning:",
            )
        if part["par_famille"].get("socle", {}).get("vues", 0) == 0:
            st.warning(
                f"**{_t('avertissement')} 2 / 2 — {_t('socle_absent_titre')}**  \n"
                + _t("socle_absent"),
                icon=":material/warning:",
            )


def _page_ensemble(table: pd.DataFrame, recolte: str) -> None:
    """Tout ce qu'il faut savoir d'une récolte, sans avoir à naviguer.

    **Une vue d'ensemble n'est pas un classement en plus petit.** Le projet cherche un
    diagnostic -- quelles tâches séparent, où un modèle n'apporte rien -- et c'est cela que
    cette page met devant, avant le palmarès.
    """
    st.title(_t("onglet_ensemble"))
    _couverture(table, recolte)

    grand = donnees.tableau_large(table, "accuracy")
    if grand.empty:
        st.info(_t("aucune_tache_expose"))
        return

    st.subheader(_t("tete_de_classement"))
    tete = grand["moyenne"].head(5)
    colonnes = st.columns(len(tete))
    for colonne, (nom, valeur) in zip(colonnes, tete.items(), strict=True):
        colonne.metric(str(nom), f"{valeur:.1f}")

    st.subheader(_t("carte_de_chaleur"))
    st.caption(_t("carte_legende"))
    _carte(donnees.carte_de_chaleur(table), table)

    st.subheader(_t("dispersion"))
    st.caption(_t("dispersion_legende"))
    _nuage_par_tache(table)


def _carte(large: pd.DataFrame, table: pd.DataFrame) -> None:
    """Dessine la carte de chaleur des modèles par tâche, repères compris.

    **Une vraie image, pas un tableau colorié.** Vingt-neuf lignes sur dix colonnes ne se
    lisent d'un coup d'oeil que si la couleur porte la valeur. L'échelle va de 0 à 100 et non
    du minimum au maximum observés : sans cela, la couleur dirait le rang dans la récolte
    plutôt que la performance.
    """
    figure, axes = plt.subplots(figsize=(1.1 * len(large.columns) + 3, 0.30 * len(large) + 1.8))
    image = axes.imshow(large.to_numpy(dtype=float), aspect="auto", cmap="Blues", vmin=0, vmax=100)
    axes.set_yticks(range(len(large)), [str(i) for i in large.index], fontsize=8)
    # **Le repere de chaque tache est marque sous son en-tete.** Une case a 52 % ne se lit pas
    # sans savoir que repondre toujours la classe majoritaire en donne 52 aussi.
    reperes = {
        str(colonne): donnees.plancher_de_la_tache(table, str(colonne))
        for colonne in large.columns
    }
    etiquettes = [
        f"{colonne}\n{reperes[str(colonne)]:.0f}" if reperes.get(str(colonne)) else str(colonne)
        for colonne in large.columns
    ]
    axes.set_xticks(range(len(large.columns)), etiquettes, fontsize=9)
    figure.colorbar(image, ax=axes, shrink=0.6, label="%")
    figure.tight_layout()
    st.pyplot(figure, use_container_width=True)
    plt.close(figure)


def _nuage_par_tache(table: pd.DataFrame) -> None:
    """Chaque modèle en un point, tâche par tâche, avec le repère en pointillé.

    **Le pointillé est ce qui rend un score lisible.** Une exactitude de 52 % ne dit rien tant
    qu'on ignore que répondre toujours la classe majoritaire en donne 52 aussi : les points
    sous la ligne sont des modèles qui n'apportent rien sur cette tâche. Les tâches sans repère
    publié n'en portent pas, plutôt qu'une ligne devinée.
    """
    choix = table[(table["metrique"] == "accuracy") & (table["nature"] == "performance")]
    if choix.empty:
        return
    taches = [t for t in donnees.ORDRE_DES_TACHES if t in set(choix["tache"])]
    figure, axes = plt.subplots(figsize=(1.0 * len(taches) + 3, 4.2))
    for rang, tache in enumerate(taches):
        valeurs = choix[choix["tache"] == tache]["valeur"].to_numpy(dtype=float)
        axes.scatter([rang] * len(valeurs), valeurs, s=18, alpha=0.55, color="#1f6feb", zorder=3)
        repere = donnees.plancher_de_la_tache(table, tache)
        if repere is not None:
            axes.plot(
                [rang - 0.38, rang + 0.38],
                [repere, repere],
                linestyle=(0, (3, 2)),
                linewidth=1.6,
                color="#c2410c",
                zorder=4,
            )
    axes.set_xticks(range(len(taches)), taches)
    axes.set_ylim(0, 100)
    axes.set_ylabel("%")
    axes.grid(axis="y", alpha=0.25, zorder=0)
    axes.spines[["top", "right"]].set_visible(False)
    # Une legende explicite : un pointille sans nom est un trait decoratif.
    axes.plot([], [], linestyle=(0, (3, 2)), color="#c2410c", label=_t("legende_repere"))
    axes.scatter([], [], s=18, color="#1f6feb", label=_t("legende_modele"))
    axes.legend(loc="lower left", frameon=False, fontsize=9)
    figure.tight_layout()
    st.pyplot(figure, use_container_width=True)
    plt.close(figure)


def _page_projet() -> None:
    """Le rappel du projet, tiré de la note de contexte."""
    st.title(_t("onglet_projet"))
    if NOTE_PDF.exists():
        st.download_button(
            _t("telecharger_note"),
            NOTE_PDF.read_bytes(),
            file_name=NOTE_PDF.name,
            mime="application/pdf",
        )
    for section in textes.PROJET[langue]:
        st.subheader(section["titre"])
        st.markdown(section["corps"])
    st.subheader("Paliers" if langue == "fr" else "Bands")
    for palier in textes.PALIERS:
        st.markdown(f"- **{palier['code']}** — {palier[langue]}")


def _page_taches(table: pd.DataFrame) -> None:
    """Le rappel des tâches, dans la forme de la note : une fiche en bandes par tâche."""
    st.title(_t("onglet_taches"))
    if NOTE_PDF.exists():
        st.download_button(
            _t("telecharger_note"),
            NOTE_PDF.read_bytes(),
            file_name=NOTE_PDF.name,
            mime="application/pdf",
            key="pdf_taches",
        )
    if langue == "fr":
        st.caption(_t("note_en_anglais"))

    fiches = _fiches()
    notees = set(table["tache"].unique())
    bandes = (
        ("GIVEN TO THE MODEL", "donne_au_modele"),
        ("EXPECTED TRUTH", "verite_attendue"),
        ("NOTE", "note"),
        ("CORPUS", "corpus"),
        ("ITEM", "item"),
        ("MOTIF", "motif"),
        ("GROUND TRUTH", "verite_terrain"),
        ("EVALUATION", "evaluation"),
        ("RESERVATION", "reservation"),
    )
    resumes = {tache["code"]: tache for tache in textes.TACHES}

    for code in donnees.ORDRE_DES_TACHES:
        fiche = fiches.get(code)
        if fiche is None:
            continue
        resume = resumes.get(code)
        libelle = resume[langue] if resume else fiche["titre"]
        marque = " ✓" if code in notees else ""
        with st.expander(f"**{code}** — {libelle}{marque}", expanded=False):
            if code not in notees:
                st.caption(_t("pas_evalue"))
            if fiche.get("etat"):
                cle = "en_developpement" if fiche["etat"] == "IN DEVELOPMENT" else "en_refonte"
                st.warning(_t(cle))
            for brute, clef in bandes:
                if fiche.get(brute):
                    st.markdown(f"**{_t(clef)}**")
                    st.markdown(fiche[brute])


def _page_classement(table: pd.DataFrame, recolte: str) -> None:
    """Modèles en lignes, tâches en colonnes, triable sur n'importe quelle colonne."""
    st.title(_t("onglet_classement"))
    _couverture(table, recolte)
    performances = donnees.metriques_ordonnees(
        sorted(table[table["nature"] == "performance"]["metrique"].unique())
    )
    metrique = str(
        st.selectbox(_t("metrique"), performances, index=0, format_func=donnees.nom_de_metrique)
    )
    sens = donnees.SENS_DES_METRIQUES.get(metrique)
    if sens:
        st.caption(sens)
    large = donnees.tableau_large(table, metrique)
    if large.empty:
        st.warning(_t("aucune_tache_expose"))
        return

    st.caption(
        _t("trier_conseil")
        + "  \n"
        + _t("legende_cases_vides").format(
            sans_objet=_t("sans_objet"), pas_evalue=_t("pas_evalue")
        )
        + " "
        + _t("moyenne_avertissement")
    )
    # **Des colonnes numériques, pas un Styler.** Le tri au clic de `st.dataframe` ne porte que
    # sur des colonnes typées ; un tableau rendu en texte se lit mais ne se trie pas.
    #
    # **Une seule barre, sur la moyenne.** Onze colonnes en barres de progression occupaient
    # l'écran entier et repoussaient les chiffres à droite : la barre devenait la donnée et le
    # nombre son annotation. Les tâches restent des nombres, comparables d'un coup d'oeil ; la
    # moyenne garde sa barre, ancrée sur le plus haut repère du jeu d'items plutôt que sur le
    # minimum observé, qui ne dit rien.
    affiche = large.rename(columns={"moyenne": _t("moyenne")})
    affiche.index.name = _t("modele")
    st.dataframe(
        _mise_en_forme(affiche),
        use_container_width=True,
        height=min(60 + 35 * len(affiche), 900),
    )

    titres = donnees.titres_des_taches(table)
    with st.expander(_t("que_mesure_chaque_tache")):
        for tache in large.columns:
            if tache in titres:
                st.markdown(f"**{tache}** : {titres[tache]}")
    st.download_button(
        _t("telecharger_tableau"),
        large.to_csv().encode("utf-8"),
        file_name=f"tribune-{metrique}.csv",
        mime="text/csv",
    )
    with st.expander(_t("latex_pour_article")):
        st.code(_latex(large, metrique, titres), language="latex")


def _mise_en_forme(affiche: pd.DataFrame) -> Any:
    """Le dégradé par colonne, et les baselines en gras.

    **Le dégradé se calcule colonne par colonne.** Une échelle unique sur tout le tableau
    laisserait `2b`, où personne ne dépasse 40, uniformément pâle : la couleur dirait alors la
    difficulté de la tâche plutôt que l'écart entre les modèles, qui est ce qu'on regarde.

    **Les baselines sont en gras parce qu'elles ne sont pas des modèles.** Une ligne
    « hasard » au milieu du classement se lit comme un système évalué tant que rien ne la
    distingue ; en gras, elle se repère comme la référence qu'elle est.
    """
    style = affiche.style.format("{:.1f}", na_rep="—").background_gradient(
        cmap="Blues", axis=0, vmin=0, vmax=100
    )
    return style.apply(
        lambda ligne: [
            "font-weight: 700" if donnees.est_une_baseline(ligne.name) else "" for _ in ligne
        ],
        axis=1,
    )


def _latex(large: pd.DataFrame, metrique: str, titres: dict[str, str]) -> str:
    """Le même tableau en LaTeX, meilleur score en gras, prêt pour l'article."""
    colonnes = list(large.columns)
    lignes = [
        r"\begin{table}[t]",
        r"  \centering",
        r"  \small",
        r"  \begin{tabular}{l" + "r" * len(colonnes) + "}",
        r"    \toprule",
        "    Modele & " + " & ".join(str(c) for c in colonnes) + r" \\",
        r"    \midrule",
    ]
    meilleurs = {colonne: large[colonne].max() for colonne in colonnes}
    for modele, rangee in large.iterrows():
        cases = []
        for colonne in colonnes:
            valeur = rangee[colonne]
            if pd.isna(valeur):
                cases.append("--")
            elif valeur == meilleurs[colonne]:
                cases.append(rf"\textbf{{{valeur:.1f}}}")
            else:
                cases.append(f"{valeur:.1f}")
        nom = str(modele).replace("_", chr(92) + "_")
        lignes.append(f"    {nom} & " + " & ".join(cases) + r" \\")
    nommees = ", ".join(f"{t} {titres.get(t, '')}".strip() for t in colonnes if t in titres)
    lignes += [
        r"    \bottomrule",
        r"  \end{tabular}",
        rf"  \caption{{{donnees.nom_de_metrique(metrique)} par tache. {nommees}.}}",
        rf"  \label{{tab:{metrique}}}",
        r"\end{table}",
    ]
    return "\n".join(lignes)


def _croise(part: pd.DataFrame, index: str) -> pd.DataFrame:
    """Croise une part de table, colonnes ordonnées par importance."""
    large = part.pivot_table(index=index, columns="metrique", values="valeur", aggfunc="first")
    large = large[donnees.metriques_ordonnees(list(large.columns))]
    return large.rename(columns=donnees.nom_de_metrique)


def _page_modele(table: pd.DataFrame, recolte: str) -> None:
    """Toutes les mesures d'un modèle, tâche par tâche."""
    st.title(_t("onglet_modele"))
    _couverture(table, recolte)
    modele = st.selectbox(_t("modele"), sorted(table["modele"].unique()))
    choix = table[table["modele"] == modele]
    for nature, etiquette in (
        ("performance", _t("performances")),
        ("repere", _t("reperes")),
        ("effectif", _t("effectifs")),
    ):
        part = choix[choix["nature"] == nature]
        if part.empty:
            continue
        st.subheader(etiquette)
        if nature == "repere":
            st.caption(_t("reperes_avertissement"))
        large = _croise(part, "tache")
        large.index.name = _t("tache")
        st.dataframe(_texte_des_cases(large, _t("sans_objet")), use_container_width=True)


def _page_tache(table: pd.DataFrame, recolte: str) -> None:
    """Tous les modèles sur une tâche, métrique par métrique."""
    st.title(_t("onglet_tache"))
    _couverture(table, recolte)
    titres = donnees.titres_des_taches(table)
    taches = [t for t in donnees.ORDRE_DES_TACHES if t in set(table["tache"])]
    tache = st.selectbox(_t("tache"), taches, format_func=lambda t: f"{t} — {titres.get(t, '')}")
    choix = table[(table["tache"] == tache) & (table["nature"] == "performance")]
    large = _croise(choix, "modele")
    large.index.name = _t("modele")
    st.caption(_t("trier_conseil"))
    st.dataframe(
        large,
        use_container_width=True,
        height=min(60 + 35 * len(large), 900),
        column_config={
            str(c): st.column_config.NumberColumn(str(c), format="%.1f") for c in large.columns
        },
    )
    reperes = table[(table["tache"] == tache) & (table["nature"] == "repere")]
    if not reperes.empty:
        st.subheader(_t("reperes"))
        st.caption(_t("reperes_avertissement"))
        valeurs = reperes.groupby("metrique")["valeur"].first()
        valeurs.index = [donnees.nom_de_metrique(c) for c in valeurs.index]
        st.dataframe(valeurs.to_frame(_t("valeur")).T, use_container_width=True)


def _page_table(table: pd.DataFrame, recolte: str) -> None:
    """La table longue, filtrable, telle qu'elle est versionnée."""
    st.title(_t("onglet_table"))
    _couverture(table, recolte)
    st.caption(_t("table_versionnee"))
    colonnes = st.columns(3)
    modeles = colonnes[0].multiselect(_t("modele"), sorted(table["modele"].unique()))
    taches = colonnes[1].multiselect(
        _t("tache"), [t for t in donnees.ORDRE_DES_TACHES if t in set(table["tache"])]
    )
    natures = colonnes[2].multiselect(_t("nature"), sorted(table["nature"].unique()))
    filtre = table
    if modeles:
        filtre = filtre[filtre["modele"].isin(modeles)]
    if taches:
        filtre = filtre[filtre["tache"].isin(taches)]
    if natures:
        filtre = filtre[filtre["nature"].isin(natures)]
    lisible = filtre[["modele", "tache", "metrique_lisible", "nature", "valeur"]].rename(
        columns={
            "modele": _t("modele"),
            "tache": _t("tache"),
            "metrique_lisible": _t("metrique"),
            "nature": _t("nature"),
            "valeur": _t("valeur"),
        }
    )
    st.dataframe(lisible, use_container_width=True, height=600, hide_index=True)
    st.download_button(
        _t("telecharger_selection"),
        filtre.to_csv(index=False).encode("utf-8"),
        file_name=f"{recolte}-selection.csv",
        mime="text/csv",
    )


# ---------------------------------------------------------------- navigation
#
# **Les pages vivent dans le menu de gauche, pas dans des onglets.** Six onglets forçaient à
# faire défiler le même en-tête avant chaque contenu, et changer de langue ramenait au premier.
# `st.navigation` porte de vraies sections, garde la page choisie d'un rechargement à l'autre,
# et sépare visuellement les résultats de la documentation.

disponibles = donnees.recoltes()
if not disponibles:
    st.error(_t("recolte_vide"))
    st.stop()

with st.sidebar:
    st.markdown(f"### Tribune\n{_t('connecte')} : **{identifiant}**")
    choisie = st.radio(
        _t("langue"),
        list(textes.LANGUES),
        format_func=lambda code: textes.LANGUES[code],
        index=list(textes.LANGUES).index(langue),
        horizontal=True,
    )
    if choisie != langue:
        st.session_state["langue"] = choisie
        st.rerun()
    recolte_choisie = str(st.selectbox(_t("recolte"), disponibles))

table_courante = donnees.charger(recolte_choisie)
if table_courante.empty:
    st.title(_t("titre"))
    st.info(_t("recolte_vide"))
    st.stop()

navigation = st.navigation({
    _t("section_resultats"): [
        st.Page(
            lambda: _page_ensemble(table_courante, recolte_choisie),
            title=_t("onglet_ensemble"),
            url_path="ensemble",
            default=True,
        ),
        st.Page(
            lambda: _page_classement(table_courante, recolte_choisie),
            title=_t("onglet_classement"),
            url_path="classement",
        ),
        st.Page(
            lambda: _page_modele(table_courante, recolte_choisie),
            title=_t("onglet_modele"),
            url_path="modele",
        ),
        st.Page(
            lambda: _page_tache(table_courante, recolte_choisie),
            title=_t("onglet_tache"),
            url_path="tache",
        ),
        st.Page(
            lambda: _page_table(table_courante, recolte_choisie),
            title=_t("onglet_table"),
            url_path="table",
        ),
    ],
    _t("section_documentation"): [
        st.Page(_page_projet, title=_t("onglet_projet"), url_path="projet"),
        st.Page(
            lambda: _page_taches(table_courante), title=_t("onglet_taches"), url_path="taches"
        ),
    ],
})

with st.sidebar:
    if st.button(_t("se_deconnecter")):
        st.session_state.clear()
        st.rerun()

navigation.run()
