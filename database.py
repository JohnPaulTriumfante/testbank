import sqlite3

def create_database():
    conn = sqlite3.connect("testbank.db")
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # Drop tables in correct order
    cursor.execute("DROP TABLE IF EXISTS choices")
    cursor.execute("DROP TABLE IF EXISTS questions")
    cursor.execute("DROP TABLE IF EXISTS problems")
    cursor.execute("DROP TABLE IF EXISTS chapters")

    # 1️⃣ Chapters table
    cursor.execute("""
        CREATE TABLE chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_number INTEGER NOT NULL,
            chapter_title TEXT NOT NULL
        );
    """)

    # 2️⃣ Problems table
    cursor.execute("""
        CREATE TABLE problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER NOT NULL,
            section TEXT,                 -- optional (Basic, Comprehensive)
            problem_code TEXT NOT NULL,   -- 1-1, 2-1, etc.
            standard TEXT,                -- IFRS, AICPA, AICA, etc.
            problem_text TEXT NOT NULL,
            FOREIGN KEY (chapter_id) REFERENCES chapters(id)
        );
    """)

    # 3️⃣ Questions table
    cursor.execute("""
        CREATE TABLE questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            correct_choice TEXT NOT NULL,
            explanation TEXT,
            FOREIGN KEY (problem_id) REFERENCES problems(id)
        );
    """)

    # 4️⃣ Choices table
    cursor.execute("""
        CREATE TABLE choices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            choice_label TEXT NOT NULL,
            choice_text TEXT NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        );
    """)

    # 5️⃣ Exam History table
    cursor.execute("""
        CREATE TABLE exam_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            created_date TEXT NOT NULL,
            num_questions INTEGER NOT NULL,
            include_problems INTEGER DEFAULT 0,
            FOREIGN KEY (chapter_id) REFERENCES chapters(id)
        );
    """)

    conn.commit()
    conn.close()
    print("Database recreated successfully.")


if __name__ == "__main__":
    create_database()