import requests
from bs4 import BeautifulSoup

def fetch_page_content(word):
    """Fetches and parses the dictionary page."""
    headers = {"User-Agent": "Mozilla/5.0"}  # TODO: Add random headers
    url = f"https://www.larousse.fr/dictionnaires/francais/{word}"

    try:
        page = requests.get(url, timeout=10)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(e)
        return None

def get_catgram(soup):
    """Extracts the grammatical category of the word."""
    catgram = soup.find("p", class_="CatgramDefinition")
    if catgram:
        for a in catgram.find_all("a"):  
            a.extract()  # Remove links
        return catgram.get_text(strip=True)
    return "Unknown"

def get_synonyms(definition):
    """Extracts synonyms from a definition block."""
    synonyms = definition.find_all("span", class_="Renvois")
    if synonyms:
        return [synonym.find("a").text.strip() for synonym in synonyms]
    return []

def get_definitions(soup):
    """Extracts and formats definitions from the page."""
    definitions = soup.select(".Definitions .DivisionDefinition")
    formatted_definitions = []

    for definition in definitions:
        num_def = definition.find("span", class_="numDef").text.strip()
        
        # Extract and remove examples
        examples = definition.find_all("span", class_="ExempleDefinition")
        example_text = [ex.text.strip() for ex in examples]
        for example in examples:
            example.extract()

        # Extract and clean definition text
        definition_text = definition.get_text(" ", strip=True).replace(num_def, "").strip()
        if definition_text.endswith(":"):
            definition_text = definition_text[:-1]
        
        # Extract synonyms
        synonyms = get_synonyms(definition)

        formatted_definitions.append({
            "number": num_def,
            "text": definition_text,
            "examples": example_text,
            "synonyms": synonyms
        })

    return formatted_definitions
