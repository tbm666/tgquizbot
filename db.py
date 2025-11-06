import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                score INTEGER DEFAULT 0
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_state (
                user_id INTEGER PRIMARY KEY,
                question_index INTEGER,
                score INTEGER
            )
        ''')
        await db.commit()


async def add_user(user_id, username):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', 
            (user_id, username)
        )
        await db.commit()


async def update_user_score(user_id, score):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE users SET score = score + ? WHERE user_id = ?', (score, user_id))
        await db.commit()


async def get_quiz_state(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index, score FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            res = await cursor.fetchone()
            return res if res else (0, 0)


async def update_quiz_state(user_id, question_index, score):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT OR REPLACE INTO quiz_state (user_id, question_index, score) 
            VALUES (?, ?, ?)
        ''', (user_id, question_index, score))
        await db.commit()
