import sqlite3
import os
from datetime import datetime

def init_database():
    """Initialize the FluentPass database with all required tables."""
    
    # Create database directory in /tmp for Render deployment
    db_dir = "."
    if os.environ.get("RENDER"):
        db_dir = "/tmp"
    
    # Database file path
    db_path = os.path.join(db_dir, 'fluentpass.db')
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            native_language VARCHAR(20) DEFAULT 'English',
            target_cefr_level VARCHAR(5) DEFAULT 'B2',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            email_verified BOOLEAN DEFAULT FALSE,
            profile_picture_url VARCHAR(255)
        )
    """)
    
    # Create user_sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token VARCHAR(255) UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address VARCHAR(45),
            user_agent TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    # Create user_progress table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            current_cefr_level VARCHAR(5) DEFAULT 'B1',
            total_xp INTEGER DEFAULT 0,
            current_streak_days INTEGER DEFAULT 0,
            longest_streak_days INTEGER DEFAULT 0,
            total_words_written INTEGER DEFAULT 0,
            total_texts_analyzed INTEGER DEFAULT 0,
            total_study_time_minutes INTEGER DEFAULT 0,
            last_activity_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    # Create writing_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS writing_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original_text TEXT NOT NULL,
            ai_feedback TEXT,
            assessed_level VARCHAR(5),
            word_count INTEGER,
            topic VARCHAR(100),
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            feedback_score DECIMAL(3,2),
            improvement_areas TEXT,
            corrected_text TEXT,
            vocabulary_extracted TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    # Create achievements table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            icon_url VARCHAR(255),
            category VARCHAR(50),
            points_required INTEGER,
            condition_type VARCHAR(50),
            condition_value INTEGER,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create user_achievements table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            achievement_id INTEGER NOT NULL,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            progress_value INTEGER DEFAULT 0,
            is_completed BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE,
            UNIQUE(user_id, achievement_id)
        )
    """)
    
    # Insert default achievements
    default_achievements = [
        ("First Steps", "Complete your first writing exercise", None, "writing", 10, "texts_analyzed", 1),
        ("Word Warrior", "Write 1000 words total", None, "writing", 50, "words_written", 1000),
        ("Streak Master", "Maintain a 7-day learning streak", None, "consistency", 100, "streak_days", 7),
        ("Level Up", "Advance to B2 level", None, "progress", 200, "level_advancement", 1),
        ("Vocabulary Builder", "Learn 100 new words", None, "vocabulary", 75, "vocabulary_learned", 100),
        ("Dedicated Learner", "Study for 10 hours total", None, "time", 150, "study_time", 600),
        ("Writing Expert", "Complete 50 writing exercises", None, "writing", 300, "texts_analyzed", 50),
        ("Consistency Champion", "Maintain a 30-day streak", None, "consistency", 500, "streak_days", 30)
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO achievements 
        (name, description, icon_url, category, points_required, condition_type, condition_value)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, default_achievements)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database initialized successfully at: {db_path}")
    return db_path

if __name__ == "__main__":
    init_database()


