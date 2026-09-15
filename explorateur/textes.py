"""Tout ce que l'explorateur affiche, en français et en anglais.

**Une seule table pour les deux langues.** Disperser les chaînes dans les pages les fait
diverger : une correction en français ne se voit pas en anglais, et personne ne s'en aperçoit
avant qu'un lecteur externe le signale. Chaque clef porte ici ses deux versions, côte à côte,
et une clef qui n'aurait qu'une version se repère à la lecture.

Le contenu du rappel du projet et du rappel des tâches vient de
`rapport/litterature/contexte-modeles-et-taches.pdf`, la note de contexte du projet. Il n'est
pas réécrit ici : le résumer autrement ferait deux descriptions du même banc.
"""

from __future__ import annotations

from typing import Any


LANGUES = {"fr": "Français", "en": "English"}

T: dict[str, dict[str, str]] = {
    "titre": {
        "fr": "Tribune : tableau de bord des résultats",
        "en": "Tribune: results dashboard",
    },
    "titre_connexion": {
        "fr": "Tribune : explorateur des résultats",
        "en": "Tribune: results explorer",
    },
    "identifiant": {"fr": "Identifiant", "en": "Username"},
    "mot_de_passe": {"fr": "Mot de passe", "en": "Password"},
    "se_connecter": {"fr": "Se connecter", "en": "Sign in"},
    "se_deconnecter": {"fr": "Se déconnecter", "en": "Sign out"},
    "identifiants_errones": {
        "fr": "Identifiant ou mot de passe incorrect.",
        "en": "Incorrect username or password.",
    },
    "connecte": {"fr": "Connecté", "en": "Signed in"},
    "recolte": {"fr": "Récolte", "en": "Harvest"},
    "langue": {"fr": "Langue", "en": "Language"},
    # ------------------------------------------------------------------ couverture
    "modeles_vus": {"fr": "Modèles avec des résultats", "en": "Models with results"},
    "modeles_vus_aide": {
        "fr": "Modèles de la flotte ayant au moins une tâche notée.",
        "en": "Fleet models with at least one scored task.",
    },
    "modeles_complets": {"fr": "Modèles complets", "en": "Complete models"},
    "modeles_complets_aide": {
        "fr": "Modèles ayant fait toutes les tâches disponibles dans cette récolte.",
        "en": "Models that completed every task available in this harvest.",
    },
    "taches_notees": {"fr": "Tâches notées", "en": "Scored tasks"},
    "taches_notees_aide": {
        "fr": "Sur les tâches que le contrat d'invites déclare, socle et québécois réunis.",
        "en": "Out of the tasks the prompt contract declares, base and Quebec combined.",
    },
    "couples_notes": {"fr": "Couples modèle-tâche", "en": "Model-task pairs"},
    "couples_notes_aide": {
        "fr": "Chaque modèle de la flotte fois chaque tâche du banc.",
        "en": "Every fleet model times every benchmark task.",
    },
    "part_du_banc": {"fr": "Part du banc couverte", "en": "Benchmark coverage"},
    "mesures": {"fr": "Mesures individuelles", "en": "Individual measurements"},
    "mesures_aide": {
        "fr": "Une ligne par modèle, tâche et métrique dans la table versionnée.",
        "en": "One row per model, task and metric in the versioned table.",
    },
    "avancement_familles": {"fr": "Avancement par famille", "en": "Progress by family"},
    "avertissement": {"fr": "Avertissement", "en": "Warning"},
    "incomplet_titre": {
        "fr": "la comparaison est incomplète",
        "en": "the comparison is incomplete",
    },
    "socle_absent_titre": {
        "fr": "aucun écart n'est encore mesuré",
        "en": "no gap is measured yet",
    },
    "incomplet": {
        "fr": (
            "{n} modèles de la flotte n'ont aucun résultat ici : "
            "{noms}. Un classement établi sur cette page ne vaut que parmi les modèles présents."
        ),
        "en": (
            "{n} fleet models have no results here: {noms}. "
            "Any ranking on this page holds only among the models shown."
        ),
    },
    "socle_absent": {
        "fr": (
            "Les tâches du socle n'ont pas encore tourné. Rien ici ne dit comment ces "
            "modèles se comportent sur le français général, donc rien ici ne mesure encore "
            "un **écart**, qui est pourtant l'objet de Tribune."
        ),
        "en": (
            "The base tasks have not run yet. Nothing here says how these models behave "
            "on general French, so nothing here measures a **gap** yet, which is what Tribune "
            "is for."
        ),
    },
    # ------------------------------------------------------------------ onglets
    "onglet_projet": {"fr": "Le projet", "en": "The project"},
    "onglet_taches": {"fr": "Les tâches", "en": "The tasks"},
    "onglet_classement": {"fr": "Classement", "en": "Ranking"},
    "onglet_modele": {"fr": "Par modèle", "en": "By model"},
    "onglet_tache": {"fr": "Par tâche", "en": "By task"},
    "onglet_table": {"fr": "Table complète", "en": "Full table"},
    # ------------------------------------------------------------------ tableaux
    "metrique": {"fr": "Métrique", "en": "Metric"},
    "modele": {"fr": "Modèle", "en": "Model"},
    "tache": {"fr": "Tâche", "en": "Task"},
    "famille": {"fr": "Famille", "en": "Family"},
    "moyenne": {"fr": "Moyenne", "en": "Mean"},
    "nature": {"fr": "Nature", "en": "Kind"},
    "valeur": {"fr": "Valeur", "en": "Value"},
    "sans_objet": {"fr": "Sans objet", "en": "Not applicable"},
    "pas_evalue": {"fr": "Pas encore évalué", "en": "Not evaluated yet"},
    "legende_cases_vides": {
        "fr": (
            "« {sans_objet} » : la tâche n'expose pas cette métrique. "
            "« {pas_evalue} » : le couple modèle-tâche n'a pas encore tourné. "
            "Ni l'un ni l'autre n'est un zéro."
        ),
        "en": (
            "“{sans_objet}”: the task does not expose this metric. "
            "“{pas_evalue}”: this model-task pair has not run yet. "
            "Neither is a zero."
        ),
    },
    "moyenne_avertissement": {
        "fr": (
            "La moyenne ne porte que sur les tâches renseignées ; elle ne se compare donc pas "
            "d'une métrique à l'autre."
        ),
        "en": (
            "The mean covers only the tasks with a value, so it does not compare across metrics."
        ),
    },
    "que_mesure_chaque_tache": {
        "fr": "Ce que mesure chaque tâche",
        "en": "What each task measures",
    },
    "telecharger_tableau": {
        "fr": "Télécharger ce tableau (CSV)",
        "en": "Download this table (CSV)",
    },
    "telecharger_selection": {
        "fr": "Télécharger la sélection (CSV)",
        "en": "Download the selection (CSV)",
    },
    "performances": {"fr": "Performances", "en": "Performance"},
    "reperes": {"fr": "Repères du jeu d'items", "en": "Item-set reference points"},
    "effectifs": {"fr": "Effectifs", "en": "Counts"},
    "reperes_avertissement": {
        "fr": (
            "Ces valeurs ne mesurent pas le modèle mais le jeu d'items : plafond humain, "
            "niveau du hasard, part de la classe majoritaire. Ce sont des points de "
            "comparaison, pas des scores."
        ),
        "en": (
            "These values do not measure the model but the item set: human ceiling, chance "
            "level, majority-class rate. They are reference points, not scores."
        ),
    },
    "fiche_modele": {"fr": "Fiche d'un modèle", "en": "Model sheet"},
    "fiche_tache": {"fr": "Fiche d'une tâche", "en": "Task sheet"},
    "table_versionnee": {
        "fr": "C'est exactement le fichier versionné dans `resultats/`. Rien n'est calculé ici.",
        "en": "This is exactly the file versioned in `resultats/`. Nothing is computed here.",
    },
    # ------------------------------------------------------------------ vue d'ensemble
    "onglet_ensemble": {"fr": "Vue d'ensemble", "en": "Overview"},
    "tete_de_classement": {"fr": "En tête", "en": "Leading"},
    "carte_de_chaleur": {
        "fr": "Toute la récolte en une image",
        "en": "The whole harvest at a glance",
    },
    "carte_legende": {
        "fr": (
            "Exactitude par modèle et par tâche. Les modèles sont ordonnés par moyenne, les "
            "tâches dans l'ordre du protocole. Une colonne pâle est une tâche que tout le monde "
            "rate ; une colonne contrastée est une tâche qui sépare."
        ),
        "en": (
            "Accuracy by model and task. Models are ordered by mean, tasks in protocol order. "
            "A pale column is a task everyone fails; a contrasted column is one that separates."
        ),
    },
    "dispersion": {
        "fr": "Chaque modèle, tâche par tâche",
        "en": "Every model, task by task",
    },
    "dispersion_legende": {
        "fr": (
            "Un point par modèle. **Le trait pointillé est le repère du jeu d'items** : hasard, "
            "classe majoritaire ou base de règles, selon la tâche. Un point sous la ligne est "
            "un modèle qui fait moins bien que répondre sans lire. Les tâches sans repère publié "
            "n'en portent pas, plutôt qu'une ligne devinée."
        ),
        "en": (
            "One dot per model. **The dotted line is the item set's reference point**: chance, "
            "majority class or a rules baseline, depending on the task. A dot below the line is "
            "a model doing worse than answering without reading. Tasks with no published "
            "reference carry none, rather than a guessed line."
        ),
    },
    "legende_repere": {"fr": "Repère du jeu d'items", "en": "Item-set reference"},
    "legende_modele": {"fr": "Un modèle", "en": "One model"},
    # ------------------------------------------------------------------ navigation
    "section_resultats": {"fr": "Résultats", "en": "Results"},
    "section_documentation": {"fr": "Documentation", "en": "Documentation"},
    "page": {"fr": "Page", "en": "Page"},
    "telecharger_note": {
        "fr": "Télécharger la note de contexte (PDF)",
        "en": "Download the context note (PDF)",
    },
    "note_en_anglais": {
        "fr": (
            "Les fiches détaillées sont extraites de la note de contexte, rédigée en anglais. "
            "Les titres et résumés ci-dessous sont en français ; le détail reste dans la langue "
            "de la note."
        ),
        "en": "The detailed sheets are extracted from the context note.",
    },
    "donne_au_modele": {"fr": "Donné au modèle", "en": "Given to the model"},
    "verite_attendue": {"fr": "Vérité attendue", "en": "Expected truth"},
    "note": {"fr": "Note", "en": "Note"},
    "corpus": {"fr": "Corpus", "en": "Corpus"},
    "item": {"fr": "Item", "en": "Item"},
    "motif": {"fr": "Motif", "en": "Rationale"},
    "verite_terrain": {"fr": "Vérité terrain", "en": "Ground truth"},
    "evaluation": {"fr": "Évaluation", "en": "Evaluation"},
    "reservation": {"fr": "Réserve", "en": "Reservation"},
    "en_developpement": {"fr": "En développement", "en": "In development"},
    "en_refonte": {"fr": "En refonte", "en": "In rework"},
    "notee": {"fr": "Notée", "en": "Scored"},
    "trier_conseil": {
        "fr": (
            "Cliquer sur l'en-tête d'une colonne trie les modèles sur cette tâche. Un second "
            "clic inverse l'ordre."
        ),
        "en": (
            "Click a column header to sort models on that task. A second click reverses the order."
        ),
    },
    "latex_pour_article": {
        "fr": "Tableau LaTeX pour l'article",
        "en": "LaTeX table for the paper",
    },
    "couverture_et_reserves": {
        "fr": "Couverture et réserves",
        "en": "Coverage and reservations",
    },
    "socle_pas_lance": {
        "fr": "Socle, français général : pas encore lancé, 0 / {total} tâches",
        "en": "Base, general French: not started, 0 / {total} tasks",
    },
    "recolte_vide": {
        "fr": (
            "Cette récolte ne porte aucun score. La notation a-t-elle tourné ? "
            "`python scripts/noter_depuis_predictions.py <récolte>/*` puis "
            "`python scripts/resultats/consolider.py`."
        ),
        "en": (
            "This harvest carries no scores. Has scoring run? "
            "`python scripts/noter_depuis_predictions.py <harvest>/*` then "
            "`python scripts/resultats/consolider.py`."
        ),
    },
    "sous_titre_connexion": {
        "fr": (
            "Résultats du banc Tribune sur le français québécois. "
            "Cohere, Mila et Université Laval."
        ),
        "en": (
            "Results of the Tribune benchmark on Quebec French. Cohere, Mila and Université Laval."
        ),
    },
    "aucune_tache_expose": {
        "fr": "Aucune tâche n'expose cette métrique.",
        "en": "No task exposes this metric.",
    },
}

# ---------------------------------------------------------------- rappel du projet
#
# Traduit de `rapport/litterature/contexte-modeles-et-taches.pdf`, section « Research
# context ». Le texte anglais est celui de la note ; le français en est la traduction.
PROJET: dict[str, list[dict[str, str]]] = {
    "fr": [
        {
            "titre": "Ce que Tribune cherche à mesurer",
            "corps": (
                "Tribune est un partenariat entre Cohere, Mila et l'Université Laval. Le projet "
                "mesure l'écart de performance des grands modèles de langue sur le français "
                "québécois, afin que Cohere sache quoi améliorer dans ses modèles pour sa "
                "clientèle québécoise."
            ),
        },
        {
            "titre": "Trois objectifs, et la raison de chacun",
            "corps": (
                "**Bâtir un banc difficile.** La connaissance du français québécois doit être "
                "nécessaire pour réussir un item : un modèle de pointe ne doit pas pouvoir s'en "
                "tirer par sa seule aisance en français. Une tâche que le français hexagonal "
                "porte à lui seul mesure l'aisance et ne dit rien de l'écart.\n\n"
                "**Mesurer l'écart sur le français québécois.** Ce qu'un modèle perd quand le "
                "français devant lui est celui du Québec plutôt que l'hexagonal sur lequel il a "
                "surtout été entraîné : lexique, registre, et la référence institutionnelle que "
                "seul l'usage local fournit. Aucun chiffre publié ne dit l'ampleur de cet écart.\n\n"
                "**Développer des tâches qui restent pertinentes.** Les comptes rendus continuent "
                "de paraître, donc les items peuvent toujours venir de séances postérieures à la "
                "coupure d'entraînement d'un modèle. C'est ce qui empêche le banc d'être saturé "
                "ou contaminé un an plus tard."
            ),
        },
        {
            "titre": "Pourquoi les comptes rendus parlementaires",
            "corps": (
                "Ils sont le matériau, pas l'objet d'étude. Ils sont publics et existent en "
                "volume, ce qui manque autrement au français québécois ; l'institution continue "
                "de les publier, donc des items postérieurs à une coupure d'entraînement restent "
                "disponibles ; et ils portent des faits institutionnels durs, votes, appartenance "
                "partisane, rôles, contre lesquels une affirmation se vérifie."
            ),
        },
        {
            "titre": "Pourquoi d'autres assemblées francophones",
            "corps": (
                "La France, la Belgique, la Suisse, le Luxembourg et les institutions européennes "
                "sont un témoin, pas un sujet d'intérêt : sans cette base, un score faible sur le "
                "français québécois ne se distingue pas d'une tâche difficile dans n'importe quel "
                "français."
            ),
        },
        {
            "titre": "Ce qui doit en sortir",
            "corps": (
                "Un modèle qui sert une clientèle québécoise est lu et on lui répond en français "
                "québécois : québécismes, registre, terminologie des institutions d'ici. Les "
                "variétés moins représentées sont moins bien servies que la variété dominante et "
                "aplaties vers une moyenne générique, si bien qu'une réponse qui pourrait venir de "
                "n'importe où dans la francophonie passe pour correcte alors qu'elle n'est que "
                "générique.\n\n"
                "Ce que le banc doit rendre est donc un **diagnostic** plutôt qu'un classement : "
                "quels échecs sont lexicaux, lesquels tiennent à une connaissance "
                "institutionnelle absente, lesquels viennent de l'aplatissement de la variété, et "
                "où dans le gradient un modèle commence à perdre. C'est cela qui dit quoi "
                "améliorer."
            ),
        },
        {
            "titre": "Pourquoi un gradient plutôt qu'un test unique",
            "corps": (
                "Une tâche unique, réussie ou ratée, dit qu'un modèle a échoué et jamais où. La "
                "difficulté est donc disposée en paliers, de sorte qu'un résultat se lise comme "
                "un niveau atteint."
            ),
        },
    ],
    "en": [
        {
            "titre": "What Tribune sets out to measure",
            "corps": (
                "Tribune is a partnership of Cohere, Mila and Université Laval. It sets out to "
                "measure the performance gap of large language models on Quebec French, so that "
                "Cohere knows what to improve in its models for its Quebec clients."
            ),
        },
        {
            "titre": "Three aims, and the reason for each",
            "corps": (
                "**Build a difficult benchmark.** Knowledge of Quebec French has to be necessary "
                "to pass an item, so a frontier model cannot clear it on general fluency in "
                "French. A task that hexagonal French carries by itself measures fluency and says "
                "nothing about the gap.\n\n"
                "**Measure the gap on Quebec French.** What a model loses when the French in "
                "front of it is Quebec's rather than the hexagonal French it was mostly trained "
                "on: lexicon, register, and the institutional reference only local usage "
                "supplies. No published number says how large that gap is.\n\n"
                "**Develop tasks that stay relevant over time.** The records keep being "
                "published, so items can always come from sittings later than a model's training "
                "cutoff, which is what keeps the benchmark from being saturated or contaminated "
                "a year on."
            ),
        },
        {
            "titre": "Why parliamentary records",
            "corps": (
                "They are the material, not the object of study. They are public and exist in "
                "volume, which Quebec French otherwise lacks; the institution keeps publishing "
                "them, so items later than a training cutoff stay available; and they carry hard "
                "institutional facts, votes, party membership, roles, that a claim can be checked "
                "against."
            ),
        },
        {
            "titre": "Why other francophone assemblies are in the corpus",
            "corps": (
                "France, Belgium, Switzerland, Luxembourg and the European institutions are a "
                "control, not a subject of interest: without that baseline, a low score on Quebec "
                "French cannot be told from a task that is hard in any French."
            ),
        },
        {
            "titre": "What comes out of it",
            "corps": (
                "A model serving a Quebec client is read and answered in Quebec French: "
                "quebecismes, register, the terminology of the institutions here. Less "
                "represented varieties are served worse than the dominant one and flattened "
                "towards a generic average, so an answer that could come from anywhere "
                "francophone passes as correct when it is merely generic.\n\n"
                "What the benchmark is meant to yield is therefore a **diagnosis** rather than a "
                "ranking: which failures are lexical, which are missing institutional knowledge, "
                "which come from the variety being flattened, and where in the gradient a model "
                "starts to lose. That is what says what to improve."
            ),
        },
        {
            "titre": "Why a gradient rather than one test",
            "corps": (
                "A single pass-or-fail task says that a model failed and never where. Difficulty "
                "is laid out as bands, so a result reads as a level reached."
            ),
        },
    ],
}

# Les paliers du banc, tels que la note de contexte les nomme.
PALIERS: list[dict[str, str]] = [
    {
        "code": "Niveau 0",
        "fr": "Compétences de base sur le texte parlementaire",
        "en": "Base competences on parliamentary text",
    },
    {
        "code": "Niveau 1",
        "fr": "Connaissance du français québécois",
        "en": "Quebec French knowledge",
    },
    {"code": "Niveau 2", "fr": "Positionnement politique", "en": "Political positioning"},
    {
        "code": "Niveau 3",
        "fr": "Reconstruction et continuation d'un échange",
        "en": "Exchange reconstruction and continuation",
    },
    {
        "code": "Niveau 4",
        "fr": "Génération argumentative ancrée",
        "en": "Grounded argumentative generation",
    },
    {
        "code": "Transversal",
        "fr": "Contraste français-anglais transversal",
        "en": "Cross-cutting French-English contrast",
    },
]

# ---------------------------------------------------------------- rappel des tâches
#
# Reprise de la table « task by task » de la note de contexte. `metrique` est la mesure
# principale, `verite` la source de la vérité terrain.
TACHES: list[dict[str, Any]] = [
    {
        "code": "1a",
        "niveau": 1,
        "fr": "Repérer le québécisme d'un échange, puis le définir",
        "en": "Find the Quebecism in an exchange, then define it",
        "format_fr": "Deux tours : terme ouvert, puis QCM",
        "format_en": "Two turns: open term, then MCQ",
        "metrique": "Exactitude du repérage",
        "metrique_en": "Detection accuracy",
        "verite": "QFrCoRT et OQLF",
        "verite_en": "QFrCoRT and OQLF",
    },
    {
        "code": "1b",
        "niveau": 1,
        "fr": "Donner le sens d'un terme de procédure parlementaire",
        "en": "Give the meaning of a parliamentary procedure term",
        "format_fr": "QCM, 5 choix plus abstention",
        "format_en": "MCQ, 5 plus abstention",
        "metrique": "Exactitude",
        "metrique_en": "Accuracy",
        "verite": "Encyclopédie du parlementarisme québécois",
        "verite_en": "Encyclopédie du parlementarisme québécois",
    },
    {
        "code": "1c",
        "niveau": 1,
        "fr": "Donner l'expansion officielle d'un sigle",
        "en": "Give the official expansion of an acronym",
        "format_fr": "Génération",
        "format_en": "Generation",
        "metrique": "Exactitude",
        "metrique_en": "Accuracy",
        "verite": "Liste de sigles versionnée",
        "verite_en": "Versioned acronym list",
    },
    {
        "code": "1d",
        "niveau": 1,
        "fr": "Donner le mot qu'un locuteur québécois a réellement employé",
        "en": "Give the word a Quebec speaker actually used",
        "format_fr": "QCM, 5 choix plus abstention",
        "format_en": "MCQ, 5 plus abstention",
        "metrique": "Exactitude",
        "metrique_en": "Accuracy",
        "verite": "Auto-supervisé",
        "verite_en": "Self-supervised",
    },
    {
        "code": "1e",
        "niveau": 1,
        "fr": "Juger si une phrase est du français québécois acceptable",
        "en": "Judge whether a sentence is acceptable Quebec French",
        "format_fr": "Jugement binaire",
        "format_en": "Binary judgment",
        "metrique": "F1 macro",
        "metrique_en": "Macro-F1",
        "verite": "QFrCoLA",
        "verite_en": "QFrCoLA",
    },
    {
        "code": "1f",
        "niveau": 1,
        "fr": "Préférer la phrase grammaticale d'une paire minimale",
        "en": "Prefer the grammatical sentence of a minimal pair",
        "format_fr": "Choix de paire",
        "format_en": "Pair choice",
        "metrique": "Exactitude",
        "metrique_en": "Accuracy",
        "verite": "QFrBLiMP",
        "verite_en": "QFrBLiMP",
    },
    {
        "code": "1h",
        "niveau": 1,
        "fr": "Donner le sens d'une expression québécoise, hors contexte",
        "en": "Give the meaning of a Quebec expression, out of context",
        "format_fr": "QCM, 5 choix plus abstention",
        "format_en": "MCQ, 5 plus abstention",
        "metrique": "Exactitude",
        "metrique_en": "Accuracy",
        "verite": "QFrCoRE",
        "verite_en": "QFrCoRE",
    },
    {
        "code": "1i",
        "niveau": 1,
        "fr": "Donner le sens d'un terme québécois, hors contexte",
        "en": "Give the meaning of a Quebec term, out of context",
        "format_fr": "QCM, 5 choix plus abstention",
        "format_en": "MCQ, 5 plus abstention",
        "metrique": "Exactitude",
        "metrique_en": "Accuracy",
        "verite": "QFrCoRT",
        "verite_en": "QFrCoRT",
    },
    {
        "code": "1j",
        "niveau": 1,
        "fr": "Distinguer la phrase humaine de la phrase machine",
        "en": "Tell the human sentence from the machine sentence",
        "format_fr": "Choix de paire",
        "format_en": "Pair choice",
        "metrique": "Exactitude",
        "metrique_en": "Accuracy",
        "verite": "Connue par construction",
        "verite_en": "Known by construction",
    },
    {
        "code": "2a",
        "niveau": 2,
        "fr": "Dire si le locuteur est du gouvernement ou de l'opposition",
        "en": "Say whether the speaker is government or opposition",
        "format_fr": "Classification binaire",
        "format_en": "Binary classification",
        "metrique": "F1 macro",
        "metrique_en": "Macro-F1",
        "verite": "Registre des votes de l'Assemblée",
        "verite_en": "Assembly voting record",
    },
    {
        "code": "2b",
        "niveau": 2,
        "fr": "Dire quel parti a déposé l'intervention",
        "en": "Say which party deposited the intervention",
        "format_fr": "QCM sur les partis siégeant",
        "format_en": "MCQ over sitting parties",
        "metrique": "F1 macro",
        "metrique_en": "Macro-F1",
        "verite": "Registre des partis de l'Assemblée",
        "verite_en": "Assembly party register",
    },
]


def t(clef: str, langue: str) -> str:
    """Rend une chaîne dans la langue demandée, ou la clef si elle manque.

    Rendre la clef plutôt qu'une chaîne vide fait voir le trou à l'écran : une traduction
    oubliee se repère alors sans relire le module.
    """
    return T.get(clef, {}).get(langue, clef)
