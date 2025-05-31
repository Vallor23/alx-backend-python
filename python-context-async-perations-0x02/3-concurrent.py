import aiosqlite
import asyncio
import os
# from dotenv  import load_dotenv

# load_dotenv()

async def async_fetch_users():
    async with aiosqlite.connect("user_db") as db:
        db.row_factory = aiosqlite.Row #Allows accessing colums as rows
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return [(row["id"], row["name"],row["age"]) for row in rows]

async def async_fetch_older_users():
    async with aiosqlite.connect("user_db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return [(row["id"], row["name"],row["age"]) for row in rows]

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
if __name__ == "__main__":
    asyncio.run(fetch_concurrently()) 
        


       