from replit import db
import random
import time


async def beg(message, client):

    if str(message.author.id) not in db["members"]:
        return "your farm doesn't exist yet, do `start` first"
    now = int(round(time.time() * 1000))
    if (
        "beg" in db["members"][str(message.author.id)]["cooldowns"]
        and db["members"][str(message.author.id)]["cooldowns"]["beg"] < now
    ):
        now = int(round(time.time() * 1000))
        if db["members"][str(message.author.id)]["cooldowns"]["beg"] + 30000 > now:
            now2 = int(round(time.time() * 1000))
            f = db["members"][str(message.author.id)]["cooldowns"]["beg"] - now2
            f = str(f)
            newvar = 30000 + db["members"][str(message.author.id)]["cooldowns"]["beg"]
            e = round((newvar - now2) / 1000)
            return f"cant beg now, wait `{str(e)}` seconds."

    if db["members"][str(message.author.id)]["money"] >= 1000:
        return "you have too much money to beg. "
    coins = 0
    thing = random.randint(1, 3)
    if thing == 1:
        coins = random.randint(-1, -3)
        return f"**market:** no.\n{message.author.mention} you lost {coins} coins"
    if thing == 2:
        coins = random.randint(5, 10)
        return f"**market:** UGH fineeeee\n{message.author.mention} you gained {coins} coins "
    if thing == 3:
        coins = random.randint(10, 20)
        return (
            f"**market:** yessir\n{message.author.mention} you gained `{coins} coins`"
        )
    a = db["members"]
    a[str(message.author.id)]["money"] += coins
    db["members"] = a
