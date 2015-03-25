import math
import time
import webbrowser
import Tkinter
from PIL import Image, ImageDraw,ImageTk,ImageFont
import random
import copy
class Res:
	sheep = 0
	wheat = 1
	log = 2
	brick = 3
	ore = 4
	desert = 5

class Purch:
	road = 1
	sett = 2
	city = 3
	devc = 4

class Devs:
	knight = 1
	hakken = 2
	vp = 3
	monopoly = 4
	roadbuild = 5
	
class Moves:
	road = 0
	settle = 1
	city = 2
	playdev = 3
	drawdev = 4
	tbank = 5
	tplayer = 6
	
	
class ZaMove():
	def __init__(self,pnum,type,spot1=None,spot2=None,resgive=None,resget=None,devtype=None):
		self.type = type
		self.pnum = pnum
		if type == Moves.road:
			self.spot1 = spot1
			self.spot2 = spot2
		if type == Moves.settle or type == Moves.city:
			self.spot1 = spot1
		if type == playdev:
			self.devtype = devtype
		if type == tbank:
			self.resget = resget
			self.resgive = resgive

	
import itertools

def lol2set(lol):
	lol.sort()
	return list(lol for lol,_ in itertools.groupby(lol))


class agent():
	def __init__(self,pnum,board):
		self.playernum = pnum
		self.gboard = board
		self.hand = []
		self.devcards = []
		self.knights = 0
		self.longestroad = 0
		self.maxsettles = 6
		self.maxcities = 4
		self.vp = 0
		self.maxroads = 29
		self.settles = []
		self.cities = []
		self.roads = []
		self.trades = {"four": True, "three": False, "log": False, "ore": False, "brick": False, "sheep": False, "wheat": False}
		
	def place_settlement(self,i, init):
		if self.gboard.settlementlegal(self.playernum,i,init) and len(self.settles) < self.maxsettles and (init or self.canafford(Purch.sett)):
			self.buy(Purch.sett)
			self.settles.append(i)
			print str(self.playernum) + "placed a settlement at " + str(i) + " totaling " + str(len(self.settles))

			self.gboard.addsett(self.playernum,i)
			if i in self.gboard.harbors:
				self.trades[self.gboard.harbors[i]] = True
		else:
			print "FAILED to place settlement"
			
	def place_road(self,i,j,init):
		if self.gboard.roadlegal(self.playernum,i,j) and len(self.roads) < self.maxroads and (init or self.canafford(Purch.road)):
			print str(self.playernum) + "placed a road at " + str(i) + "-" + str(j) + " totaling " + str(len(self.roads))
			self.buy(Purch.road)
			self.roads.append([i,j])
			self.gboard.addroad(self.playernum,i,j)
		else:
			print "FAILED to place road at " + str(i) + "-" + str(j)

			# check for maxroad
			
	def place_city(self,i):
		if self.gboard.citylegal(self.playernum,i) and len(self.cities) < self.maxcities and self.canafford(Purch.city):
			self.buy(Purch.city)
			self.cities.append(i)
			self.settles.remove(i)
			print str(self.playernum) + "placed a city at " + str(i) + " totaling " + str(len(self.cities))
			self.gboard.addcity(self.playernum,i)
		else:
			print "FAILED to place city"
			
	def buy_devc(self,i):
		if self.canafford(Purch.devc):
			self.buy(Purch.devc)
			self.devcards.append(self.gboard.drawdev())
		else:
			print "Can't afford dev card"
					
	def has(self,list):
		z = copy.deepcopy(self.hand)
		for nec in list:
			if nec in z:
				z.remove(nec)
			else:
				return False
		return True

	def spend(self,list):
		for nec in list:
			if nec in self.hand:
				self.hand.remove(nec)
			else:
				return False
		return True	
	
	def canafford(self,purch):
		if purch == Purch.road:
			return self.has([Res.brick,Res.log])
		if purch == Purch.sett:
			return self.has([Res.brick,Res.log,Res.sheep,Res.wheat])
		if purch == Purch.city:
			return self.has([Res.ore,Res.ore,Res.ore,Res.wheat,Res.wheat])
		if purch == Purch.devc:
			return self.has([Res.sheep,Res.wheat,Res.ore])
			
	def buy(self,purch):
		if purch == Purch.road:
			return self.spend([Res.brick,Res.log])
		if purch == Purch.sett:
			return self.spend([Res.brick,Res.log,Res.sheep,Res.wheat])
		if purch == Purch.city:
			return self.spend([Res.ore,Res.ore,Res.ore,Res.wheat,Res.wheat])
		if purch == Purch.devc:
			return self.spend([Res.sheep,Res.wheat,Res.ore])
		
	def playdev(self,devc,knightpos=None,knighttarget=None,hakkres=None,roadspots=[],monres=None):
		if devc in self.devcards:
			devcards.remove(devc)
		else:
			return False
		if devc == Devs.knight:
			self.gboard.moveKnight(knightpos,pnum,knighttarget)
			self.knights += 1
		if devc == Devs.hakken:
			self.hand.append[hakkres[0],hakkres[1]]
		if devc == Devs.monopoly:
			self.gboard.monSteal(monres)
		if devc == Devs.roadbuild:
			self.gboard.buildRoad[roadspots[0]]
			self.gboard.buildRoad[roadspots[1]]
		if devc == Devs.vp:
			self.vp += 1

	def init_draw(self):
		for settle in self.settles:
			for pair in self.gboard.resadj(settle):
				if self.gboard.resources[pair[0]][pair[1]] < 5:
					self.hand.append(self.gboard.resources[pair[0]][pair[1]])
				
	def respond_to_die(self,dienum):
		for settle in self.settles:
			for pair in self.gboard.resadj(settle):
				if self.gboard.nums[pair[0]][pair[1]] == dienum and self.gboard.robberspot != pair and self.gboard.resources[pair[0]][pair[1]] < 5:
					self.hand.append(self.gboard.resources[pair[0]][pair[1]])
					print str(self.playernum) + " draws a " + str(self.gboard.resources[pair[0]][pair[1]]) + ", now " + str(self.hand)


		for settle in self.cities:
			for pair in self.gboard.resadj(settle):
				if self.gboard.nums[pair[0]][pair[1]] == dienum and self.gboard.robberspot != pair:
					self.hand = self.hand + [self.gboard.resources[pair[0]][pair[1]]] + [self.gboard.resources[pair[0]][pair[1]]]
					print str(self.playernum) + " draws two " + str(self.gboard.nums[pair[0]][pair[1]]) + ", now " + str(self.hand)

					
	def generate_moves(self):
				# road    #settle  #city    #draw dev   # play dev #trade bank # player trade
		moves = {"r": [], "s": [], "c": [], "d": [], "p": [], "t": [], "l": []}
		if self.canafford(Purch.road):
			moves["r"] = self.get_legalroads()
		if self.canafford(Purch.sett):
			moves["s"] = self.get_legalsettlements()
		if self.canafford(Purch.city):
			moves["c"] = self.get_legalcities()
		if self.canafford(Purch.devc):
			moves["d"] = [1]
		moves["p"] = copy.deepcopy(self.devcards)
		moves["t"] = self.get_trades()
		return moves
		
	def generate_movesUCT(self):
				# road    #settle  #city    #draw dev   # play dev #trade bank # player trade
		moves = []
		if self.canafford(Purch.road):
			x = self.get_legalroads()
			for i in x:
				moves.append(move(self.playernum,x[0],x[1]))
				
		if self.canafford(Purch.sett):
			moves["s"] = self.get_legalsettlements()
		if self.canafford(Purch.city):
			moves["c"] = self.get_legalcities()
		if self.canafford(Purch.devc):
			moves["d"] = [1]
		moves["p"] = copy.deepcopy(self.devcards)
		moves["t"] = self.get_trades()
		movfinal = []
		for i in moves:
			for j in moves[i]:
				movfinal += (i + str(moves[j]) 
		return movfinal
	
	
	def get_legalroads(self):
		poss = []
		for vertex in set(self.settles + self.cities + [tex for road in self.roads for tex in road]):
			for adjposs in self.gboard.vertexadj(vertex):
				if self.gboard.roadlegal(self.playernum,vertex,adjposs):
					poss.append([vertex,adjposs])
		print lol2set(poss)
		return lol2set(poss)
		
	def get_legalcities(self):
		return copy.deepcopy(self.settles)
		
	def get_legalsettlements(self,init=False):
		if init:
			return [v for v in xrange(len(self.gboard.vertices)) if v != 0 and self.gboard.settlementlegal(self.playernum,v,init=True)]
		else:
			poss = []
			for vertex in set([tex for road in self.roads for tex in road]):
				if self.gboard.settlementlegal(self.playernum,vertex):
					print "LEGA"
					poss.append(vertex)
			return list(set(poss))
		
	def get_trades(self):
		default = 4
		if (self.trades["three"]):
			default = 3
		trades = [default] * 5
		if (self.trades["sheep"]):
			trades[0] = 2
		if (self.trades["wheat"]):
			trades[1] = 2
		if (self.trades["log"]):
			trades[2] = 2
		if (self.trades["brick"]):
			trades[3] = 2
		if (self.trades["ore"]):
			trades[4] = 2
		return [self.hand.count(i) / trades[i] for i in xrange(0,5)]
		
	def discard_half(self):
		for i in xrange(int(len(self.hand) / 2)):
			self.hand.remove(random.choice(self.hand))
	
	def selectRobber(self):
		target = random.choice([x for x in range(4) if x != self.playernum])
		spot = random.choice(self.gboard.getresourcespots(target))
		print "targeting " + str(target) + " at " + str(spot)
		return spot, target
		
	def trade_bank(self,pnum,give,get):
		for card in give:
			self.players[pnum].hand.remove(card)
		self.players[pnum].hand += get
	
	def play_move(self,move):
		if move.type == Moves.city:
			self.place_city(move.spot1)
		if move.type == Moves.settlement:
			self.place_settlement(move.spot1)
		if move.type == Moves.road:
			self.place_road(move.spot1,move.spot2)
		if move.type == Moves.tbank:
			self.trade_bank(move.pnum,move.resgive,move.res.get)
		if move.type == Move.drawdev
			self.players[move.pnum].hand +
		if move.type == Move.playdev:
			self.players[move.pnum].hand.remove(random.choice(self.players[move.pnum].hand))
		
		elif len(moves["s"]) > 0:
			schoice = random.choice(moves["s"])
			self.place_settlement(schoice,init=False)
		elif len(moves["r"]) > 0:
			roadchoice = random.choice(moves["r"])
			self.place_road(roadchoice[0],roadchoice[1],init=False)
		print str(self.playernum) + "'s moves are " + str(moves)
					
	def phase2(self):
		moves = self.generate_moves()
		if len(moves["c"]) > 0:
			cchoice = random.choice(moves["c"])
			self.place_city(cchoice)
		elif len(moves["s"]) > 0:
			schoice = random.choice(moves["s"])
			self.place_settlement(schoice,init=False)
		elif len(moves["r"]) > 0:
			roadchoice = random.choice(moves["r"])
			self.place_road(roadchoice[0],roadchoice[1],init=False)
		print str(self.playernum) + "'s moves are " + str(moves)
		
		
	def random_init(self):
		poss = self.get_legalsettlements(init=True)
		settle = random.choice(list(poss))
		self.place_settlement(settle,True)
		self.place_road(settle,random.choice(self.gboard.vertexadj(settle)),init=True)
		
		

class board():

	def __init__(self):
		self.currentturn = 0
		self.players = []
		self.colors = ['green','yellow','brown','red','gray','black']
		self.playercolors = ['orange','gray','pink','blue']
		self.nums,self.resources,self.robberspot = self.init_board()
		self.vertices = [-1] * 55
		self.connections = {0:[],1:[2,9],2:[1,3],3:[2,4,11],4:[3,5],5:[4,6,13],6:[5,7],7:[6,15], \
		 8:[9,18],9:[1,8,10],10:[9,11,20],11:[3,10,12],12:[11,13,22],13:[5,12,14],14:[13,15,24],15:[7,14,16],16:[15,26],\
		 17:[18,28],18:[8,17,19],19:[18,20,30],20:[10,19,21],21:[20,22,32],22:[12,21,23],23:[22,24,34],24:[14,23,25],25:[24,26,36],26:[16,25,27],27:[26,38],\
		 28:[17,29],29:[28,30,39],30:[19,29,31],31:[30,32,41],32:[21,31,33],33:[32,34,43],34:[23,33,35],35:[34,36,45],36:[25,35,37],37:[36,38,47],38:[27,37],\
		 39:[29,40],40:[39,41,48],41:[31,40,42],42:[41,43,50],43:[33,42,44],44:[43,45,52],45:[35,44,46],46:[45,47,54],47:[37,46],\
		 48:[40,49],49:[48,50],50:[42,49,51],51:[50,52],52:[44,51,53],53:[52,54],54:[46,53]}
		self.roads = copy.deepcopy(self.connections)
		self.harbors = {1:"sheep",2:"sheep",4:"three",5:"three",15:"log",16:"log",27:"ore",38:"ore",46:"brick",47:"brick",52:"three",51:"three",49:"wheat",48:"wheat",39:"three",29:"three",18:"three",8:"three"}
		for i in self.roads:
			for j in xrange(len(self.roads[i])):
				self.roads[i][j] = -1
		self.devdeck = [Devs.hakken] * 2 + [Devs.roadbuild] * 2 + [Devs.monopoly] * 2 + [Devs.knight] * 14 + [Devs.vp] * 5
		random.shuffle(self.devdeck)
		self.draw_board()
	
	def settlementlegal(self,pnum,i,init=False):
		adjs = self.vertexadj(i)
		noadjsetts = (len([v for v in adjs if self.vertices[v] != -1]) == 0)
		neighborroad = (len([j for j in self.connections[i] if self.roads[i][self.connections[i].index(j)] == pnum]) > 0)
		if noadjsetts and self.vertices[i] == -1:
			if init or neighborroad:
				return True
			else:
				return False
				
	def citylegal(self,pnum,i):
		return self.vertices[i] == pnum
				
	def roadlegal(self,pnum,i,j):
		if self.roads[i][self.connections[i].index(j)] != -1:
			return False
		neighborroad = (len([v for v in self.roads[i] + self.roads[j] if v == pnum]) > 0)
		neighborsett = (len([v for v in self.vertexadj(i) + self.vertexadj(j) if self.vertices[v] == pnum]) > 0)
		if neighborroad or neighborsett:
			return True
		else:
			return False
			
	def drawdev(self):
		return self.devdeck.pop()

	def monSteal(self,resource,pnum):
		for pl in [p for p in xrange(0,4) if p != pnum]:
			while resource in self.players[pl].hand:
				self.players[pl].hand.remove(resource)
				self.players[pnum].hand.append(resource)
				
	def moveKnight(self,spot,robber,robbed):
		legit = False
		for v in self.whichvertices(spot):
			if self.vertices[v] == robbed:
				legit = True
		if legit and spot != self.robberspot and len(self.players[robbed].hand) > 0:
			card = random.choice(self.players[robbed].hand)
			self.players[robbed].hand.remove(card)
			self.players[robber].hand.append(card)
			self.robberspot = spot
		
	def addsett(self,pnum,i):
		self.vertices[i] = pnum
		
	def addcity(self,pnum,i):
		self.vertices[i] = 10*(pnum+1)
		
	def addroad(self,pnum,i,j):
		self.roads[i][self.connections[i].index(j)] = pnum
		self.roads[j][self.connections[j].index(i)] = pnum
		
	# get all settlement vertices for particular player
	def getsetts(self,pnum):
		return [i for i in xrange(len(self.vertices)) if self.vertices[i] == pnum]
	
	def getcities(self,pnum):
		return [i for i in xrange(len(self.vertices)) if self.vertices[i] == (pnum+1)*10]
			
	# returns all the resource spots an opponent can draw from
	def getresourcespots(self,pnum):
		setts = self.getsetts(pnum)
		cities = self.getcities(pnum)
		res = []
		for sett in setts:
			print self.resadj(sett)
			res = res + self.resadj(sett)
		for city in cities:
			res = res + self.resadj(city) + self.resadj(city)
		return res
				
	# returns vertices adjacent to this vertex
	def vertexadj(self,i):
		return self.connections[i]
		 
	# returns resources adjacent to this vertex
	def resadj(self,i):
		reslist = []
		if i in [1,2,3,9,10,11]:
			reslist.append([0,0])
		if i in [3,4,5,11,12,13]:
			reslist.append([0,1])
		if i in [5,6,7,13,14,15]:
			reslist.append([0,2])
		if i in [8,9,10,18,19,20]:
			reslist.append([1,0])
		if i in [10,11,12,20,21,22]:
			reslist.append([1,1])
		if i in [12,13,14,22,23,24]:
			reslist.append([1,2])
		if i in [14,15,16,24,25,26]:
			reslist.append([1,3])
		if i in [17,18,19,28,29,30]:
			reslist.append([2,0])
		if i in [19,20,21,30,31,32]:
			reslist.append([2,1])
		if i in [21,22,23,32,33,34]:
			reslist.append([2,2])
		if i in [23,24,25,34,35,36]:
			reslist.append([2,3])
		if i in [25,26,27,36,37,38]:
			reslist.append([2,4])
		if i in [29,30,31,39,40,41]:
			reslist.append([3,0])
		if i in [31,32,33,41,42,43]:
			reslist.append([3,1])
		if i in [33,34,35,43,44,45]:
			reslist.append([3,2])
		if i in [35,36,37,45,46,47]:
			reslist.append([3,3])
		if i in [40,41,42,48,49,50]:
			reslist.append([4,0])
		if i in [42,43,44,50,51,52]:
			reslist.append([4,1])
		if i in [44,45,46,52,53,54]:
			reslist.append([4,2])
		return reslist
	
	# returns vertices adjacent to a resource
	def whichvertices(self,gridspot):
		print "Checking adjacent vertices to " + str(gridspot)
		if (gridspot == [0,0]):
			return [1,2,3,9,10,11]
		if (gridspot == [0,1]):
			return[3,4,5,11,12,13]
		if (gridspot == [0,2]):
			return [5,6,7,13,14,15]
		if (gridspot == [1,0]):
			return [8,9,10,18,19,20]
		if (gridspot == [1,1]):
			return [10,11,12,20,21,22]
		if (gridspot == [1,2]):
			return [12,13,14,22,23,24]
		if (gridspot == [1,3]):
			return [14,15,16,24,25,26]
		
		if gridspot == [2,0]:
			return [17,18,19,28,29,30]
		if gridspot == [2,1]:
			return [19,20,21,30,31,32]
		if gridspot == [2,2]:
			return [21,22,23,32,33,34]
		if gridspot == [2,3]:
			return [23,24,25,34,35,36]
		if gridspot == [2,4]:
			return [25,26,27,36,37,38]
			
		if gridspot == [3,0]:
			return [29,30,31,39,40,41]
		if gridspot == [3,1]:
			return [31,32,33,41,42,43]
		if gridspot == [3,2]:
			return [33,34,35,43,44,45]
		if gridspot == [3,3]:
			return [35,36,37,45,46,47]
		if gridspot == [4,0]:
			return [40,41,42,48,49,50]
		if gridspot == [4,1]:
			return [42,43,44,50,51,52]
		if gridspot == [4,2]:
			return [44,45,46,52,53,54]
			
	def init_board(self):
		seq = [2,3,3,4,4,5,5,6,6,0,8,8,9,9,10,10,11,11,12]
		random.shuffle(seq)
		
		self.window = Tkinter.Tk()
		# sheep wheat log brick ore
		seqres = [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,4,4,4]
		random.shuffle(seqres)
		robberspot = [-1,-1]
		seq2 = [[-1 for col in range(5)] for row in range(5)]
		res2 = [[-1 for col in range(5)] for row in range(5)]
		deserted = False
		for i in range(len(seq)):
			coords = squareize(i)
			if seq[i] == 0:
				robberspot = [coords[0],coords[1]]
				seq2[coords[0]][coords[1]] = 0
				res2[coords[0]][coords[1]] = 5
				deserted = True
			else:
				seq2[coords[0]][coords[1]] = seq[i]
				res2[coords[0]][coords[1]] = seqres[i -deserted]
		return seq2,res2,robberspot
		
	def vertextocoord(self,i):
		if (i % 2 == 0):
			if (i > 0 and i < 8):
				return [126+67*(i/2-1),80]
			if (i < 18):
				return [119+67*(i/2-5),150]
			if (i < 28):
				return [60 + 67*(i/2-9),208]
			if (i < 40):
				return [85+67*(i/2-15),264]
			if (i < 48):
				return [85+67*(i/2-20),340]
			return [85+67*(i/2-24),400]
		if (i % 2 == 1):
			if (i > 0 and i < 8):
				return [92+67*(i/2),100]
			if (i < 16):
				return [92+67*(i/2-4),138]
			if (i < 28):
 				return [33+60 + 67*(i/2-9),224]
			if (i < 38):
				return [33+85+67*(i/2-15),280]
			if (i < 48):
				return [33+85+67*(i/2-20),324]
			return [33+85+67*(i/2-24),410]
		return [0,0]
		
	def do_turn(self,pnum):
		dice = random.randint(1,6) + random.randint(1,6)
		print str(pnum) + " rolled a " + str(dice)
		if dice == 7:
			for player in self.players:
				if len(player.hand) > 7:
					player.discard_half()
			position, robbed = self.players[pnum].selectRobber()
			self.moveKnight(position,pnum,robbed)
		else:
			for player in self.players:
				player.respond_to_die(dice)
				# trade
		self.players[pnum].phase2()
		
	def play_turns(self,n):
		for i in xrange(n):
			self.do_turn(self.currentturn)
			self.currentturn = (self.currentturn + 1) % 4
			#if self.currentturn == 0:
				#self.print_state()
		
	def init_game(self):
		for i in xrange(4):
			self.players[i].random_init()
		for i in range(3,-1,-1):
			self.players[i].random_init()
		for i in xrange(4):
			self.players[i].init_draw()
	
	def print_state(self):
		for player in self.players:
			print player.playernum;
			print "Hand: " + str(player.hand)
			print "Devcards: " + str(player.devcards)
			print "Settlements: " + str(player.settles)
			print "Cities: " + str(player.cities)
			print "Roads: " + str(player.roads)
			print "Trades: " + str(player.trades)
			
	def state(self):
		s = ""
		for player in self.players:
			s += "Player " + str(player.playernum) + ":\n"
			s += "Hand: " + str(player.hand) + "\n"
			s += "Devcards: " + str(player.devcards) + "\n"
			s += "Settlements: " + str(player.settles) + "\n"
			s += "Cities: " + str(player.cities)+ "\n"
			s += "Roads: " + str(player.roads)+ "\n"
			s += "Trades: " + str(player.trades)+ "\n"
			s += "\n"
		return s
		
	def draw_board(self):
		for i in range(0,5):
			for j in range(0,5 - abs(2 - i)): 
				hexanchor = (abs(2-i) *33 + 60 + j * 67, 80 + i * 64)
				hexagon = hexagon_generator(40, offset=hexanchor,rotation=30)
				w.create_polygon(list(hexagon), outline='black', fill=self.colors[self.resources[i][j]])
				w.create_oval((hexanchor[0] -10, hexanchor[1] + 30,hexanchor[0] + 10,hexanchor[1]+50), fill='white')
				w.create_text((hexanchor[0] -7, hexanchor[1]+35), text=str(self.nums[i][j]), fill='black')
		for i in xrange(len(self.vertices)):
			ans = self.vertextocoord(i)
			if self.vertices[i] > -1 and self.vertices[i] < 10:
				w.create_oval((ans[0]-5,ans[1]-5,ans[0]+5,ans[1]+5), fill=self.playercolors[self.vertices[i]])
			if self.vertices[i] >= 10 and self.vertices[i] < 100:
				w.create_oval((ans[0]-10,ans[1]-10,ans[0]+10,ans[1]+10), fill=self.playercolors[self.vertices[i]/10 - 1])
			for j in self.connections[i]:
				ans2 = self.vertextocoord(j)
				if self.roads[i][self.connections[i].index(j)] > -1 and  self.roads[i][self.connections[i].index(j)] < 10:
					w.create_line((ans[0], ans[1], ans2[0],ans2[1]), fill=self.playercolors[self.roads[i][self.connections[i].index(j)]])
			w.create_text((ans[0],ans[1]),text=str(i),fill='black')
		#w.after(100,self.draw_board)
		
		

		
def squareize(i):
	if i < 3:
		return (0,i)
	elif i < 7:
		return (1,i-3)
	elif i < 12:
		return (2,i-7)
	elif i < 16:
		return (3,i-12)
	else:
		return (4,i-16)
	
def hexagon_generator(edge_length, offset,rotation):
  """Generator for coordinates in a hexagon."""
  x, y = offset
  for angle in range(0, 360, 60):
    x += math.cos(math.radians(angle+rotation)) * edge_length
    y += math.sin(math.radians(angle+rotation)) * edge_length
    yield x, y
  
