import sqlite3
import os
from datetime import datetime

def init_content_database():
    """Initialize the FluentPass content database with all required tables."""
    
    # Create database directory in /tmp for Render deployment
    db_dir = "."
    if os.environ.get("RENDER"):
        db_dir = "/tmp"
    
    # Database file path
    db_path = os.path.join(db_dir, 'fluentpass.db')
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create content_library table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content_library (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) NOT NULL,
            content_type VARCHAR(50) NOT NULL, -- 'reading', 'listening', 'grammar', 'vocabulary', 'exam_prep'
            cefr_level VARCHAR(5) NOT NULL, -- 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'
            topic VARCHAR(100) NOT NULL,
            difficulty_score INTEGER DEFAULT 1, -- 1-10 scale
            text_content TEXT,
            summary TEXT,
            audio_url VARCHAR(255),
            duration_minutes INTEGER,
            word_count INTEGER,
            tags TEXT, -- JSON array of tags
            exam_type VARCHAR(50), -- 'goethe', 'telc', 'testdaf', 'osd', 'general'
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create vocabulary_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vocabulary_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER NOT NULL,
            german_word VARCHAR(100) NOT NULL,
            english_translation VARCHAR(200) NOT NULL,
            example_sentence TEXT,
            word_type VARCHAR(50), -- 'noun', 'verb', 'adjective', 'adverb', etc.
            difficulty_level VARCHAR(5), -- CEFR level
            frequency_rank INTEGER, -- How common the word is
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (content_id) REFERENCES content_library(id) ON DELETE CASCADE
        )
    """)
    
    # Create anki_cards table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS anki_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER NOT NULL,
            front_text TEXT NOT NULL,
            back_text TEXT NOT NULL,
            card_type VARCHAR(50) DEFAULT 'vocabulary', -- 'vocabulary', 'grammar', 'phrase'
            difficulty_level VARCHAR(5),
            tags TEXT, -- JSON array of tags
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (content_id) REFERENCES content_library(id) ON DELETE CASCADE
        )
    """)
    
    # Create grammar_rules table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grammar_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER NOT NULL,
            rule_name VARCHAR(100) NOT NULL,
            rule_description TEXT NOT NULL,
            examples TEXT, -- JSON array of examples
            cefr_level VARCHAR(5) NOT NULL,
            category VARCHAR(50), -- 'cases', 'verbs', 'adjectives', 'syntax', etc.
            difficulty_score INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (content_id) REFERENCES content_library(id) ON DELETE CASCADE
        )
    """)
    
    # Create user_content_progress table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_content_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content_id INTEGER NOT NULL,
            completion_status VARCHAR(20) DEFAULT 'not_started', -- 'not_started', 'in_progress', 'completed'
            completion_percentage INTEGER DEFAULT 0,
            time_spent_minutes INTEGER DEFAULT 0,
            last_accessed TIMESTAMP,
            score DECIMAL(5,2), -- User's score on the content (if applicable)
            notes TEXT, -- User's personal notes
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (content_id) REFERENCES content_library(id) ON DELETE CASCADE,
            UNIQUE(user_id, content_id)
        )
    """)
    
    # Create content_categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL UNIQUE,
            description TEXT,
            icon_url VARCHAR(255),
            color_code VARCHAR(7), -- Hex color code
            sort_order INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create content_tags table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER NOT NULL,
            tag_name VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (content_id) REFERENCES content_library(id) ON DELETE CASCADE
        )
    """)
    
    # Insert default content categories
    default_categories = [
        ("Daily Life", "Everyday situations and conversations", None, "#4CAF50", 1),
        ("Work & Career", "Professional and business German", None, "#2196F3", 2),
        ("Travel & Tourism", "Travel-related vocabulary and situations", None, "#FF9800", 3),
        ("Education & Study", "Academic and educational content", None, "#9C27B0", 4),
        ("Health & Wellness", "Medical and health-related topics", None, "#F44336", 5),
        ("Culture & Society", "German culture and social topics", None, "#795548", 6),
        ("Environment & Nature", "Environmental and nature topics", None, "#4CAF50", 7),
        ("Technology & Media", "Technology and media-related content", None, "#607D8B", 8),
        ("Grammar Fundamentals", "Core grammar rules and structures", None, "#3F51B5", 9),
        ("Exam Preparation", "Specific exam preparation materials", None, "#E91E63", 10)
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO content_categories 
        (name, description, icon_url, color_code, sort_order)
        VALUES (?, ?, ?, ?, ?)
    """, default_categories)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Content database initialized successfully at: {db_path}")
    return db_path

if __name__ == "__main__":
    init_content_database()


