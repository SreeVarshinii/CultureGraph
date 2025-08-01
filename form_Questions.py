# --- Co-Founder Scenario Questions ---
scenario_questions = [
    ("How do you typically handle disagreements in a team setting?", "I usually try to listen to everyone and then find a fair solution."),
    ("What role do you usually take in a group project?", "I often end up organizing and making sure everyone’s on track."),
    ("Describe your ideal work environment.", "Quiet, focused, with minimal interruptions."),
    ("How do you approach deadlines and time management?", "I create a schedule and follow it strictly."),
    ("How do you handle failure?", "I reflect on what went wrong and try to learn from it."),
    ("What's your approach to taking risks in business?", "I assess everything logically before taking a step."),
    ("How do you recharge or take breaks during intense periods?", "I take short walks and listen to music."),
    ("How do you deal with ambiguity or uncertain situations?", "I analyze the situation and reduce ambiguity with planning."),
    ("What values are non-negotiable for you in a professional relationship?", "Honesty, accountability, and mutual respect."),
    ("If there's a major disagreement with your co-founder, how would you resolve it?", "I’d initiate a calm discussion and try to align perspectives."),
    ("What would you do if your co-founder wanted to pivot in a direction you strongly disagreed with?", "I'd want to understand their reasoning first."),
    ("How do you usually recharge after a stressful day?", "I usually go for a walk or listen to music."),
    ("What motivates you the most when building something new?", "Solving real problems and helping people."),
    ("What's your preferred way of communicating in a team?", "Short async check-ins with room for autonomy."),
    ("What kind of working rhythm suits you best (e.g., early morning, async, deep work)?", "Deep work in the morning."),
    ("How do you respond when your ideas are challenged by your teammate?", "I welcome pushback if it's logical."),
    ("If your startup faced financial uncertainty, what would be your instinctive action?", "Cut non-essentials and double down on core."),
    ("What motivates you to wake up and build every day?", "Knowing I’m building something that matters."),
    ("Would you rather build something meaningful to you or something that will definitely scale?", "I'd go for meaningful even if it's slower."),
    ("How do you give feedback to your teammates?", "Start with empathy and clarity."),
    ("How often do you like to check in with your co-founder?", "Once a week syncs, plus async notes."),
    ("How do you balance personal life and startup work?", "Hard stop at 7 PM — recharge is important."),
    ("How do you respond when you’re overwhelmed or overcommitted?", "I step away briefly and then prioritize."),
    ("What does success look like to you?", "Success is doing work I’m proud of, sustainably."),
    ("What kind of impact do you want your work to have on the world?", "I want to enable better lives through technology."),
    ("How do you approach decision-making under pressure?", "I slow down and weigh every option carefully."),
    ("How do you stay motivated during long, difficult projects?", "I revisit the purpose and impact of what I’m building.")
]

# --- Cultural Categories ---
categories = {
    "🎵 Music Identity": [
        ("Favorite Artists", "music_artists", "text", "Taylor Swift"),
        ("Regularly Listened Bands", "music_bands", "text", "Imagine Dragons"),
        ("Genres that Define You", "music_genres", "multi3", ["Pop", "Rock", "Hip-Hop", "Jazz", "Classical"]),
        ("Artist You'd Travel to See", "music_travel", "text", "Coldplay"),
        ("Artist Reflecting Your Energy", "music_energy", "text", "Adele")
    ],
    "📚 Intellectual Taste": [
        ("Favorite Books or Authors", "books_authors", "text", "George Orwell"),
        ("Most Read Genre", "book_genres", "multi3", ["Fiction", "Non-Fiction", "Science Fiction", "Biography", "Mystery"]),
        ("Book that Influenced You", "book_influence", "text", "1984"),
        ("Books You Dislike", "book_dislike", "text", "Romance Novels"),
        ("Book to Gift a Co-Founder", "book_gift", "text", "The Lean Startup")
    ],
    "🛍 Lifestyle & Aesthetic": [
        ("Brands You Use Daily", "brands_daily", "text", "Apple, Nike, Google"),
        ("Value-Aligned Fashion/Tech Brands", "brands_values", "text", "Patagonia, Tesla"),
        ("Brands You Trust Most", "brands_trust", "text", "Amazon, Sony, IKEA"),
        ("Inspirational Brands for Builders", "brands_builder", "text", "Tesla"),
        ("Preferred Product Aesthetic", "product_aesthetic", "radio", ["Sleek", "Minimalist", "Colorful", "Raw"])
    ],
    "✈ Travel Preferences": [
        ("Top 3 Dream Destinations", "travel_dreams", "text", "Japan, Iceland, Italy"),
        ("Peaceful/Creative Place", "travel_peace", "text", "Bali"),
        ("Places You Travel to Most", "travel_type", "radio", ["Mountains", "Cities", "Islands", "Villages"]),
        ("Remote Work Destination", "travel_remote", "text", "Portugal"),
        ("Most Admired Culture", "travel_culture", "text", "Japanese")
    ],
    "🎬 Film Personality": [
        ("Films That Shaped You", "film_influence", "text", "Inception"),
        ("Genres You Rewatch", "film_genres", "multi", ["Drama", "Comedy", "Sci-Fi", "Action", "Fantasy"]),
        ("Director You Admire", "film_director", "text", "Christopher Nolan"),
        ("Movie Reflecting Your Philosophy", "film_philosophy", "text", "The Pursuit of Happyness"),
        ("Film Universe You'd Live In", "film_universe", "text", "Marvel Universe")
    ],
    "👥 Inspiration & Role Models": [
        ("Most Inspiring Professional", "role_inspire", "text", "Steve Jobs"),
        ("Followed Public Figures", "role_public", "text", "Elon Musk, Oprah Winfrey, Barack Obama"),
        ("Dream Podcast Guest or Mentor", "role_mentor", "text", "Naval Ravikant"),
        ("Favorite Modern Thinker", "role_thinker", "text", "Yuval Noah Harari"),
        ("Relatable Celebrity Lifestyle", "role_celebrity", "text", "Emma Watson")
    ],
    "🗺 Emotional Geography": [
        ("Where You Grew Up", "geo_upbringing", "text", "Chennai, India"),
        ("Cities That Feel Like Home", "geo_home", "text", "New York, San Francisco, Mumbai"),
        ("City You'd Live in Long-term", "geo_future", "text", "Amsterdam"),
        ("Region Matching Your Lifestyle", "geo_region", "text", "Scandinavia"),
        ("Place You Feel Most Inspired", "geo_inspired", "text", "Tokyo")
    ],
    "🎙 Listening & Learning": [
        ("Top 5 Podcasts", "podcasts_fav", "text", "The Daily, Lex Fridman, Tim Ferriss"),
        ("Podcast That Changed You", "podcast_change", "text", "Naval Podcast"),
        ("Favorite Podcast Host", "podcast_host", "text", "Tim Ferriss"),
        ("Preferred Format", "podcast_format", "radio", ["Interview", "Solo", "News", "Storytelling"]),
        ("When You Listen", "podcast_time", "radio", ["Morning", "Work", "Evening", "Commute"])
    ],
    "📺 Media Affinity": [
        ("Shows You Rewatch", "tv_rewatch", "text", "Friends, The Office"),
        ("Comfort Show", "tv_comfort", "text", "Brooklyn Nine-Nine"),
        ("Favorite Character Show", "tv_character", "text", "Ted Lasso"),
        ("Genre You Binge Most", "tv_genres", "multi", ["Comedy", "Thriller", "Drama", "Fantasy", "Reality"]),
        ("Must-Watch Show", "tv_mustwatch", "text", "Black Mirror")
    ],
    "🎮 Play Style & Strategy": [
        ("Games You Play Most", "game_most", "text", "Minecraft, FIFA"),
        ("Solo/Co-op/Competitive?", "game_mode", "radio", ["Solo", "Co-op", "Competitive"]),
        ("Favorite Game Universe", "game_universe", "text", "The Witcher"),
        ("Game Reflecting Decision Style", "game_decision", "text", "Civilization VI"),
        ("Game Genre That Defines You", "game_genre", "multi", ["RPG", "Shooter", "Strategy", "Simulation", "Adventure"])
    ]}
