from replit import db
from zstats import convertInt, getShop
import random


async def sell(message, client):
    args = message.content.split(" ")
    if str(message.author.id) not in db["members"]:
        await message.channel.send(" make an account to sell stuff")
        return
    if len(args) == 2:
        await message.channel.send(" what are you selling lol")
        return

    thing = None
    allPos = []
    objs = []
    obj = {"animals": {}, "tools": {}, "seeds": {}, "merch": {}}
    getShop(obj, db["members"][str(message.author.id)]["location"])
    animals, tools, seeds, merch = (
        obj["animals"],
        obj["tools"],
        obj["seeds"],
        obj["merch"],
    )
    for i in [seeds, merch, tools, animals]:
        possibilities = [j for j in list(i.keys()) if args[2] in j and j != "name"]
        if not bool(possibilities):
            continue
        allPos.extend(possibilities)
        for j in possibilities:
            objs.append(i)
    if not bool(allPos):
        await message.channel.send(" that does not exist.")
        return
    smallest = min(allPos, key=len)
    thing = objs[allPos.index(smallest)]
    item = thing[smallest]
    key = smallest
    if not str(item["sellcost"]).isnumeric():
        await message.channel.send(" You can't sell that item!")
        return
    if key not in db["members"][str(message.author.id)][thing["name"]]:
        await message.channel.send(" you don't have that")
        return
    if key in tools:
        thing = tools
    if len(args) == 3:
        amount = 1
    elif len(args) == 4 and args[3] in ["a", "all", "max"]:
        if thing["name"] in ["animals", "seeds"]:
            amount = db["members"][str(message.author.id)][thing["name"]][key]["amount"]
        if thing["name"] in ["merch"]:
            amount = db["members"][str(message.author.id)]["merch"][key]
        if thing == tools:
            amount = 1
    elif len(args) == 4:
        amount = convertInt(args[3])
        if not bool(amount):
            amount = 1
    else:
        amount = 1
    if amount <= 0:
        await message.channel.send(
            "what are you doing, how are you supposed to sell negative things, go back to kindergarten u idiot"
        )
        return

    thingr = random.randint(1, 35)
    if thingr == 1:
        if "undeadwool" in db["members"][str(message.author.id)]["merch"]:
            return
        things = ["rock", "tree", "rock", "stone"]
        thing2 = random.choice(things)
        await message.channel.send(
            f"On the way over to sell your thingies, you accidentally punched a hard {thing2} and died. you paid 100 coins to be reborn."
        )
        a = db["members"]
        if a[str(message.author.id)]["money"] < 100:
            a[str(message.author.id)]["money"] = 0
        else:
            a[str(message.author.id)]["money"] -= 100
        db["members"] = a
        return

    got = thing[key]["sellcost"]
    got *= amount
    got = round(got)

    a = db["members"]
    if thing["name"] in ["animals", "seeds"]:
        if amount > a[str(message.author.id)][thing["name"]][key]["amount"]:
            await message.channel.send(" you don't have that many")
            return
    if thing["name"] == "merch":
        if amount > a[str(message.author.id)]["merch"][key]:
            await message.channel.send(" you don't have that many")
            return
    if thing["name"] == "tools":
        if key not in a[str(message.author.id)]["tools"]:
            await message.channel.send("you dont have that")
            return
        amount = 1
    if thing["name"] == "tools":
        amount = 1

    a[str(message.author.id)]["money"] += got
    if thing["name"] in ["merch"]:
        a[str(message.author.id)][thing["name"]][key] -= amount
        if a[str(message.author.id)][thing["name"]][key] == 0:
            del a[str(message.author.id)]["merch"][key]
    elif thing["name"] in ["animals", "seeds"]:
        a[str(message.author.id)][thing["name"]][key]["amount"] -= amount
        if a[str(message.author.id)][thing["name"]][key]["amount"] == 0:
            del a[str(message.author.id)][thing["name"]][key]
    else:
        del a[str(message.author.id)][thing["name"]][key]
    a[str(message.author.id)]["amounts"]["sold"] += amount
    db["members"] = a

    repgain = random.choice(1,4)
    repmsg = ''
    if repgain == 1:
      a = db['members'][str(message.author.id)]['reputation']
      gain = random.choice(1,3)
      a = gain
      repmsg = 'market: thanks for selling that thing, i really wanted it         **reputation +gain**'
      db['members'][str(message.author.id)]['reputation'] = a

    money = db["members"][str(message.author.id)]["money"]
    tts = [
        f"You sold `{amount} {key}(s)` for `{got} coins`. you now have `{money} coins`",
        f"`{amount} {key}(s)` sold successfully.",
        f"yessir you got `{got} coins`, now you have `{money}` total",
        f"selling success, you gained `{got} coins`",
    ]
    ts = random.choice(tts)
    await message.reply(f"{ts}\n{repmsg}")
