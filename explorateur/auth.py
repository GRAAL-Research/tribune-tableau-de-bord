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
from streamlit.errors import StreamlitSecretNotFoundError

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


def _ressemble_a_une_empreinte(valeur: object) -> bool:
    """Vrai si cette valeur a la forme `sel$empreinte`, en hexadecimal.

    Sert a reconnaitre un compte pose a la racine des secrets, sans l'en-tete de section.
    """
    texte = str(valeur)
    sel, separateur, derive = texte.partition("$")
    return bool(separateur) and all(
        part and len(part) % 2 == 0 and set(part) <= set("0123456789abcdef")
        for part in (sel, derive)
    )


def _comptes() -> dict[str, str]:
    """Les comptes declares, sous l'en-tete `[comptes]` ou a la racine des secrets.

    **La racine est acceptee parce que l'en-tete s'oublie.** Mesure du 15 septembre 2026,
    premiere configuration de l'hebergeur : les deux lignes avaient ete collees sans le
    `[comptes]` qui les precede, et l'application refusait l'acces a tout le monde en disant
    « aucun compte n'est configure » -- ce qui etait vrai de son point de vue et incomprehensible
    du cote de qui venait de les coller. Une entree de racine dont la valeur a la forme d'une
    empreinte est un compte ; une variable d'environnement ordinaire ne l'a pas.
    """
    comptes: dict[str, str] = {}
    try:
        secrets = dict(st.secrets)
    except (FileNotFoundError, StreamlitSecretNotFoundError):
        return {}
    sous_entete = secrets.get("comptes")
    if sous_entete is not None:
        comptes.update({str(nom): str(valeur) for nom, valeur in dict(sous_entete).items()})
    comptes.update({
        str(nom): str(valeur)
        for nom, valeur in secrets.items()
        if nom != "comptes" and _ressemble_a_une_empreinte(valeur)
    })
    return comptes


def _refuser_faute_de_configuration() -> None:
    """Explique comment configurer, plutot que de laisser entrer.

    **Sans comptes declares, l'acces est refuse et non ouvert.** Un mur qui s'efface quand sa
    configuration manque est pire qu'aucun mur : il donne l'impression d'exister.
    """
    st.error("Aucun compte n'est configure : l'acces est refuse.")
    st.markdown(
        "Les comptes vont dans les secrets, **precedes de leur en-tete de section** :\n\n"
        '```toml\n[comptes]\nmarie = "a1b2...$c3d4..."\n```\n\n'
        "En local, dans `.streamlit/secrets.toml` ; en ligne, dans la configuration de "
        "l'hebergeur. Les empreintes se fabriquent avec :\n\n"
        "```bash\npython -m explorateur.empreinte --identifiant marie\n```"
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
