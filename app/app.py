import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("French Dictionary")

st.query_params(page="mypage")

# get query params from URL
query_params = st.query_params
#word = query_params.get("word", "")

# User input for URL
word = st.text_input("Enter your word", value=word)

if st.button("Search Definition"):
    if word:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            url = "https://www.larousse.fr/dictionnaires/francais/"+word
            page = requests.get(url, timeout=10)
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

            if definitions:
                st.subheader(f"{word} ({catgram_text})")

                formatted_definitions = []

                for definition in definitions:
                    # Extract the definition number and text
                    num_def = definition.find("span", class_="numDef").text.strip()

                    # Extract all examples if available
                    examples = definition.find_all("span", class_="ExempleDefinition")
                    example_text = "<br>"
                    
                    if examples:
                        #example_text = "<br><span style='color:blue; font-style:italic;'>Example(s):</span><br>"
                        for i, example in enumerate(examples):
                            i=i+1
                            example_text += f"<span style='color:blue; font-style:italic;'>- {example.text.strip()}</span>  "
                    
                    # Now we can remove them from definition
                    for example in definition.find_all("span", class_="ExempleDefinition"):
                        example.extract()
                    definition_text = definition.get_text(" ", strip=True).replace(num_def, '').strip()
                    # if there is a ":" at the end, remove it
                    if definition_text[-1] == ":":
                        definition_text = definition_text[:-1]
                    

                    # Extract synonyms if available
                    synonyms = definition.find_all("span", class_="Renvois")
                    synonym_text = ""
                    if synonyms:
                        synonym_links = [synonym.find("a").text.strip() for synonym in synonyms]
                        synonym_text = f"<br><strong>Synonyms: </strong>{' - '.join(synonym_links)}"

                    # Format the complete definition with the number, examples, and synonyms
                    formatted_definitions.append(
                        f"<span style='font-weight: bold; font-size: 16px;'>{num_def}</span> {definition_text}{example_text}{synonym_text}"
                    )

                # Join all formatted definitions with line breaks
                st.markdown("<br><br>".join(formatted_definitions), unsafe_allow_html=True)

            else:
                st.warning("No definitions found!")

        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a valid word.")
