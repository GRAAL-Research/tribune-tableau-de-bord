"""Mur d'authentification de l'explorateur, par identifiant et mot de passe.

**Ce que ce mur protege, et ce qu'il ne protege pas.** Il empeche un visiteur de passage de
lire des resultats non publies. Ce n'est pas un systeme d'authentification d'entreprise : pas
de second facteur, pas de revocation de session, pas de journal d'acces. Pour des resultats de
recherche avant publication, c'est le bon niveau ; pour des donnees personnelles, il ne le
serait pas.

**Les mots de passe ne sont jamais dans le depot.** Ils vivent dans `st.secrets`, c'est-a-dire
dans `.streamlit/secrets.toml` en local -- ignore par git -- et dans la configuration de
l'hebergeur en ligne. Le depot ne porte qu'un gabarit sans valeur.

**Ils sont compares par empreinte, jamais en clair.** Une empreinte PBKDF2-SHA256 avec sel :
la lecture des secrets ne revele alors aucun mot de passe utilisable ailleurs, ce qui compte
parce que les gens reutilisent les leurs.

La comparaison passe par `hmac.compare_digest`, qui prend le meme temps quel que soit
l'endroit ou les chaines different. Une comparaison ordinaire s'arrete au premier octet
different et laisse deviner le secret octet par octet.
"""

from __future__ import annotations

import binascii
import hashlib
import hmac
import secrets

import streamlit as st

from explorateur import textes


# Cout de la derivation. 600 000 iterations est la recommandation OWASP 2023 pour
# PBKDF2-SHA256 ; le retard d'une seconde a la connexion est invisible pour une personne et
# couteux pour qui essaie un dictionnaire.
ITERATIONS = 600_000
OCTETS_DE_SEL = 16


def empreinte(mot_de_passe: str, sel: bytes | None = None) -> str:
    """Rend l'empreinte d'un mot de passe, sous la forme ``sel$empreinte`` en hexadecimal."""
    sel = sel or secrets.token_bytes(OCTETS_DE_SEL)
    derive = hashlib.pbkdf2_hmac("sha256", mot_de_passe.encode("utf-8"), sel, ITERATIONS)
    return f"{binascii.hexlify(sel).decode()}${binascii.hexlify(derive).decode()}"


def _correspond(mot_de_passe: str, attendu: str) -> bool:
    """Vrai si le mot de passe donne produit l'empreinte attendue."""
    try:
        sel_hex, empreinte_hex = attendu.split("$", 1)
        sel = binascii.unhexlify(sel_hex)
    except (ValueError, binascii.Error):
        return False
    calcule = hashlib.pbkdf2_hmac("sha256", mot_de_passe.encode("utf-8"), sel, ITERATIONS)
    return hmac.compare_digest(binascii.hexlify(calcule).decode(), empreinte_hex)


def _comptes() -> dict[str, str]:
    """Les comptes declares, ou un dictionnaire vide si la configuration manque."""
    try:
        bruts = st.secrets["comptes"]
    except (KeyError, FileNotFoundError):
        return {}
    return {str(nom): str(valeur) for nom, valeur in dict(bruts).items()}


def _refuser_faute_de_configuration() -> None:
    """Explique comment configurer, plutot que de laisser entrer.

    **Sans comptes declares, l'acces est refuse et non ouvert.** Un mur qui s'efface quand sa
    configuration manque est pire qu'aucun mur : il donne l'impression d'exister.
    """
    st.error("Aucun compte n'est configure : l'acces est refuse.")
    st.markdown(
        "Creer `.streamlit/secrets.toml` a partir de `secrets.toml.exemple`, ou renseigner "
        "les secrets chez l'hebergeur. Les empreintes se fabriquent avec :\n\n"
        "```bash\npython -m explorateur.empreinte\n```"
    )


def exiger_une_connexion(langue: str = "fr") -> str:
    """Bloque tant que la personne n'est pas connue, et rend son identifiant.

    Streamlit rejoue le script en entier a chaque interaction : l'etat de connexion vit donc
    dans `st.session_state`, et `st.stop()` interrompt le rendu de tout ce qui suit.
    """
    if st.session_state.get("connecte"):
        return str(st.session_state["identifiant"])

    comptes = _comptes()
    st.title(textes.t("titre_connexion", langue))
    if not comptes:
        _refuser_faute_de_configuration()
        st.stop()

    with st.form("connexion"):
        identifiant = st.text_input(textes.t("identifiant", langue))
        mot_de_passe = st.text_input(textes.t("mot_de_passe", langue), type="password")
        envoye = st.form_submit_button(textes.t("se_connecter", langue))

    if envoye:
        attendu = comptes.get(identifiant)
        # **Le meme message dans les deux cas.** Distinguer « identifiant inconnu » de « mot
        # de passe errone » dit a qui cherche quels identifiants existent.
        if attendu and _correspond(mot_de_passe, attendu):
            st.session_state["connecte"] = True
            st.session_state["identifiant"] = identifiant
            st.rerun()
        else:
            st.error(textes.t("identifiants_errones", langue))
    st.stop()
    return ""
