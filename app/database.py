import aiosqlite
import os

DATABASE_URL = os.getenv("DATABASE_URL","tasks.db") # If not set, defaults to tasks.db. This is how Docker will pass the DB path later.

async def create_tables():
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS tasks (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             title TEXT NOT NULL,
                             description TEXT,
                             status TEXT NOT NULL DEFAULT 'pending',
                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                             completed_at TIMESTAMP
                             
                         )
                         """)
        await db.commit()

async def get_db():
    async with aiosqlite.connect(DATABASE_URL) as db:
        db.row_factory = lambda cursor, row: {
        description[0].lower(): value 
        for description, value in zip(cursor.description, row)
        } # row_factory = aiosqlite.Row — makes rows behave like dicts so you can do row["title"] instead of row[1]
        yield db