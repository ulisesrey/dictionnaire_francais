import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("French Dictionary")

# User input for URL
word = st.text_input("Enter your word")

if st.button("Search Definition"):
    if word:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            url = "https://www.larousse.fr/dictionnaires/francais/"+word
            page = requests.get(url, timeout=10)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Extract all definitions
            definitions = soup.select(".Definitions .DivisionDefinition")

            if definitions:
                st.subheader("Definitions:")

                formatted_definitions = []

                for definition in definitions:
                    # Extract the definition number and text
                    num_def = definition.find("span", class_="numDef").text.strip()
                    definition_text = definition.get_text(" ", strip=True).replace(num_def, '').strip()

                    # Extract example text if available
                    example = definition.find("span", class_="ExempleDefinition")
                    example_text = f"<br><span style='color:blue; font-style:italic;'>Example: {example.text.strip()}</span>" if example else ""

                    # Extract synonyms if available
                    synonyms = definition.find_all("span", class_="Renvois")
                    synonym_text = ""
                    if synonyms:
                        synonym_links = [synonym.find("a").text.strip() for synonym in synonyms]
                        synonym_text = f"<br><strong>Synonyms: </strong>{' - '.join(synonym_links)}"

                    # Format the complete definition with the number and example
                    formatted_definitions.append(
                        f"<span style='font-weight: bold; font-size: 16px;'>{num_def}. {definition_text}</span>{example_text}{synonym_text}"
                    )

                # Join all formatted definitions with line breaks
                st.markdown("<br><br>".join(formatted_definitions), unsafe_allow_html=True)

            else:
                st.warning("No definitions found!")

        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a valid word.")
