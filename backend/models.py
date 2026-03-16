class MusicRecommender:
    def __init__(self):
        # AI Knowledge Base: Mood to features mapping
        self.mood_features = {
            'happy': {
                'tempo': 'fast',
                'energy': 'high',
                'danceability': 'high',
                'valence': 'positive'
            },
            'sad': {
                'tempo': 'slow',
                'energy': 'low',
                'danceability': 'low',
                'valence': 'negative'
            },
            'energetic': {
                'tempo': 'very_fast',
                'energy': 'very_high',
                'danceability': 'high',
                'valence': 'high_energy'
            },
            'relaxed': {
                'tempo': 'slow',
                'energy': 'low',
                'danceability': 'medium',
                'valence': 'calm'
            },
            'angry': {
                'tempo': 'fast',
                'energy': 'high',
                'danceability': 'medium',
                'valence': 'aggressive'
            }
        }
        
        # AI Knowledge Base: Genre to mood compatibility
        self.genre_mood_map = {
            'pop': ['happy', 'energetic'],
            'rock': ['energetic', 'angry'],
            'jazz': ['relaxed', 'sad'],
            'classical': ['relaxed', 'sad'],
            'hip-hop': ['energetic', 'happy'],
            'electronic': ['energetic', 'happy'],
            'acoustic': ['relaxed', 'sad'],
            'metal': ['angry', 'energetic'],
            'rnb': ['relaxed', 'happy'],
            'country': ['happy', 'relaxed']
        }
    
    def get_recommendations(self, songs, mood, genre, limit=10):
        """
        AI rule-based recommendation logic
        """
        if not songs:
            return []
        
        scored_songs = []
        
        for song in songs:
            score = 0
            
            # AI Rule 1: Genre matching (40% weight)
            if song.get('genre', '').lower() == genre.lower():
                score += 40
            
            # AI Rule 2: Mood matching (60% weight)
            song_mood = song.get('mood', '').lower()
            if song_mood == mood:
                score += 60
            elif song_mood in self.genre_mood_map.get(genre.lower(), []):
                score += 30
            
            # AI Rule 3: Feature matching (bonus points)
            features = song.get('features', {})
            mood_feat = self.mood_features.get(mood, {})
            
            if features:
                # Tempo matching
                if features.get('tempo') == mood_feat.get('tempo'):
                    score += 5
                
                # Energy matching
                if features.get('energy') == mood_feat.get('energy'):
                    score += 5
                
                # Popularity bonus
                if features.get('popularity', 0) > 70:
                    score += 5
            
            scored_songs.append((song, score))
        
        # AI Decision: Sort by score and return top recommendations
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [song for song, score in scored_songs[:limit]]
    
    def get_mood_description(self, mood):
        """Get description for each mood"""
        descriptions = {
            'happy': '😊 Upbeat and joyful tunes to lift your spirits',
            'sad': '😢 Melancholic and emotional melodies for reflection',
            'energetic': '⚡ High-energy tracks to get you moving',
            'relaxed': '😌 Calm and soothing sounds for relaxation',
            'angry': '😠 Intense and powerful music to match your energy'
        }
        return descriptions.get(mood, '🎵 Personalized recommendations for you')