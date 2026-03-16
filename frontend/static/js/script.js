// API Base URL - changed for deployment
const API_BASE_URL = '/api';

// Load moods and genres on page load
document.addEventListener('DOMContentLoaded', function() {
    loadMoods();
    loadGenres();
    
    // Initialize database with sample songs
    initializeDatabase();
});

// Load moods from API
async function loadMoods() {
    try {
        const response = await fetch(`${API_BASE_URL}/moods`);
        const data = await response.json();
        
        if (data.success) {
            const moodSelect = document.getElementById('mood');
            data.moods.forEach(mood => {
                const option = document.createElement('option');
                option.value = mood.id;
                option.textContent = `${mood.emoji} ${mood.name}`;
                moodSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading moods:', error);
        showError('Failed to load moods');
    }
}

// Load genres from API
async function loadGenres() {
    try {
        const response = await fetch(`${API_BASE_URL}/genres`);
        const data = await response.json();
        
        if (data.success) {
            const genreSelect = document.getElementById('genre');
            data.genres.forEach(genre => {
                const option = document.createElement('option');
                option.value = genre.id;
                option.textContent = genre.name;
                genreSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading genres:', error);
        showError('Failed to load genres');
    }
}

// Initialize database with sample songs
async function initializeDatabase() {
    try {
        const response = await fetch(`${API_BASE_URL}/initialize-db`, {
            method: 'POST'
        });
        const data = await response.json();
        console.log('Database initialized:', data);
    } catch (error) {
        console.error('Error initializing database:', error);
    }
}

// Handle form submission
document.getElementById('musicForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const mood = document.getElementById('mood').value;
    const genre = document.getElementById('genre').value;
    
    if (!mood || !genre) {
        showError('Please select both mood and genre');
        return;
    }
    
    // Show loading state
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<div class="loading-spinner"></div> AI is analyzing your mood...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mood, genre })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayRecommendations(data);
        } else {
            showError(data.error || 'Failed to get recommendations');
        }
    } catch (error) {
        console.error('Error getting recommendations:', error);
        showError('Failed to connect to the server');
    } finally {
        // Restore button state
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
});

// Display recommendations
function displayRecommendations(data) {
    const resultsSection = document.getElementById('results');
    const moodDescription = document.getElementById('moodDescription');
    const recommendationsList = document.getElementById('recommendationsList');
    
    // Set mood description
    moodDescription.textContent = data.mood_description || 
        'Here are your AI-powered recommendations';
    
    // Clear previous results
    recommendationsList.innerHTML = '';
    
    if (data.recommendations && data.recommendations.length > 0) {
        data.recommendations.forEach(song => {
            const songCard = createSongCard(song);
            recommendationsList.appendChild(songCard);
        });
    } else {
        recommendationsList.innerHTML = '<p class="no-results">No songs found matching your criteria. Try different selections!</p>';
    }
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Create song card element with clickable links and fallback search
function createSongCard(song) {
    const card = document.createElement('div');
    card.className = 'song-card';
    
    const features = song.features || {};
    
    // Create search URL as fallback
    const searchQuery = encodeURIComponent(`${song.title} ${song.artist} song`);
    const youtubeSearchUrl = `https://www.youtube.com/results?search_query=${searchQuery}`;
    const spotifySearchUrl = `https://open.spotify.com/search/${searchQuery}`;
    
    // Use provided URLs if available, otherwise use search URLs
    const youtubeUrl = song.youtube_url || youtubeSearchUrl;
    const spotifyUrl = song.spotify_url || spotifySearchUrl;
    
    const linksHTML = `
        <a href="${youtubeUrl}" target="_blank" class="platform-link youtube" title="Search on YouTube">
            <span>▶️</span> YouTube
        </a>
        <a href="${spotifyUrl}" target="_blank" class="platform-link spotify" title="Search on Spotify">
            <span>🎧</span> Spotify
        </a>
    `;
    
    card.innerHTML = `
        <div class="song-title">${song.title}</div>
        <div class="song-artist">${song.artist}</div>
        <div class="song-details">
            <span class="song-tag">🎵 ${song.genre}</span>
            <span class="song-tag">${getMoodEmoji(song.mood)} ${song.mood}</span>
            ${features.popularity ? `<span class="features-badge">⭐ ${features.popularity}% popular</span>` : ''}
        </div>
        <div class="song-details">
            ${features.tempo ? `<span class="song-tag">⏱️ ${features.tempo}</span>` : ''}
            ${features.energy ? `<span class="song-tag">⚡ ${features.energy}</span>` : ''}
            ${features.danceability ? `<span class="song-tag">💃 ${features.danceability}</span>` : ''}
        </div>
        <div class="platform-links">
            ${linksHTML}
        </div>
    `;
    
    return card;
}

// Get mood emoji
function getMoodEmoji(mood) {
    const emojis = {
        'happy': '😊',
        'sad': '😢',
        'energetic': '⚡',
        'relaxed': '😌',
        'angry': '😠'
    };
    return emojis[mood.toLowerCase()] || '🎵';
}

// Show error message
function showError(message) {
    alert('Error: ' + message);
}