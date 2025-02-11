"""
Streamlit app that displays the definitions to the user
"""
import streamlit as st
from scraper import fetch_page_content, get_catgram, get_definitions

st.title("Dictionaire Français")

# Get query params
query_params = st.query_params
word = query_params.get("mot", "")

# User input field
word = st.text_input("Mot à chercher", value=word, placeholder="Écrivez votre mot ici")

if word:
    soup = fetch_page_content(word)
    if soup:
        catgram_text = get_catgram(soup)
        definitions = get_definitions(soup)

        if definitions:
            st.subheader(f"{word} ({catgram_text})")

            for definition in definitions:
                num_def = definition["number"]
                definition_text = definition["text"]
                examples = definition["examples"]
                synonyms = definition["synonyms"]
                antonyms = definition["antonyms"]

                example_text = "<br>".join([f"<span style='color:blue; font-style:italic;'>- {ex}</span>" for ex in examples])
                synonym_text = f"<br><strong>Synonyms: </strong>{' - '.join(synonyms)}" if synonyms else ""
                antonym_text = f"<br><strong>Antonyms: </strong>{' - '.join(antonyms)}" if antonyms else ""

                st.markdown(
                    f"<span style='font-weight: bold; font-size: 16px;'>{num_def}</span> {definition_text}<br>{example_text}{synonym_text}{antonym_text}",
                    unsafe_allow_html=True
                )
        else:
            st.warning("Aucune définition trouvée !")
    else:
        st.error("Échec de récupération de la page. Veuillez réessayer.")
else:
    st.warning("Veuillez entrer un mot valide.")