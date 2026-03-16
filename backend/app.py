from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database.db import songs_collection
from models import MusicRecommender

app = Flask(__name__, 
            static_folder='../frontend/static',
            template_folder='../frontend/templates')
CORS(app)

recommender = MusicRecommender()

# Sample songs data for initialization
SAMPLE_SONGS = [
    # HAPPY SONGS
    {
        "title": "Happy",
        "artist": "Pharrell Williams",
        "genre": "pop",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=ZbZSe6N_BXs",
        "spotify_url": "https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 95
        }
    },
    {
        "title": "Can't Stop the Feeling",
        "artist": "Justin Timberlake",
        "genre": "pop",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=ru0K8uYEZWw",
        "spotify_url": "https://open.spotify.com/track/1WkMMavIMc4JZ8cfMmxHkI",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 92
        }
    },
    {
        "title": "Good Vibrations",
        "artist": "Marky Mark",
        "genre": "pop",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=B7p3G2ZbQVs",
        "spotify_url": "https://open.spotify.com/track/2oXhQ90Wq3R8W0lShP2KHL",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 85
        }
    },
    {
        "title": "Uptown Funk",
        "artist": "Mark Ronson ft. Bruno Mars",
        "genre": "pop",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=OPf0YbXqDm0",
        "spotify_url": "https://open.spotify.com/track/32OlwWuMpZ6b0aN2RZOeMS",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 96
        }
    },
    {
        "title": "Walking on Sunshine",
        "artist": "Katrina & The Waves",
        "genre": "rock",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=iPUmE-tne5U",
        "spotify_url": "https://open.spotify.com/track/05wIrZSwuaVWhcv5FfqeH0",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 87
        }
    },
    {
        "title": "I Got You (I Feel Good)",
        "artist": "James Brown",
        "genre": "funk",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=o4OWJ6JTvss",
        "spotify_url": "https://open.spotify.com/track/5haXbSJqjjM0TCJ5XkfEaC",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 89
        }
    },
    {
        "title": "Shake It Off",
        "artist": "Taylor Swift",
        "genre": "pop",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=nfWlot6h_JM",
        "spotify_url": "https://open.spotify.com/track/5xTtaWoae3wi06K5WfVUUH",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 94
        }
    },
    {
        "title": "Best Day Of My Life",
        "artist": "American Authors",
        "genre": "rock",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=Y66j_BUCBMY",
        "spotify_url": "https://open.spotify.com/track/5Hroj5K7vLpIG4FNCRIjbP",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 88
        }
    },
    {
        "title": "On Top of the World",
        "artist": "Imagine Dragons",
        "genre": "rock",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=w5tWYmIOWGk",
        "spotify_url": "https://open.spotify.com/track/6pSYR9pVjRSLsZo5KdAWyZ",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 86
        }
    },
    {
        "title": "Hey Ya!",
        "artist": "OutKast",
        "genre": "hip-hop",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=PWgvGjAhvIw",
        "spotify_url": "https://open.spotify.com/track/2PpruBYCo4H7WOBJ7Q2EwM",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 93
        }
    },
    {
        "title": "I Wanna Dance with Somebody",
        "artist": "Whitney Houston",
        "genre": "pop",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=eH3giaIzONA",
        "spotify_url": "https://open.spotify.com/track/2tUBqZG2AbRi7Q0BIrVrEj",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 91
        }
    },
    {
        "title": "Don't Worry Be Happy",
        "artist": "Bobby McFerrin",
        "genre": "reggae",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=d-diB65scQU",
        "spotify_url": "https://open.spotify.com/track/4hObp5bmIJ3PP3cKA9K9GY",
        "features": {
            "tempo": "medium",
            "energy": "medium",
            "danceability": "medium",
            "popularity": 84
        }
    },
    {
        "title": "Sugar",
        "artist": "Maroon 5",
        "genre": "pop",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=09R8_2nJtjg",
        "spotify_url": "https://open.spotify.com/track/2iuZJX9X9P0GKaE93xcPjk",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 90
        }
    },
    {
        "title": "Party Rock Anthem",
        "artist": "LMFAO",
        "genre": "electronic",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=KQ6zr6kCPj8",
        "spotify_url": "https://open.spotify.com/track/0IkKz2J93C94Ei4BvDop7P",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 87
        }
    },
    {
        "title": "Dancing Queen",
        "artist": "ABBA",
        "genre": "pop",
        "mood": "happy",
        "youtube_url": "https://www.youtube.com/watch?v=xFrGuyw1V8s",
        "spotify_url": "https://open.spotify.com/track/0GjEhVFGZW8afUYGChu3Rr",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 92
        }
    },

    # SAD SONGS
    {
        "title": "Someone Like You",
        "artist": "Adele",
        "genre": "pop",
        "mood": "sad",
        "youtube_url": "https://www.youtube.com/watch?v=hLQl3WQQoQ0",
        "spotify_url": "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 90
        }
    },
    {
        "title": "Fix You",
        "artist": "Coldplay",
        "genre": "rock",
        "mood": "sad",
        "youtube_url": "https://www.youtube.com/watch?v=k4V3Mo61fJM",
        "spotify_url": "https://open.spotify.com/track/7LVHVU3tWfcxj5aiPFEW4Q",
        "features": {
            "tempo": "slow",
            "energy": "medium",
            "danceability": "low",
            "popularity": 94
        }
    },
    {
        "title": "Hurt",
        "artist": "Johnny Cash",
        "genre": "country",
        "mood": "sad",
        "youtube_url": "https://www.youtube.com/watch?v=8AHCfZTRGiI",
        "spotify_url": "https://open.spotify.com/track/28cnXtME493VX9NOw9cIUh",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 88
        }
    },
    {
        "title": "Everybody Hurts",
        "artist": "R.E.M.",
        "genre": "rock",
        "mood": "sad",
        "youtube_url": "https://www.youtube.com/watch?v=5rOiW_xY-kc",
        "spotify_url": "https://open.spotify.com/track/6PypGyiu0Y2lCDBN1XZEnP",
        "features": {
            "tempo": "slow",
            "energy": "medium",
            "danceability": "low",
            "popularity": 86
        }
    },
    {
        "title": "Tears in Heaven",
        "artist": "Eric Clapton",
        "genre": "rock",
        "mood": "sad",
        "youtube_url": "https://www.youtube.com/watch?v=JxPj3GAYYZ0",
        "spotify_url": "https://open.spotify.com/track/1kgdslQYmeTR4thk9whoRw",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 87
        }
    },
    {
        "title": "The Sound of Silence",
        "artist": "Simon & Garfunkel",
        "genre": "folk",
        "mood": "sad",
        "youtube_url": "https://www.youtube.com/watch?v=NAEppFUWLfc",
        "spotify_url": "https://open.spotify.com/track/3Yf2qG4xF8MzlcaWQ8mF6M",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 89
        }
    },
    {
        "title": "My Immortal",
        "artist": "Evanescence",
        "genre": "rock",
        "mood": "sad",
        "youtube_url": "https://www.youtube.com/watch?v=5anLPw0Efmo",
        "spotify_url": "https://open.spotify.com/track/4UzVcXufOhGUwF56HT7b8M",
        "features": {
            "tempo": "slow",
            "energy": "medium",
            "danceability": "low",
            "popularity": 85
        }
    },
    {
        "title": "Yesterday",
        "artist": "The Beatles",
        "genre": "rock",
        "mood": "sad",
        "youtube_url": "https://www.youtube.com/watch?v=wXTJBr9tt8Q",
        "spotify_url": "https://open.spotify.com/track/3BQHpFgAp4l80e1XslIjNI",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 93
        }
    },
    {
        "title": "Hallelujah",
        "artist": "Jeff Buckley",
        "genre": "rock",
        "mood": "sad",
        "youtube_url": "https://www.youtube.com/watch?v=y8AWFf7EAc4",
        "spotify_url": "https://open.spotify.com/track/3pRaLNL3b8x5uBOcsgvdqM",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 91
        }
    },
    {
        "title": "Say Something",
        "artist": "A Great Big World",
        "genre": "pop",
        "mood": "sad",
        "youtube_url": "https://www.youtube.com/watch?v=RxPZh4AnWyk",
        "spotify_url": "https://open.spotify.com/track/6Vc5wAMmXdKIAM7WUoEb7N",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 84
        }
    },

    # ENERGETIC SONGS
    {
        "title": "Eye of the Tiger",
        "artist": "Survivor",
        "genre": "rock",
        "mood": "energetic",
        "youtube_url": "https://www.youtube.com/watch?v=btPJPFnesV4",
        "spotify_url": "https://open.spotify.com/track/2KH16WveTQWT6KOG9Rg6e2",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "medium",
            "popularity": 88
        }
    },
    {
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "genre": "pop",
        "mood": "energetic",
        "youtube_url": "https://www.youtube.com/watch?v=4NRXx6U8ABQ",
        "spotify_url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 98
        }
    },
    {
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "genre": "rock",
        "mood": "energetic",
        "youtube_url": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ",
        "spotify_url": "https://open.spotify.com/track/3z8h0TU7ReDPLIbEnYhWZb",
        "features": {
            "tempo": "mixed",
            "energy": "high",
            "danceability": "medium",
            "popularity": 99
        }
    },
    {
        "title": "Stronger",
        "artist": "Kanye West",
        "genre": "hip-hop",
        "mood": "energetic",
        "youtube_url": "https://www.youtube.com/watch?v=PsO6ZnUZI0g",
        "spotify_url": "https://open.spotify.com/track/4fzsfWzRhPawzqhX8Qt9F3",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 92
        }
    },
    {
        "title": "Don't Stop Me Now",
        "artist": "Queen",
        "genre": "rock",
        "mood": "energetic",
        "youtube_url": "https://www.youtube.com/watch?v=HgzGwKwLmgM",
        "spotify_url": "https://open.spotify.com/track/5T8EDUDqKcs6OSOwEsfqG7",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 96
        }
    },
    {
        "title": "Lose Yourself",
        "artist": "Eminem",
        "genre": "hip-hop",
        "mood": "energetic",
        "youtube_url": "https://www.youtube.com/watch?v=_Yhyp-_hX2s",
        "spotify_url": "https://open.spotify.com/track/5Z01UMMf7V1o0MzF86s6WJ",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 95
        }
    },
    {
        "title": "Can't Hold Us",
        "artist": "Macklemore & Ryan Lewis",
        "genre": "hip-hop",
        "mood": "energetic",
        "youtube_url": "https://www.youtube.com/watch?v=2zNSgSzhBfM",
        "spotify_url": "https://open.spotify.com/track/3bidbhpOYeV4knp8AIu8Xn",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 89
        }
    },
    {
        "title": "Thunder",
        "artist": "Imagine Dragons",
        "genre": "rock",
        "mood": "energetic",
        "youtube_url": "https://www.youtube.com/watch?v=fKopy74weus",
        "spotify_url": "https://open.spotify.com/track/1zB4vmk8tFRmM9UULNzbLB",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 91
        }
    },
    {
        "title": "Believer",
        "artist": "Imagine Dragons",
        "genre": "rock",
        "mood": "energetic",
        "youtube_url": "https://www.youtube.com/watch?v=7wtfhZwyrcc",
        "spotify_url": "https://open.spotify.com/track/0pqnGHJpmpxLKifKRmU6WP",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 94
        }
    },
    {
        "title": "We Will Rock You",
        "artist": "Queen",
        "genre": "rock",
        "mood": "energetic",
        "youtube_url": "https://www.youtube.com/watch?v=-tJYN-eG1zk",
        "spotify_url": "https://open.spotify.com/track/54flyrjcdnQdco7300avMJ",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "high",
            "popularity": 93
        }
    },

    # RELAXED SONGS
    {
        "title": "Weightless",
        "artist": "Marconi Union",
        "genre": "electronic",
        "mood": "relaxed",
        "youtube_url": "https://www.youtube.com/watch?v=UfcAVejslrU",
        "spotify_url": "https://open.spotify.com/track/6kkwvBWu6onsWw3bbDeSZK",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 75
        }
    },
    {
        "title": "Clair de Lune",
        "artist": "Debussy",
        "genre": "classical",
        "mood": "relaxed",
        "youtube_url": "https://www.youtube.com/watch?v=CvFH_6DNRCY",
        "spotify_url": "https://open.spotify.com/track/5VzeoI43uoPLUuOBeSNo0W",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 82
        }
    },
    {
        "title": "Meditation",
        "artist": "Yiruma",
        "genre": "classical",
        "mood": "relaxed",
        "youtube_url": "https://www.youtube.com/watch?v=4NfE3rkL0m0",
        "spotify_url": "https://open.spotify.com/track/4nrwRfiRSfEl5hO7Lp7RMB",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 78
        }
    },
    {
        "title": "River Flows in You",
        "artist": "Yiruma",
        "genre": "classical",
        "mood": "relaxed",
        "youtube_url": "https://www.youtube.com/watch?v=7maJOI3QMu0",
        "spotify_url": "https://open.spotify.com/track/2UuUSE6r6vi4AQLgCk6R7S",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 86
        }
    },
    {
        "title": "Gymnopédie No.1",
        "artist": "Erik Satie",
        "genre": "classical",
        "mood": "relaxed",
        "youtube_url": "https://www.youtube.com/watch?v=S-Xm7s9eGxU",
        "spotify_url": "https://open.spotify.com/track/0kSHGtJbD3IRTUnrBOnq3q",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 79
        }
    },
    {
        "title": "Spiegel im Spiegel",
        "artist": "Arvo Pärt",
        "genre": "classical",
        "mood": "relaxed",
        "youtube_url": "https://www.youtube.com/watch?v=SyQwR36vUv0",
        "spotify_url": "https://open.spotify.com/track/3qPqX8yCzU63f6C876MlRm",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 74
        }
    },
    {
        "title": "The Blue Danube",
        "artist": "Johann Strauss II",
        "genre": "classical",
        "mood": "relaxed",
        "youtube_url": "https://www.youtube.com/watch?v=_CTYymbbLI4",
        "spotify_url": "https://open.spotify.com/track/4JwP0Y8AzmL0LxY4E0g6yD",
        "features": {
            "tempo": "medium",
            "energy": "medium",
            "danceability": "medium",
            "popularity": 80
        }
    },
    {
        "title": "Bach Cello Suite No.1",
        "artist": "Yo-Yo Ma",
        "genre": "classical",
        "mood": "relaxed",
        "youtube_url": "https://www.youtube.com/watch?v=1prweT95Mo0",
        "spotify_url": "https://open.spotify.com/track/71EIrLjjXtxspM5RKDEmIA",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 83
        }
    },
    {
        "title": "Morning Mood",
        "artist": "Edvard Grieg",
        "genre": "classical",
        "mood": "relaxed",
        "youtube_url": "https://www.youtube.com/watch?v=w7sIIHk7B10",
        "spotify_url": "https://open.spotify.com/track/6I0ioHCefLgYH9IEPE2TrL",
        "features": {
            "tempo": "medium",
            "energy": "medium",
            "danceability": "low",
            "popularity": 77
        }
    },
    {
        "title": "Moonlight Sonata",
        "artist": "Beethoven",
        "genre": "classical",
        "mood": "relaxed",
        "youtube_url": "https://www.youtube.com/watch?v=4Tr0otuiQuU",
        "spotify_url": "https://open.spotify.com/track/7kmF1kcUJkZ1BhxVc3X6rb",
        "features": {
            "tempo": "slow",
            "energy": "low",
            "danceability": "low",
            "popularity": 90
        }
    },

    # ANGRY SONGS
    {
        "title": "Killing in the Name",
        "artist": "Rage Against the Machine",
        "genre": "rock",
        "mood": "angry",
        "youtube_url": "https://www.youtube.com/watch?v=bWXazVhlyxQ",
        "spotify_url": "https://open.spotify.com/track/59WN2psjkt1tyaxjspN8fp",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "medium",
            "popularity": 85
        }
    },
    {
        "title": "Break Stuff",
        "artist": "Limp Bizkit",
        "genre": "metal",
        "mood": "angry",
        "youtube_url": "https://www.youtube.com/watch?v=ZpUYjpKg9KY",
        "spotify_url": "https://open.spotify.com/track/5cZqsjVs6MevCnAkasbEOX",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "medium",
            "popularity": 83
        }
    },
    {
        "title": "Given Up",
        "artist": "Linkin Park",
        "genre": "rock",
        "mood": "angry",
        "youtube_url": "https://www.youtube.com/watch?v=0xyxtzD54rM",
        "spotify_url": "https://open.spotify.com/track/0fagwTd9C8sLZkzVLH73Qt",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "medium",
            "popularity": 82
        }
    },
    {
        "title": "Down with the Sickness",
        "artist": "Disturbed",
        "genre": "metal",
        "mood": "angry",
        "youtube_url": "https://www.youtube.com/watch?v=09LTT0xwdfw",
        "spotify_url": "https://open.spotify.com/track/40rvBMQizxkIqnjPdEWY1v",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "medium",
            "popularity": 84
        }
    },
    {
        "title": "Bodies",
        "artist": "Drowning Pool",
        "genre": "metal",
        "mood": "angry",
        "youtube_url": "https://www.youtube.com/watch?v=04F4xlWSFh0",
        "spotify_url": "https://open.spotify.com/track/7CpbhqKUedOIrcvc94p60Y",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "medium",
            "popularity": 81
        }
    },
    {
        "title": "Psychosocial",
        "artist": "Slipknot",
        "genre": "metal",
        "mood": "angry",
        "youtube_url": "https://www.youtube.com/watch?v=5R6e5VWQeUQ",
        "spotify_url": "https://open.spotify.com/track/3Rc6WNE2m8qQHPzKt9LvXa",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "medium",
            "popularity": 86
        }
    },
    {
        "title": "Du Hast",
        "artist": "Rammstein",
        "genre": "metal",
        "mood": "angry",
        "youtube_url": "https://www.youtube.com/watch?v=W3q8Od5qJio",
        "spotify_url": "https://open.spotify.com/track/5Xdpd6Pp8jT7RWYMjKqsV7",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "medium",
            "popularity": 87
        }
    },
    {
        "title": "Walk",
        "artist": "Pantera",
        "genre": "metal",
        "mood": "angry",
        "youtube_url": "https://www.youtube.com/watch?v=AkFqg5wAuFk",
        "spotify_url": "https://open.spotify.com/track/7fcfNW0XxTWlwVlftzfDOR",
        "features": {
            "tempo": "fast",
            "energy": "high",
            "danceability": "medium",
            "popularity": 85
        }
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Music Recommendation System API is running"})

@app.route('/api/initialize-db', methods=['POST'])
def initialize_db():
    """Initialize database with sample songs"""
    try:
        # Clear existing data
        songs_collection.delete_many({})
        
        # Insert sample songs
        result = songs_collection.insert_many(SAMPLE_SONGS)
        
        return jsonify({
            "success": True,
            "message": f"Database initialized with {len(result.inserted_ids)} songs"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reset-db', methods=['GET'])
def reset_db():
    """Manually reset database"""
    try:
        # Clear existing data
        songs_collection.delete_many({})
        
        # Insert sample songs
        result = songs_collection.insert_many(SAMPLE_SONGS)
        
        return jsonify({
            "success": True,
            "message": f"Database reset with {len(result.inserted_ids)} songs"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/songs', methods=['GET'])
def get_songs():
    """Get all songs"""
    try:
        songs = list(songs_collection.find({}, {'_id': 0}))
        return jsonify({"success": True, "songs": songs})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """Get song recommendations based on mood and genre"""
    try:
        data = request.json
        mood = data.get('mood', '').lower()
        genre = data.get('genre', '').lower()
        
        # Get all songs from database
        songs = list(songs_collection.find({}, {'_id': 0}))
        
        if not songs:
            # If no songs in DB, use sample data
            songs = SAMPLE_SONGS
        
        # Get AI recommendations
        recommendations = recommender.get_recommendations(songs, mood, genre)
        
        return jsonify({
            "success": True,
            "recommendations": recommendations,
            "count": len(recommendations),
            "mood_description": recommender.get_mood_description(mood)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/moods', methods=['GET'])
def get_moods():
    """Get available moods"""
    moods = [
        {"id": "happy", "name": "Happy", "emoji": "😊"},
        {"id": "sad", "name": "Sad", "emoji": "😢"},
        {"id": "energetic", "name": "Energetic", "emoji": "⚡"},
        {"id": "relaxed", "name": "Relaxed", "emoji": "😌"},
        {"id": "angry", "name": "Angry", "emoji": "😠"}
    ]
    return jsonify({"success": True, "moods": moods})

@app.route('/api/genres', methods=['GET'])
def get_genres():
    """Get available genres"""
    genres = [
        {"id": "pop", "name": "Pop"},
        {"id": "rock", "name": "Rock"},
        {"id": "jazz", "name": "Jazz"},
        {"id": "classical", "name": "Classical"},
        {"id": "hip-hop", "name": "Hip Hop"},
        {"id": "electronic", "name": "Electronic"},
        {"id": "acoustic", "name": "Acoustic"},
        {"id": "metal", "name": "Metal"},
        {"id": "rnb", "name": "R&B"},
        {"id": "country", "name": "Country"}
    ]
    return jsonify({"success": True, "genres": genres})

if __name__ == '__main__':
    app.run()