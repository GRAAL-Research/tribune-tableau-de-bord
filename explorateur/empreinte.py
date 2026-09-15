"""Fabrique l'empreinte d'un mot de passe, a coller dans les secrets.

Usage::

    python -m explorateur.empreinte
    python -m explorateur.empreinte --identifiant marie

Le mot de passe est demande sans echo et n'apparait ni a l'ecran ni dans l'historique du
shell : le passer en argument le laisserait dans `~/.bash_history` et dans la liste des
processus.
"""

from __future__ import annotations

import argparse
import getpass
import sys

from explorateur.auth import empreinte


def main(argv: list[str] | None = None) -> int:
    """Point d'entree."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--identifiant", default="", help="Pour afficher la ligne complete.")
    args = parser.parse_args(argv)
    premier = getpass.getpass("Mot de passe : ")
    if premier != getpass.getpass("Repeter : "):
        print("les deux saisies different", file=sys.stderr)
        return 1
    if not premier:
        print("un mot de passe vide n'est pas accepte", file=sys.stderr)
        return 1
    calcule = empreinte(premier)
    if args.identifiant:
        print(f'{args.identifiant} = "{calcule}"')
    else:
        print(calcule)
    return 0


if __name__ == "__main__":
    sys.exit(main())
