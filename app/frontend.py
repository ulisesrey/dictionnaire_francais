import streamlit as st
import requests

st.title("French Dictionary (Powered by FastAPI)")

# Get query parameter from URL (if any)
query_params = st.query_params
word_from_url = query_params.get("word", [""])[0]  # Extract word from URL

# Input field for word search (with auto-filled value from URL if available)
word = st.text_input("Enter a word", value=word_from_url)

# Auto-fetch if word exists in URL (and if the input hasn't changed)
if word_from_url and not word:
    st.experimental_set_query_params(word=word_from_url)
    st.rerun()  # ✅ Trigger rerun to fetch the word's definition based on the URL

# Search button with unique key
if st.button("Search Definition", key="search_button"):
    if word:
        # Call FastAPI backend (Ensure FastAPI is running at localhost:8000)
        api_url = f"http://localhost:8501/api/definition/{word}"  # Ensure FastAPI is on this port
        response = requests.get(api_url)

        if response.status_code == 200:
            try:
                # Try to parse the response as JSON
                data = response.json()

                # Display the data
                st.subheader(f"{data['word']} ({data['category']})")

                for definition in data["definitions"]:
                    st.markdown(f"**{definition['number']}**. {definition['definition']}")
                    for example in definition["examples"]:
                        st.markdown(f"_• {example}_")

            except ValueError:
                # Handle invalid JSON (empty response or non-JSON content)
                st.error(f"Invalid JSON response received from API. Response: {response.text}")
        else:
            # Handle failed request (non-200 status code)
            st.error(f"Failed to fetch definition. HTTP Status Code: {response.status_code}")

    else:
        st.warning("Please enter a valid word.")
