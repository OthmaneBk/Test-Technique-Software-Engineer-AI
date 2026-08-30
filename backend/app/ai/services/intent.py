import re

SHOW_ALL_PATTERNS = [
    r"toutes? les données",
    r"affiche.*données",
    r"montre.*données",
    r"liste.*données",
    r"voir toutes",
    r"all data",
    r"show.*data",
    r"display.*data",
    r"list.*data",
    r"see all",
    r"todos? los datos",
    r"mostrar.*datos",
    r"lista.*datos",
    r"ver todos",
]


def is_show_all_intent(question: str) -> bool:
    q = question.lower()
    return any(re.search(p, q) for p in SHOW_ALL_PATTERNS)