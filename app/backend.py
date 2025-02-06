from fastaipi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()
@app.get("/api/definition/{word}")
async def get_definition(word: str):
    
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.larousse.fr/dictionnaires/francais/{word}"
    page = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get Catgram
    catgram = soup.find("p", class_="CatgramDefinition")
    if catgram:
        # Remove <a> tags inside the CatgramDefinition
        for a in catgram.find_all("a"):
            a.extract()

        catgram_text = catgram.get_text(strip=True)
    else:
        catgram_text = "Unknown"

    # Extract all definitions
    definitions = soup.select(".Definitions .DivisionDefinition")
    result = []

    for definition in definitions:
        # Extract the definition number and text
        num_def = definition.find("span", class_="numDef").text.strip()

        # Extract all examples if available
        examples = definition.find_all("span", class_="ExempleDefinition")
        example_text = [ex.text.strip() for ex in examples]
        

        # Now we can remove them from definition
        for example in definition.find_all("span", class_="ExempleDefinition"):
            example.extract()
        definition_text = definition.get_text(" ", strip=True).replace(num_def, '').strip()
        
        # if there is a ":" at the end, remove it
        if definition_text[-1] == ":":
            definition_text = definition_text[:-1]
        
        result.append({"number": num_def, "definition": definition_text, "examples": example_text})
        
        if not result:
            return {"word": word, "category": "", "definitions": ["No definitions found."]}

        return {"word": word, "catgram": catgram_text, "definitions": result}

    #     # Extract synonyms if available
    #     synonyms = definition.find_all("span", class_="Renvois")
    #     synonym_text = ""
    #     if synonyms:
    #         synonym_links = [synonym.find("a").text.strip() for synonym in synonyms]
    #         synonym_text = f"<br><strong>Synonyms: </strong>{' - '.join(synonym_links)}"

    #     # Format the complete definition with the number, examples, and synonyms
    #     formatted_definitions.append(
    #         f"<span style='font-weight: bold; font-size: 16px;'>{num_def}</span> {definition_text}{example_text}{synonym_text}"
    #     )

    # # Join all formatted definitions with line breaks
    # st.markdown("<br><br>".join(formatted_definitions), unsafe_allow_html=True)

