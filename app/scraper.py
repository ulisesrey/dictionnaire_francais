"""Responsible for fetching and parsing definitions from the website."""
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

def get_related_words(definition):
    """Extracts synonyms and antonyms from a definition block."""
    synonyms, antonyms = [], []
    
    for libelle in definition.find_all("p", class_="LibelleSynonyme"):
        related_type = libelle.get_text(strip=True).lower()  # "synonymes :" or "contraires :"
        related_block = libelle.find_next_sibling("p", class_="Synonymes")

        if related_block:
            words = []
            # Extract words inside <a> and outside <a>
            for elem in related_block.find_all(["a", "span"], recursive=True):
                words.append(elem.get_text(strip=True))
            
            full_text = related_block.get_text(separator=" ", strip=True)  # Get full line of synonyms/antonyms
            all_words = full_text.split(" - ")  # Split by " - " to separate words correctly
            
            if "synonyme" in related_type:
                synonyms.extend(all_words)
            elif "contraire" in related_type:
                antonyms.extend(all_words)

    return synonyms, antonyms

def get_clean_definition_text(definition):
    """Extracts only the definition text, ignoring examples, synonyms, and antonyms."""
    
    num_def = definition.find("span", class_="numDef")
    if num_def:
        num_def.extract()  # Remove the number tag

    # The first text node after removing numDef is the real definition
    # TODO: Improve this logic to handle more complex cases, see https://github.com/ulisesrey/dictionnaire_francais/issues/12
    definition_text = definition.get_text(" ", strip=True).split(":")[0]  # Stop at ":" to avoid examples
    
    return definition_text


def get_definitions(soup):
    """Extracts and formats definitions from the page."""
    # TODO: Working on this line
    definitions = soup.find_all("div", class_=["Zone-Entree1 header-article", "Zone-Entree header-article"])
    formatted_definitions = []

    for definition in definitions:
        num_def = definition.find("span", class_="numDef").text.strip()
        
        # Extract and remove examples
        examples = definition.find_all("span", class_="ExempleDefinition")
        example_text = [ex.text.strip() for ex in examples]
        for example in examples:
            example.extract()

        # Extract and clean definition text
        definition_text = get_clean_definition_text(definition)
        
        # Extract synonyms and antonyms
        synonyms, antonyms = get_related_words(definition)

        formatted_definitions.append({
            "number": num_def,
            "text": definition_text,
            "examples": example_text,
            "synonyms": synonyms,
            "antonyms": antonyms
        })

    return formatted_definitions