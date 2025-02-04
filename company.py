from TMDB import url, BEARER_TOKEN, make_request

# Produktionsfirma nach Namen suchen
def search_company_by_name(company_name):
    if not company_name.strip():
        print("Kein Firmenname angegeben.")
        return []
    company_url = f"{url}/search/company"
    params = {"query": company_name}
    return make_request(company_url, params).get("results", [])

# Produktionsfirma basierend auf Namen suchen
def get_company_id(company_name):
    company_url = f"{url}/search/company"
    params = {"query": company_name}
    response_data = make_request(company_url, params)
    if response_data:
        companies = response_data.get("results", [])
        if companies:
            return companies[0].get("id")
    return None
