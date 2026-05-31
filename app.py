import streamlit as st
from content_based_filtering import recommend
from scipy.sparse import load_npz
import pandas as pd

# Transformed data path

transformed_data_path = "data/transformed_data.npz"

# Cleaned data path

cleaned_data_path = "data/cleaned_data.csv"

# Cleaned Data loading

data = pd.read_csv(cleaned_data_path)

# Transformed Data loading

transformed_data = load_npz(transformed_data_path)

# Text Input
song_name = st.text_input("Enter a song name:")
st.write("You entered:",song_name)

# Fixing the case of input

song_name = song_name.lower()

k= st.selectbox("How many recommendation do you want?",[5,10,15,20], index=1)

# Button

if st.button('Get Recommendations'):
    if (data['name'] == song_name).any():
        st.write('Recommendations for',f"**{song_name}**")
        recommendations = recommend(song_name,data,transformed_data,k)

        # Display Recommendations
        for ind,recommendation in recommendations.iterrows():
            song_name = recommendation['name'].title()
            artist_name = recommendation['artist'].title()

            if ind == 0:
                st.markdown("## Currently Playing")
                st.markdown(f"#### **{song_name}** by **{artist_name}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
            elif ind == 1:
                st.markdown('### next up ')
                st.markdown(f"### {ind}. **{song_name}** by **{artist_name}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
            else:
                st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
    else:
        st.write(f"Sorry, we couldn't find {song_name} in out database. Please try another")
