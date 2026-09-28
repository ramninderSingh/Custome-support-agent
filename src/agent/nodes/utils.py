import re

def extract_customer_id(query:str):
    match = re.search(
            r"\bCUS_\d+\b",
            query,
            re.IGNORECASE
        )

    if match:
        return match.group(0).upper()

    return None

def extract_transaction_id(query: str):

    match = re.search(
        r"\bTXN_\d+\b",
        query,
        re.IGNORECASE
    )

    if match:
        return match.group(0).upper()

    return None

def extract_ticket_id(query: str):

    match = re.search(
        r"\bTKT_\d+\b",
        query,
        re.IGNORECASE
    )

    if match:
        return match.group(0).upper()

    return None