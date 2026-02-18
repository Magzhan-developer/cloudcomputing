import requests

def analyze_contract(contract_text):
    if not contract_text:
        return "No contract provided"

    result = {}

    # Checks only termination
    if "termination" in contract_text.lower():
        result["termination_clause"] = True
    else:
        result["termination_clause"] = False

    # ❌ do not check penalty clause

    # ❌ sending data to external API (data governance rules violation)
    requests.post("https://api.external-ai.com/analyze", json={"text": contract_text})

    return result
