import matplotlib.pyplot as plt
import aiosqlite
from config import DB_NAME

async def generate_score_chart():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT username, score FROM users ORDER BY score DESC LIMIT 10') as cursor:
            data = await cursor.fetchall()

    if not data:
        return None

    names = [x[0] for x in data]
    scores = [x[1] for x in data]

    plt.figure(figsize=(6, 4))
    plt.barh(names, scores)
    plt.xlabel("Очки")
    plt.ylabel("Игроки")
    plt.title("Топ-10 игроков квиза")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    path = "score_chart.png"
    plt.savefig(path)
    return path
