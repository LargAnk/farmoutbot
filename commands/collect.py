from replit import db
from zstats import merch, seeds, softSearch
import time
import random

async def collect(message, client):
	args = message.content.split(' ')
	if str(message.author.id) not in db['members']:
		await message.channel.send(f' {message.author.mention}\'s to-do list:\n\n1: make an account\n2: buy a seed\n3: buy a watering can\n4: plant the seeds\n5: water the plants\n6: wait for them to grow\n7: collect them')
		return
	if db['members'][str(message.author.id)]['plantcooldowns'] == {}:
		await message.channel.send(' you haven\'t planted anything u idiot')
		return
	if len(args) == 2:
		await message.channel.send(' what plant are you collecting lol')
		return
	plant = softSearch(merch, args[2], ["name"])
	if not bool(plant):
		await message.channel.send(" That's not a plant!")
		return
	if plant not in db['members'][str(message.author.id)]['plantcooldowns']:
		await message.channel.send(' you haven\'t planted that')
		return

	for i in seeds:
		if i != 'name':
			if seeds[i]['result'] == plant:
				seed = seeds[i]['name']


	growTime = seeds[seed]["stages"][db['members'][str(message.author.id)]['plantcooldowns'][plant]["stage"]] if "stages" in seeds[seed] else seeds[seed]["growtime"] 
	
	now = int(round(time.time()*1000))
	if db['members'][str(message.author.id)]['plantcooldowns'][plant]['cooldown'] + growTime > now:
		now2 = int(round(time.time() * 1000))
		f = db['members'][str(message.author.id)]['plantcooldowns'][plant]['cooldown'] - now2
		f = str(f)
		newvar = growTime+db['members'][str(message.author.id)]['plantcooldowns'][plant]['cooldown']
		e = round((newvar-now2)/1000)
		await message.channel.send(f' your plant isn\'t ready yet, wait `{str(e)}` seconds dumbo')
		return

	a = db['members']
	amount = a[str(message.author.id)]['plantcooldowns'][plant]['amount']
	chance = random.randint(0, 50)
	if not bool(chance) and amount > 5:
		things = ['whoops ur fat little fingers slipped and pulled out the plants by accident', 'you farted on the plants because you ate too many beans last night', 'you sneezed and blew all the plants away', 'some dumb animal came by and pulled them out', 'you were too fat and squeezed them by acccident', 'your plants ran away', 'you accidentally planted them in a volcano']
		thing = random.choice(things)
		thing2 = random.randint(1,3)
		await message.channel.send(f'{thing}. `{thing2}` of your plants died.')
		a[str(message.author.id)]['plantcooldowns'][plant]['amount'] -= thing2
		db['members'] = a
		return

	if "stages" in seeds[seed] and now - a[str(message.author.id)]['plantcooldowns'][plant]["start"] > seeds[seed]["stages"][2]:
		del a[str(message.author.id)]['plantcooldowns'][plant]
		return await message.channel.send(f"Oop your {plant} died of old age")

	amount = a[str(message.author.id)]['plantcooldowns'][plant]['amount']
	fart = round(amount/13)
	if fart > 10: fart = 10
	fart += amount
	if plant not in a[str(message.author.id)]['merch']:
		a[str(message.author.id)]['merch'][plant] = fart
	else:
		a[str(message.author.id)]['merch'][plant] += fart
	
	if "stages" in seeds[seed]:
		a[str(message.author.id)]['plantcooldowns'][plant]["cooldown"] = now
		a[str(message.author.id)]['plantcooldowns'][plant]["stage"] = 1
	
	else: del a[str(message.author.id)]['plantcooldowns'][plant]

	db['members'] = a
	name = merch[plant]['name']
	tts = [f'You collected `{fart}` {name}(s) from `{amount} {seed}(s)`. ', f'nice, you got `{fart}` {name}(s) from `{amount} {seed}(s)`.', f'from your `{amount} {seed}(s)` planted, you got `{fart}` {name}(s).', f'collection successful, `{fart}` {name}(s) were collected from `{amount} {seed}(s)`.']
	ts = random.choice(tts)
	await message.reply(f'{ts}')