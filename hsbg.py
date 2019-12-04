import random

class Minion:
	def __init__(self, name, att, hp, stars=1, taunt=False, deathrattle=[], deatheffect=[], shield=False):
		self.name = name
		self.att = att
		self.hp = hp
		self.stars = stars
		self.taunt = taunt
		self.deathrattle = deathrattle
		self.deatheffect = deatheffect
		self.shield = shield
		# self.aura = []

	def __str__(self):
		bar = "=="
		stats = ""
		for i in range(len(self.name)):
			bar += "="
			if i >= len(str(self.att)) and i < len(self.name) - len(str(self.hp)):
				stats += " "
		return bar + "\n" \
				"|" + self.name + "|\n" + \
				"|" + str(self.att) + stats + str(self.hp) + "|\n" + \
				bar

	def fight(self, minion):
		if self.shield:
			self.shield = False
		else:
			self.hp -= minion.att
		if minion.shield:
			minion.shield = False
		else:
			minion.hp -= self.att

	def buff(self, att=0, hp=0):
		self.att += att
		self.hp += hp

class DeathEffect:
	def __init__(self, death_effect_id):
		self.death_effect_id = death_effect_id

	def handle(self, dying_board, other_board, i): #todo: put seed
		if self.death_effect_id == 1: #give random shield
			if len(dying_board) == 1:
				return
			j = None
			while i == j or j is None: 
				j = random.randrange(0,len(dying_board))
			dying_board.get_minion(j).shield = True

class Board:
	def __init__(self):
		self.minions = []
		self.rank = 1

	def __str__(self):
		string = "board:\n[\n"
		for minion in self.minions:
			string += minion.__str__()
		string += "\n]"
		return string 

	def summon(self, minion):
		self.minions.append(minion)

	def cleanup(self):
		for i in range(len(self.minions)):
			if i >= len(self.minions):
				break
			if self.minions[i].hp <= 0:
				for effect in self.minions[i].deatheffect:
					effect.handle(self,None,i)
				self.minions = self.minions[:i] + self.minions[i].deathrattle + self.minions[i+1:]
				i -= 1
		return len(self) == 0

	def get_minion(self, i):
		if i >= len(self):
			return self.minions[i%len(self)]
		else:
			return self.minions[i]

	def get_damage(self):
		damage = 0
		for minion in self.minions:
			damage += minion.stars
		return damage + self.rank

	def get_taunts(self):
		taunts = 0
		for minion in self.minions:
			if minion.taunt:
				taunts += 1
		return taunts

	def __len__(self):
		return len(self.minions)

class Result:
	def __init__(self,target,damage):
		self.target = target
		self.damage = damage

	def __str__(self):
		string = ""
		if self.target == 1:
			string += "Win! They "
		elif self.target == 0:
			string += "Loss! You "
		else:
			string += "Tie! Both "
		string += "took " + str(self.damage) + " damage."
		return string

def combat(bottom_board, top_board, seed=[]):
	if len(seed) == 0:
		seed.append(random.randrange(0,2))
	done_fighting = top_board.cleanup()
	done_fighting = bottom_board.cleanup() or done_fighting
	i = 1
	bottom_fight = seed[0] == 0
	top_tape = 0
	bottom_tape = 0
	while(not done_fighting):
		if bottom_fight:
			target, i = get_target(top_board, seed, i)
			bottom_board.get_minion(bottom_tape).fight(top_board.get_minion(target))
			bottom_tape += 1
		else:
			target, i = get_target(bottom_board, seed, i)
			top_board.get_minion(top_tape).fight(bottom_board.get_minion(target))
			top_tape += 1
		done_fighting = top_board.cleanup()
		done_fighting = bottom_board.cleanup() or done_fighting
		bottom_fight = not bottom_fight
	if len(bottom_board) == 0:
		if len(top_board) == 0:
			return Result(-1, 0)
		else:
			return Result(0,top_board.get_damage())
	if len(top_board) == 0:
		return Result(1,bottom_board.get_damage())
	print("COMBAT FINISHED WITHOUT A WINNER")
	return None

def get_target(board, seed, i):
	target = None
	taunts = board.get_taunts()
	while(target is None):
		if taunts == 0:
			if i >= len(seed):
				seed.append(random.randrange(0,len(board)))
			target = seed[i]
		else:
			if i >= len(seed):
				seed.append(random.randrange(0,len(board)))
			target = seed[i]
		i += 1
	return (target, i)

def create_minion(minion_id=None, name=None):
	if minion_id is None and name is None:
		print("I cant create nothing bro")
		return
	name_id_map = {"Alleycat": 1, "Tabbycat": 2, "Direwolf Alpha": 3, "Voidwalker": 4, "Vulgar Humunculus": 5, "Mecharoo": 6, "Joe-E Bot": 7, "Micro Machine": 8, "Murloc Tidecaller": 9, "Murloc Tidehunter": 10, "Murloc": 11, "Rockpool Hunter": 12, "Righteous Protector": 13, "Selfless Hero": 14, "Wrath Weaver": 15}
	id_name_map = {1: "Alleycat", 2: "Tabbycat", 3: "Direwolf Alpha", 4: "Voidwalker", 5: "Vulgar Humunculus", 6: "Mecharoo", 7: "Joe-E Bot", 8: "Micro Machine", 9: "Murloc Tidecaller", 10: "Murloc Tidehunter", 11: "Murloc", 12: "Rockpool Hunter", 13: "Righteous Protector", 14: "Selfless Hero", 15: "Wrath Weaver"}
	if name is not None:
		minion_id = name_id_map.get(name)
		if minion_id is None:
			print(name + " is a bad name")
			return
	if name is None:
		name = id_name_map.get(minion_id)
		if name is None:
			print(minion_id + " is a bad id")
	att = 0
	hp = 0
	stars = 1
	taunt = False
	deathrattle = []
	deatheffect = []
	shield = False
	if minion_id == 1:
		att = 1
		hp = 1
	elif minion_id == 2:
		att = 1
		hp = 1
	elif minion_id == 3:
		att = 2
		hp = 2
	elif minion_id == 4:
		att = 1
		hp = 3
	elif minion_id == 5:
		att = 2
		hp = 4
		taunt=True
	elif minion_id == 6:
		att = 1
		hp = 1
		deathrattle = [create_minion(7)]
	elif minion_id == 7:
		att = 1
		hp = 1
	elif minion_id == 8:
		att = 1
		hp = 2
	elif minion_id == 9:
		att = 1
		hp = 2
	elif minion_id == 10:
		att = 2
		hp = 1
	elif minion_id == 11:
		att = 1
		hp = 1
	elif minion_id == 12:
		att = 2
		hp = 3
	elif minion_id == 13:
		att = 1
		hp = 1
		shield = True
	elif minion_id == 14:
		att = 2
		hp = 1
	elif minion_id == 15:
		att = 1
		hp = 1
	return Minion(name, att, hp, stars=stars, taunt=taunt, deathrattle=deathrattle, deatheffect=deatheffect, shield=shield)

their_board = Board()
their_board.summon(Minion("shield",2,5, deatheffect=[DeathEffect(1)]))
their_board.summon(Minion("one",1,5))
my_board = Board()
my_board.summon(Minion("Amalgam",1,5))
result = combat(my_board, their_board, [0,0])
print(their_board)
print(my_board)
print(result)