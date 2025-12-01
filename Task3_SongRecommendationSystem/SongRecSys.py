import pandas as pd
import numpy as np
from collections import defaultdict

# diverse music database with real variety
songs_data = {
    'song_id': list(range(1, 31)),
    'title': [
        # Bollywood
        'Apna Bana Le', 'Kesariya', 'Chaleya', 'Tum Hi Ho', 'Dil Diyan Gallan',
        'Zinda', 'Malang', 'Param Sundari', 'Nadiyon Paar', 'Jugnu',
        # English
        'Blinding Lights', 'Levitating', 'Eye of the Tiger', 'Lose Yourself',
        'Someone Like You', 'Happier', 'Till I Collapse', 'Unstoppable',
        # Marathi
        'Gulabachi Kali', 'Kombdi Palali', 'Apsara Aali', 'Zingaat',
        # South Indian
        'Oo Antava', 'Rowdy Baby', 'Arabic Kuthu', 'Kaavaalaa',
        'Vaseegara', 'Vaathi Coming', 'Soul of Doctor', 'Jimikki Kammal'
    ],
    'artist': [
        'Arijit Singh', 'Arijit Singh', 'Arijit Singh', 'Arijit Singh', 'Atif Aslam',
        'Bhaag Milkha Bhaag', 'Ved Sharma', 'Shaan', 'Sachin-Jigar', 'Badshah',
        'The Weeknd', 'Dua Lipa', 'Survivor', 'Eminem',
        'Adele', 'Marshmello', 'Eminem', 'Sia',
        'Ajay Gogavale', 'Ajay-Atul', 'Ajay-Atul', 'Ajay-Atul',
        'Indravathi Chauhan', 'Dhanush', 'Anirudh', 'Shilpa Rao',
        'Bombay Jayashri', 'Anirudh', 'Anirudh', 'Vineeth Sreenivasan'
    ],
    'language': [
        'Hindi', 'Hindi', 'Hindi', 'Hindi', 'Hindi',
        'Hindi', 'Hindi', 'Hindi', 'Hindi', 'Hindi',
        'English', 'English', 'English', 'English',
        'English', 'English', 'English', 'English',
        'Marathi', 'Marathi', 'Marathi', 'Marathi',
        'Telugu', 'Tamil', 'Tamil', 'Tamil',
        'Tamil', 'Tamil', 'Tamil', 'Malayalam'
    ],
    'mood': [
        'Romantic', 'Romantic', 'Romantic', 'Sad', 'Romantic',
        'Motivating', 'Party', 'Party', 'Party', 'Party',
        'Party', 'Party', 'Gym', 'Motivating',
        'Sad', 'Happy', 'Gym', 'Motivating',
        'Romantic', 'Party', 'Party', 'Party',
        'Party', 'Party', 'Party', 'Party',
        'Romantic', 'Gym', 'Happy', 'Party'
    ],
    'genre': [
        'Pop', 'Pop', 'Pop', 'Ballad', 'Pop',
        'Rock', 'EDM', 'Pop', 'Remix', 'Hip-Hop',
        'Pop', 'Pop', 'Rock', 'Hip-Hop',
        'Ballad', 'Pop', 'Hip-Hop', 'Pop',
        'Folk', 'Folk', 'Folk', 'Folk',
        'Item', 'Dance', 'Kuthu', 'Melody',
        'Classical', 'Dance', 'Melody', 'Folk'
    ]
}

# user listening history with ratings
user_ratings = {
    'user_id': [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 
                4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5],
    'song_id': [1, 2, 4, 11, 15, 26, 3, 7, 8, 10, 12, 22, 13, 14, 17, 23, 24, 28,
                6, 13, 14, 17, 18, 19, 20, 21, 22, 24, 30],
    'rating': [5, 5, 4, 5, 3, 4, 5, 5, 4, 5, 4, 5, 5, 5, 5, 4, 5, 4,
               5, 5, 4, 5, 5, 5, 5, 5, 4, 5, 4]
}

songs_df = pd.DataFrame(songs_data)
ratings_df = pd.DataFrame(user_ratings)

def get_user_listening_history(user_id):
    """Get songs that user has already listened to"""
    user_songs = ratings_df[ratings_df['user_id'] == user_id]
    history = user_songs.merge(songs_df, on='song_id')
    return history

def content_based_recommendations(user_id, top_n=5):
    """Recommend songs similar to what user has liked"""
    user_history = get_user_listening_history(user_id)
    
    # get songs user rated highly (4 or 5 stars)
    liked_songs = user_history[user_history['rating'] >= 4]
    
    if len(liked_songs) == 0:
        return []
    
    # find songs with similar attributes
    liked_moods = liked_songs['mood'].values
    liked_languages = liked_songs['language'].values
    liked_genres = liked_songs['genre'].values
    
    # get songs user hasn't listened to yet
    listened_song_ids = user_history['song_id'].values
    unlistened_songs = songs_df[~songs_df['song_id'].isin(listened_song_ids)]
    
    recommendations = []
    
    for _, song in unlistened_songs.iterrows():
        score = 0
        reasons = []
        
        # score based on matching attributes
        if song['mood'] in liked_moods:
            score += 3
            reasons.append(f"{song['mood']} vibe")
        
        if song['language'] in liked_languages:
            score += 2
            reasons.append(f"{song['language']} song")
        
        if song['genre'] in liked_genres:
            score += 1
            reasons.append(f"{song['genre']} genre")
        
        if score > 0:
            recommendations.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'artist': song['artist'],
                'language': song['language'],
                'mood': song['mood'],
                'score': score,
                'reason': ', '.join(reasons)
            })
    
    # sort by score and return top N
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations[:top_n]

def collaborative_filtering_recommendations(user_id, top_n=5):
    """Recommend songs that similar users enjoyed"""
    
    # create user-song rating matrix
    rating_matrix = ratings_df.pivot_table(
        index='user_id', 
        columns='song_id', 
        values='rating'
    ).fillna(0)
    
    if user_id not in rating_matrix.index:
        return []
    
    # calculate similarity between users
    user_similarities = {}
    current_user_ratings = rating_matrix.loc[user_id]
    
    for other_user in rating_matrix.index:
        if other_user != user_id:
            other_ratings = rating_matrix.loc[other_user]
            
            # find common rated songs
            common_songs = (current_user_ratings > 0) & (other_ratings > 0)
            
            if common_songs.sum() > 0:
                # calculate similarity using correlation
                similarity = np.corrcoef(
                    current_user_ratings[common_songs],
                    other_ratings[common_songs]
                )[0, 1]
                
                if not np.isnan(similarity):
                    user_similarities[other_user] = similarity
    
    # find songs from similar users
    listened_song_ids = get_user_listening_history(user_id)['song_id'].values
    recommendations = defaultdict(float)
    
    for similar_user, similarity in sorted(user_similarities.items(), 
                                          key=lambda x: x[1], 
                                          reverse=True)[:3]:
        similar_user_songs = ratings_df[
            (ratings_df['user_id'] == similar_user) & 
            (ratings_df['rating'] >= 4) &
            (~ratings_df['song_id'].isin(listened_song_ids))
        ]
        
        for _, row in similar_user_songs.iterrows():
            recommendations[row['song_id']] += similarity * row['rating']
    
    # convert to list with song details
    rec_list = []
    for song_id, score in recommendations.items():
        song = songs_df[songs_df['song_id'] == song_id].iloc[0]
        rec_list.append({
            'song_id': song_id,
            'title': song['title'],
            'artist': song['artist'],
            'language': song['language'],
            'mood': song['mood'],
            'score': score,
            'reason': 'listeners like you loved this'
        })
    
    rec_list.sort(key=lambda x: x['score'], reverse=True)
    return rec_list[:top_n]

def display_recommendations(user_id):
    """Show personalized recommendations for user"""
    print(f"\n{'='*70}")
    print(f"🎵 MUSIC RECOMMENDATIONS FOR USER {user_id}")
    print(f"{'='*70}\n")
    
    # show listening history
    history = get_user_listening_history(user_id)
    print("Your Listening History:")
    print("-" * 70)
    for _, song in history.iterrows():
        stars = "⭐" * song['rating']
        print(f"{song['title']} - {song['artist']}")
        print(f"   [{song['language']}] [{song['mood']}] {stars}\n")
    
    # content-based recommendations
    print("\n💚 SONGS YOU MIGHT LOVE (Based on Your Taste):")
    print("-" * 70)
    content_recs = content_based_recommendations(user_id, top_n=5)
    
    if content_recs:
        for i, rec in enumerate(content_recs, 1):
            print(f"{i}. {rec['title']} - {rec['artist']}")
            print(f"   [{rec['language']}] [{rec['mood']}]")
            print(f"   Why: {rec['reason']}\n")
    else:
        print("Not enough data yet. Keep listening!\n")
    
    # collaborative filtering recommendations
    print("\n🔥 TRENDING WITH LISTENERS LIKE YOU:")
    print("-" * 70)
    collab_recs = collaborative_filtering_recommendations(user_id, top_n=3)
    
    if collab_recs:
        for i, rec in enumerate(collab_recs, 1):
            print(f"{i}. {rec['title']} - {rec['artist']}")
            print(f"   [{rec['language']}] [{rec['mood']}]")
            print(f"   Why: {rec['reason']}\n")
    else:
        print("Not enough similar listeners yet!\n")

def show_songs_by_filter():
    """Browse songs by mood or language"""
    print("\n" + "="*70)
    print("BROWSE SONGS")
    print("="*70)
    print("\n1. By Mood")
    print("2. By Language")
    print("3. Show All Songs")
    
    choice = input("\nEnter choice (1-3): ")
    
    if choice == '1':
        moods = songs_df['mood'].unique()
        print("\nAvailable Moods:", ", ".join(moods))
        mood = input("Enter mood: ").capitalize()
        filtered = songs_df[songs_df['mood'] == mood]
    elif choice == '2':
        languages = songs_df['language'].unique()
        print("\nAvailable Languages:", ", ".join(languages))
        lang = input("Enter language: ").capitalize()
        filtered = songs_df[songs_df['language'] == lang]
    else:
        filtered = songs_df
    
    print("\n" + "-"*70)
    for _, song in filtered.iterrows():
        print(f"ID {song['song_id']}: {song['title']} - {song['artist']}")
        print(f"   [{song['language']}] [{song['mood']}] [{song['genre']}]\n")

def add_user_rating(user_id, song_id, rating):
    """Let user rate a song"""
    global ratings_df
    
    # check if song exists
    if song_id not in songs_df['song_id'].values:
        print("❌ Invalid song ID!")
        return
    
    new_rating = pd.DataFrame({
        'user_id': [user_id],
        'song_id': [song_id],
        'rating': [rating]
    })
    ratings_df = pd.concat([ratings_df, new_rating], ignore_index=True)
    
    song = songs_df[songs_df['song_id'] == song_id].iloc[0]
    print(f"✓ Rated '{song['title']}' with {rating} stars!")

# main program
def main():
    print("🎵 WELCOME TO MUSIC RECOMMENDER 🎵")
    print("Discover Bollywood, English, Marathi & South Indian songs!")
    
    while True:
        print("\n" + "="*70)
        print("\nMENU:")
        print("1. Get Recommendations")
        print("2. Browse Songs")
        print("3. Rate a Song")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == '4':
            print("\nThanks for using Music Recommender! 🎧")
            break
        
        elif choice == '1':
            user_id = input("Enter your User ID (1-5): ")
            try:
                user_id = int(user_id)
                if 1 <= user_id <= 5:
                    display_recommendations(user_id)
                else:
                    print("Please enter a valid User ID (1-5)")
            except ValueError:
                print("Invalid input!")
        
        elif choice == '2':
            show_songs_by_filter()
        
        elif choice == '3':
            try:
                user_id = int(input("Your User ID (1-5): "))
                song_id = int(input("Song ID: "))
                rating = int(input("Rate it (1-5 stars): "))
                
                if 1 <= user_id <= 5 and 1 <= rating <= 5:
                    add_user_rating(user_id, song_id, rating)
                else:
                    print("Invalid input!")
            except ValueError:
                print("Invalid input!")
        
        else:
            print("Invalid choice!")

if __name__ == '__main__':
    main()

# Made this using collaborative filtering and content-based filtering techniques