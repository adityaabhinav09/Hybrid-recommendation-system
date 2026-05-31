import pandas as pd

DATA_PATH = 'data/Music Info.csv'

def data_cleaning(data):


    return (data.drop_duplicates(subset='spotify_id')
            .drop(columns=['genre','spotify_id'])
            .fillna({'tags':'no_tags'})
            .assign(
                name=lambda x:x['name'].str.lower(),
                artist = lambda x:x['artist'].str.lower(),
                tags = lambda x: x['tags'].str.lower()
            ).reset_index(drop=True)
    )

def data_for_content_based_filtering(data):

    return (
        data.drop(columns=['track_id','name','spotify_preview_url'])
    )

def main(data_path):
    
    #data loading
    data = pd.read_csv(data_path)

    #data cleaning
    cleaned_data = data_cleaning(data)

    #save clean data
    cleaned_data.to_csv("data/cleaned_data.csv",index=False)


if __name__ == "__main__":
    main(DATA_PATH)