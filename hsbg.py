import random
import copy
import csv

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
		return self

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
		if self.target == -1:
			string += "Win! They "
		elif self.target == 1:
			string += "Loss! You "
		else: #self.target == 0
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
			return Result(0, 0)
		else:
			return Result(-1,top_board.get_damage())
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

def simulate(bottom_board_number, top_board_number, seeds=None, simulations=1000):
	bottom_board = build_board(bottom_board_number)
	top_board = build_board(top_board_number)
	bottom_board.cleanup()
	top_board.cleanup()
	results = {}
	if seeds is None:
		seeds = [[random.randrange(0,2)] for i in range(simulations)]
	for seed in seeds:
		bottom = copy.deepcopy(bottom_board)
		top = copy.deepcopy(top_board)
		result = combat(bottom, top, seed)
		dmg = result.damage * result.target
		if dmg in results:
			results[dmg] = results[dmg] + 1
		else:
			results[dmg] = 1
	return results

def build_board(board_number):
	board = Board()
	if board_number == 0: #straight buy
		board.summon(create_minion(1))
		board.summon(create_minion(2))
	elif board_number == 1:
		board.summon(create_minion(3))
	elif board_number == 2:
		board.summon(create_minion(4))
	elif board_number == 3:
		board.summon(create_minion(5))
	elif board_number == 4:
		board.summon(create_minion(6))
	elif board_number == 5:
		board.summon(create_minion(8))
	elif board_number == 6:
		board.summon(create_minion(9))
	elif board_number == 7:
		board.summon(create_minion(10))
		board.summon(create_minion(11))
	elif board_number == 8:
		board.summon(create_minion(12))
	elif board_number == 9:
		board.summon(create_minion(13))
	elif board_number == 10:
		board.summon(create_minion(14))
	elif board_number == 11:
		board.summon(create_minion(15))
	elif board_number == 12: #brann
		board.summon(create_minion(1).buff(1,1))
		board.summon(create_minion(2))
	elif board_number == 13:
		board.summon(create_minion(5).buff(1,1))
	elif board_number == 14:
		board.summon(create_minion(10).buff(1,1))
		board.summon(create_minion(11))
	elif board_number == 15:
		board.summon(create_minion(11).buff(1,1))
		board.summon(create_minion(10))
	elif board_number == 16:
		board.summon(create_minion(12))
	elif board_number == 17: #yogg
		board.summon(create_minion(1).buff(1,1))
		board.summon(create_minion(2))
	elif board_number == 18:
		board.summon(create_minion(3).buff(1,1))
	elif board_number == 19:
		board.summon(create_minion(4).buff(1,1))
	elif board_number == 20:
		board.summon(create_minion(5).buff(1,1))
	elif board_number == 21:
		board.summon(create_minion(6).buff(1,1))
	elif board_number == 22:
		board.summon(create_minion(8).buff(1,1))
	elif board_number == 23:
		board.summon(create_minion(9).buff(1,1))
	elif board_number == 24:
		board.summon(create_minion(10).buff(1,1))
		board.summon(create_minion(11))
	elif board_number == 25:
		board.summon(create_minion(11).buff(1,1))
		board.summon(create_minion(10))
	elif board_number == 26:
		board.summon(create_minion(12).buff(1,1))
	elif board_number == 27:
		board.summon(create_minion(13).buff(1,1))
	elif board_number == 28:
		board.summon(create_minion(14).buff(1,1))
	elif board_number == 29:
		board.summon(create_minion(15).buff(1,1))
		#rat king
		#curator
		#rag
		#nefarian
		#lich king
		#mech girl
		#patches
		#sir finley
		#queen tagwoggle
		#AFK
	return board

def run_simulations():
	results = {}
	for i in range(13,14):
		for j in range(i,12):
			results[i,j] = simulate(i,j)
	return results

# their_board = Board()
results = run_simulations()
print(results)

# with open('test.csv', 'w') as f:
    # for key in results.keys():
        # f.write("%s,%s\n"%(key,results[key]))

# their_board.summon(Minion("Murloc",1,1))
# their_board.summon(Minion("Murloc Tidecaller",2,2))
# print(their_board)
# my_board = Board()
# my_board.summon(Minion("Direwolf Alpha",1,1))
# my_board.summon(Minion("Direwolf Alpha",2,2))
# results = simulate(my_board, their_board, simulations=10)