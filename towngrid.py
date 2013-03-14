#!/usr/bin/env python
# -- Custom Helpers:
from helpers.pygamehelper import *
from helpers.newcursor import *
from helpers.simplequeue import *
#from helpers.sprite_stuff import *
# -- 'Official' modules:
from pygame import *
from pygame.locals import *
from random import randint,uniform
from os import path
import sys

class GameConsts:	
	#--Files
	imageFolder = "images"
	#--Interface--
	tileWidth = 32
	tileHeight = 32
	tilePadding = 0	
	scrollSpeed	= 8
	aniFreq = 10 #amount of ticks betweem changing of sprite frames
	#--GamePlay--
	maxDistance = 6
	startYear = 1950
	daysPerMonth = 10
	initialBudget = 1500			
	
# Tile Types
class TileType:
	grass = 0
	water = 1
	road = 2
	building = 3
	decoration = 4	
	typestring = ["Grass","Water","Road","Building","Decoration"]
	
# Directions
class Direction:
	north = 0
	east = 1
	south = 2
	west = 3
	opposite = [2,3,0,1]

def loadSprite(fileName):
	try:
		return pygame.image.load(path.join(GameConsts.imageFolder,fileName))
	except:
		raise("Could not load image from file: %s"%fileName)				
		
def rotate90(sprite):
	return pygame.transform.rotate(sprite,-90)

class SpriteMatrix:
	def __init__(self,images):
		self.imageWidth = images[0].get_width()
		self.imageHeight = images[0].get_height()
		self.tilesX = self.imageWidth // GameConsts.tileWidth
		self.tilesY = self.imageHeight // GameConsts.tileHeight				
		self.matrix = [[TileSprite([]) for i in range(self.imageWidth // GameConsts.tileWidth)] for j in range(self.imageHeight // GameConsts.tileHeight)]
		for i in range(len(images)):
			w = images[i].get_width()
			h = images[i].get_height()
			if w == self.imageWidth:
				if h == self.imageHeight:
					if w % GameConsts.tileWidth == 0 and h % GameConsts.tileHeight == 0:
						tw = w // GameConsts.tileWidth
						th = h // GameConsts.tileHeight
						for row in range(th):
							for col in range(tw):
								newImage = pygame.Surface((GameConsts.tileWidth,GameConsts.tileHeight))								
								newImage.blit(images[i],(0,0),(col * GameConsts.tileWidth,row * GameConsts.tileHeight,GameConsts.tileWidth,GameConsts.tileHeight))
								self.matrix[row][col].addFrame(newImage)
						print "SpriteMatrix received image of %d x %d tiles"%(tw,th)		
					else:
						raise("Image width AND height must be divisable by the respective tile dimensions.")	 
				else:
					self.wrongDimensionError()	
			else:
				self.wrongDimensionError()	
				
	def animate(self):
		for i in range(self.tilesY):
			for j in range(self.tilesX):
				self.matrix[i][j].animate()
		
	def getTileSpriteAt(self,x,y):
		return self.matrix[y][x]
		
	def wrongDimensionError(self):
		raise("Consquent images in SpriteMatrix must have similar dimensions.")					
	
class TileSprite:
	def __init__(self,images):				
		if len(images) == 0:
			pass
			#raise("You can't initialize a sprite without image(s).")
		self.frameList = []
		for i in images:
			self.frameList.append(i)
		self.lastFrame = len(self.frameList) - 1
		self.frameIndex = 0
		
	def addFrame(self, image):		
		self.frameList.append(image)
		self.lastFrame = len(self.frameList) - 1
		
	def getFrame(self):
		return self.frameList[self.frameIndex]
		
	def animate(self):
		self.frameIndex += 1
		if self.frameIndex > self.lastFrame:
			self.frameIndex = 0	 		
			
class Sprites:
	#tiles = [	pygame.image.load(), \
				#pygame.image.load(), \
				#pygame.image.load("images/tile_road.gif"), \
				#pygame.image.load()]
	
	#button sprites
	button_select = loadSprite("button_select.gif")
	button_build = loadSprite("button_troffel.gif")
	button_destroy = loadSprite("button_tnt.gif")
	button_return = loadSprite("button_return.gif")
	button_house = loadSprite("button_house.gif")
	button_road = loadSprite("button_road.gif")
	button_business = loadSprite("button_business.gif")			
	button_park = loadSprite("button_park.gif")
	#interface sprites
	interface_bkgd = pygame.image.load("images/interface_backgd3.gif")			


tileSprites={	
	'base_grass' : TileSprite([loadSprite("tile_dirt.gif")]),
	'base_water' : TileSprite([	loadSprite("tile_water_ani2_1.gif"),\
								loadSprite("tile_water_ani2_2.gif"),\
								loadSprite("tile_water_ani2_3.gif"),\
								loadSprite("tile_water_ani2_4.gif")]),
	'building_house' : TileSprite([loadSprite("tile_house.gif")]),
	'building_house_bad' : TileSprite([loadSprite("tile_house_bad.gif")]),
	'building_house_abandon' : TileSprite([loadSprite("tile_house_abandon.gif")]),
	'building_house_condemned' : TileSprite([loadSprite("tile_house_condemned.gif")]),
	'building_business' : SpriteMatrix([loadSprite("store_w64.gif")]),
	'building_park' : TileSprite([	loadSprite("tile_park_f1.gif"),\
									loadSprite("tile_park_f2.gif")])}
	#'building_construction' : None}

#road sprites	
tempSprite = loadSprite("tiles_road_cont.gif")		
tileSprites['road_NS'] = TileSprite([tempSprite])
tileSprites['road_EW'] = TileSprite([rotate90(tempSprite)])

tempSprite = loadSprite("tiles_road_bridge.gif")	
tileSprites['road_bridge_EW'] = TileSprite([tempSprite])
tileSprites['road_bridge_NS'] = TileSprite([rotate90(tempSprite)])

tempSprite = loadSprite("tiles_road_corner.gif")	
tileSprites['road_corner_ES'] = TileSprite([tempSprite])
tileSprites['road_corner_SW'] = TileSprite([rotate90(tileSprites['road_corner_ES'].getFrame())])
tileSprites['road_corner_NW'] = TileSprite([rotate90(tileSprites['road_corner_SW'].getFrame())])
tileSprites['road_corner_NE'] = TileSprite([rotate90(tileSprites['road_corner_NW'].getFrame())])
	
tempSprite = loadSprite("tiles_road_t_junct.gif")	
tileSprites['road_tjunct_NSW'] = TileSprite([tempSprite])
tileSprites['road_tjunct_NEW'] = TileSprite([rotate90(tileSprites['road_tjunct_NSW'].getFrame())])
tileSprites['road_tjunct_NES'] = TileSprite([rotate90(tileSprites['road_tjunct_NEW'].getFrame())])
tileSprites['road_tjunct_ESW'] = TileSprite([rotate90(tileSprites['road_tjunct_NES'].getFrame())])
	
tempSprite = loadSprite("tiles_road_dead.gif")	
tileSprites['road_dead_N'] = TileSprite([tempSprite])
tileSprites['road_dead_E'] = TileSprite([rotate90(tileSprites['road_dead_N'].getFrame())])
tileSprites['road_dead_S'] = TileSprite([rotate90(tileSprites['road_dead_E'].getFrame())])
tileSprites['road_dead_W'] = TileSprite([rotate90(tileSprites['road_dead_S'].getFrame())])
	
tileSprites['road_lone'] = TileSprite([loadSprite("tiles_road_lone.gif")])
tileSprites['road_xing'] = TileSprite([loadSprite("tiles_road_xing.gif")])
	
tileSprites['deco_statue'] = TileSprite([loadSprite("tiles_statue_f1.gif"),loadSprite("tiles_statue_f2.gif")])

# -- Constants for construction and town finance:
maintenanceCosts = {	
	'road' : 2, 
	'bridge' : 10,
	'decoration' : 5,
	'park' : 3,
	'community_building_church' : 50,
	'community_building_police' : 150,
	'community_building_hospital' : 200}
	
constructionCosts = {
	'road' : 5,
	'house' : 50,
	'business' : 150,  
	'park' : 10}
	
baseTaxRevenue = {
	'house' : 10,
	'business' : 30}
	
objectDimensions = {
	'road' : (1,1),
	'house' : (1,1),
	'business' : (2, 1),
	'park' : (1,1)}
				
class ActionType:
	changeMode = 0
	enterMenu = 1
	setTool = 2
	
class Tool:	
	build_road = 0
	build_house = 1
	build_business = 2
	build_park = 3
	
class CursorMode:
	select = 0
	destroy = 1	
	build = 2
	
class BuildingState:	
	construction = 0
	normal = 1
	decay = 2
	abandoned = 3
	condemned = 4
	strings = ("Under construction.","Fine.","In decay.","Abandoned.","Condemned (not habitable).")
	
class OccupantType:
	road = 0
	building = 1
	#park = 2
	decoration = 2
	
class BuildingType:
	house = 0
	business = 1
	park = 2
	community = 3
	strings = ["House","Store","Park"]
	
class HouseType:
	ordinary = 0

class BusinessType:
	small_shop = 0
	
familyLastNames = (	"Johnson","McAlister","Williams","Sims","Deaver","Rhyme","Griswold","Simpson","Flintstone","Jetson","Griffin","Burton","O'Reilly", \
					"Clark","Figgins","Robbins","Hanson","Clinton","Bush","Smith","Watterson","Barks")	
businessNames = ("Hardware","Grocery","Clothing","Vegetable","Computer","Toys","Electronics","Candy","Book","Game")

class ButtonAction:
	def __init__(self,actionType,value):
		self.type = actionType
		self.value = value
		  
class Button:
	def __init__(self,image,id,action=None):
		self.image = image
		self.pos = (0,0)
		self.id = id
		self.action = action
		
	def clicked(self,cursorpos):
		if MouseInRect(cursorpos, (self.pos[0], self.pos[1], 32, 32)):
			return True
		return False
		
class MenuType:
	build=0
	default=1
	
class Menu:
	buttons = []
	#Build Menu
	buttons.append([	Button(Sprites.button_return,3,ButtonAction(ActionType.enterMenu,MenuType.default)), \
						Button(Sprites.button_road,4,ButtonAction(ActionType.setTool,Tool.build_road)), \
						Button(Sprites.button_house,5,ButtonAction(ActionType.setTool,Tool.build_house)), \
						Button(Sprites.button_business,6,ButtonAction(ActionType.setTool,Tool.build_business)), \
						Button(Sprites.button_park,7,ButtonAction(ActionType.setTool,Tool.build_park))])
	#Main Menu					
	buttons.append([	Button(Sprites.button_select,0,ButtonAction(ActionType.changeMode,CursorMode.select)), \
						Button(Sprites.button_build,1,ButtonAction(ActionType.enterMenu,MenuType.build)), \
						Button(Sprites.button_destroy,2,ButtonAction(ActionType.changeMode,CursorMode.destroy))])	

#-- classes										
class Town:	
	def __init__(self,width,height):
		self.houses = []
		self.roads = []
		self.businesses = []
		self.parks = []
		self.balance = GameConsts.initialBudget
		self.clock = GameClock(self)
		self.grid = TileGrid(self,width,height)
	
	def addObject(self,obj):
		if obj.type == OccupantType.road:
			self.roads.append(obj)
		elif obj.type == OccupantType.building:
			if obj.buildingType == BuildingType.house:
				self.houses.append(obj)
			elif obj.buildingType == BuildingType.business:
				self.businesses.append(obj)
			elif obj.buildingType == BuildingType.park:
				self.parks.append(obj)
			else:
				raise("Unknown building type")	
		else:
			raise("Unknown occupant type")				
			
	def canSpend(self,ammount):
		if (self.balance - ammount) >= 0:
			return True
		return False	
	
	def spendMoney(self,ammount):
		if (self.balance - ammount) >= 0:
			self.balance -= ammount
			return True
		return False	
		
	def collectTaxes(self):
		collected = 0
		for r in self.houses:
			collected += r.collectTaxes()
		for b in self.businesses:
			collected += b.collectTaxes()
		return collected
		
	def calculateExpenditures(self):
		roadCosts = len(self.roads) * maintenanceCosts['road']
		parkCosts = len(self.parks) * maintenanceCosts['park']
		return (roadCosts + parkCosts)
		
	def budget(self):
		income = self.collectTaxes()						
		spendings = self.calculateExpenditures()
		surplus = (income - spendings)
		self.balance += surplus
						
	def	findJobs(self, month):
		newEmployments = 0
		jobless = 0
		households = 0.0 + len(self.houses)
		#print "try to find jobs for %d houses"%len(self.houses)
		for r in self.houses:
			if r.existant:			
				if r.habitable:
					nearbyBuildings = r.getConnectedBuildings()
					if not r.employed:
						#print "%d nearby buildings."%len(nearbyBuildings)			
						jobFound = False
						for b in nearbyBuildings:
							if b.buildingType == BuildingType.business:
								#print "business found!"
								if b.hire():
									newEmployments += 1
									r.employAt(b)
									jobFound = True
									break
						if not jobFound:
							r.noJob()
							jobless += 1							
					else:
						r.hasJob()					
					if month % 3 == 0:
						self.scoreNeighborhood(r,nearbyBuildings)
			else:
				if r.employed:
					r.workPlace.lostEmployee()
				self.houses.pop(self.houses.index(r))
		print "Found work for %d households."%newEmployments
		if households > 0:
			print "Unemployment: %d"%((jobless / households) * 100)+"%"
	
	def handleBusinessDemands(self):
		for b in self.businesses:
			if b.existant:				
				nearbyBuildings = b.getConnectedBuildings()
				nearbyHouses = []
				customers = 0
				for bu in nearbyBuildings:
					if bu.buildingType == BuildingType.house:
						if bu.state < BuildingState.abandoned:
							customers += 1
						nearbyHouses.append(bu)						
				b.adaptLaborDemand(nearbyHouses,customers)							
			else:
				print "found removed business"
				for h in self.houses:
					if h.employed:						
						if h.workPlace == b:
							print "this guy worked here."
							h.terminateEmployment()
				self.businesses.pop(self.businesses.index(b))						
			
	def findShops(self):
		pass	
		
	def scoreNeighborhood(self,house,nearbyHouses):			
		pass
		
	def getDateString(self):
		return self.clock.getDateString() 
			
class GameClock:
	def __init__(self,town):
		self.pause = False
		self.gameSecs = 0
		self.gameDays = 0
		self.gameMonths = 0
		self.gameYears = GameConsts.startYear
		self.myTown = town
		self.monthNames = ("JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC")
				
	def pause(self):
		if not self.pause:
			self.pause = True
	
	def unPause(self):
		if self.pause:
			self.pause = False
			
	def getMonthsSince(self,dateTuple):
		return (self.gameYears - dateTuple[0]) * 12 + (self.gameMonths - dateTuple[1])
					
	def tick(self):		
		self.gameDays += 1
		if self.gameDays > GameConsts.daysPerMonth:
			self.gameDays = 0
			self.gameMonths += 1
			#monthlyStuff
			self.myTown.findJobs(self.gameMonths)
			self.myTown.handleBusinessDemands()
			if self.gameMonths > 11:
				self.gameMonths = 0
				self.gameYears += 1
				self.myTown.budget()
				
	def getDateString(self):
		return "%s %d"%(self.monthNames[self.gameMonths],self.gameYears)		
					
class TileGrid:
	def __init__(self, town, width=10, height=10, originX=0, originY=0):
		self.height = height
		self.width = width
		self.tiles = []
		self.pixelHeight = self.height * (GameConsts.tileHeight + GameConsts.tilePadding)
		self.pixelWidth = self.width * (GameConsts.tileWidth + GameConsts.tilePadding)
		self.origin = originX, originY 
		self.gridImg = pygame.Surface((self.pixelWidth,self.pixelHeight))
		self.highlighted = None
		self.myTown = town
		self.generate()
		self.refresh()
		
	def generateRiver(self):
		#generate river
		riverX = (self.width / 2)				
		prob_l = randint(1,7) 
		prob_r = prob_l + (8 - prob_l)		
		for i in range(self.height):
			randomNr = randint(1,10)			
			if randomNr <= prob_l:
				riverX -= 1
			elif randomNr <= prob_r:
				riverX += 1
			if riverX >= 0 and riverX < self.width:
				tileNr = (i*self.width) + riverX
				t1 = self.tiles[tileNr]
				t1.changeType(TileType.water)
				if riverX < (self.width - 1):
					t2 = self.tiles[tileNr + 1]
					t2.changeType(TileType.water)
		
	def placeStatue(self):
		#Place statue at center:
		centerX = self.width / 2
		centerY = self.height / 2
		tileNr = (centerY * self.width) + centerX
		while self.tiles[tileNr].type != TileType.grass:
			tileNr -= 1
		self.tiles[tileNr].changeType(TileType.decoration)	
		
		
	def generate(self):
		t = 0
		#fill with standard tiles
		for i in range(self.height):
			for j in range(self.width):
				x = self.origin[0] + j * GameConsts.tileWidth
				y = self.origin[1] + i * GameConsts.tileHeight				
				newTile = Tile(t,GameTileData(x, y, tileSprites['base_grass']),TileType.grass)
				self.tiles.append(newTile)
				if j > 0:	
					self.tiles[t-1].addNeighbor(Direction.east,newTile)
					if j < (self.width - 1):
						newTile.addNeighbor(Direction.west,self.tiles[t-1])
				if i > 0:
					self.tiles[t-self.width].addNeighbor(Direction.south,newTile)
					if i < (self.height - 1):
						newTile.addNeighbor(Direction.north,self.tiles[t-self.width])					
				t += 1
		
		self.generateRiver()
		self.placeStatue()		
					
	def blitTile(self, t):
		spriteX = t.gameData.coords[0]
		spriteY = t.gameData.coords[1]
		self.gridImg.blit(t.gameData.sprite.getFrame(),(spriteX,spriteY))
			
	def refresh(self):		
		for t in self.tiles:
			self.blitTile(t)
		
	def getTileFromCoords(self,pos):
		#print pos
		x = pos[0] // GameConsts.tileWidth
		y = pos[1] // GameConsts.tileHeight
		if x >= 0 and x < self.width and y >= 0 and y < self.height:
			return self.tiles[(y*self.width) + x]
		return None
		
	def highlightTile(self,pos):		
		if self.highlighted != None:
			self.blitTile(self.highlighted)
		t = self.getTileFromCoords(pos)
		if t != None:
			r = (t.gameData.coords[0],t.gameData.coords[1],GameConsts.tileWidth,GameConsts.tileHeight)
			pygame.draw.rect(self.gridImg,(255,0,0),r,1)
			self.highlighted = t
						
	def actOnTile(self,id,toolTuple):
		mode = toolTuple[0]
		subMode = toolTuple[1]
		if id >= 0 and id < len(self.tiles):	
			if mode == CursorMode.destroy:
				t = self.tiles[id]								
				if t.occupant != None:					
					tiles = t.occupant.getTiles()
					t.occupant.destroy()
					#if t.clear():
					for ti in tiles:
						self.blitTile(ti)
					self.refresh()
					return True
			elif mode == CursorMode.build:
				t = self.tiles[id]
				return self.constructObj(t,subMode)
		else:		
			raise("Wrong tile ID supplied to TileGrid.")
		return False
		
	def constructObj(self,tile,buildMode):		
		if buildMode == Tool.build_road:
			if self.myTown.canSpend(constructionCosts['road']):
				r = Road(tile)
				if self.constructOnTile(r, tile, objectDimensions['road']):
					self.myTown.spendMoney(constructionCosts['road'])
					return True
		elif buildMode == Tool.build_house:
			if self.myTown.canSpend(constructionCosts['house']):
				h = House(tile)
				if self.constructOnTile(h, tile, objectDimensions['house']):
					self.myTown.spendMoney(constructionCosts['house'])
					return True
		elif buildMode == Tool.build_business:
			if self.myTown.canSpend(constructionCosts['business']):
				b = Business(tile)
				if self.constructOnTile(b, tile, objectDimensions['business']):
					self.myTown.spendMoney(constructionCosts['business'])
					return True		
		elif buildMode == Tool.build_park:
			if self.myTown.canSpend(constructionCosts['park']):
				p = Park(tile)
				if self.constructOnTile(p, tile, objectDimensions['park']):
					self.myTown.spendMoney(constructionCosts['park'])
					return True
		return False	
	
	def constructOnTile(self, obj, tile, objDim):
		if tile.isBuildable(obj.type, objDim[0], objDim[1]):
			obj.newConstruct()
			self.myTown.addObject(obj)
			self.refresh()
			return True					
		return False
		
	def animateTileSprites(self):
		for s in tileSprites.keys():
			tileSprites[s].animate()
		self.refresh()	
					
				
class GameTileData:
	def __init__(self, x, y, sprite):
		self.coords = x,y
		self.sprite = sprite
		self.baseSprite = sprite
		
	def changeSprite(self,newSprite):
		self.sprite = newSprite
	
	def revertSprite(self):
		self.sprite = self.baseSprite

class Tile:
	def __init__(self, id, gameData, type=TileType.grass):
		self.id = id
		self.neighbors = [None,None,None,None]
		self.type = type
		self.gameData = gameData
		self.vacant = True
		self.occupant = None
		self.baseType = TileType.grass
					
	def addNeighbor(self, direction, neighbor):
		self.neighbors[direction] = neighbor
	
	def removeNeighbor(self, direction):
		self.neighbors[direction] = None
		
	def clear(self):		
		if self.occupant != None:
			#if self.type == TileType.road:
			#	self.occupant.destroy()
			#elif self.type == TileType.building:
			#	self.occupant.destroy()					
			self.type = self.baseType	
			self.gameData.revertSprite()						
			self.occupant = None			
			self.vacant = True
			return True
		return False	
		
	def buildOpon(self,newType,occupant):
		self.type = newType
		self.occupant = occupant		
		
	def changeType(self,newType):
		if newType == TileType.water:
			self.gameData.sprite = tileSprites['base_water']
			self.gameData.baseSprite = tileSprites['base_water']
		elif newType == TileType.grass:
			self.gameData.sprite = tileSprites['base_grass']
			self.gameData.baseSprite = tileSprites['base_grass']
		elif newType == TileType.decoration:
			self.gameData.sprite = tileSprites['deco_statue']	
		else:
			raise "Unknown TileType"
		self.type = newType
		
	def getInfoString(self):		
		if self.occupant != None:
			return self.occupant.getInfoString()
		return "%s on tile #%d"%(TileType.typestring[self.type],self.id)
		
	def debugInfo(self):
		print "========="
		print "Tile ID: %d"%self.id
		print "Tile Type: %s"%TileType.typestring[self.type]
		print "Neighbors: "
		for dir in range(4):
			if self.neighbors[dir] == None:
				print "N%d: None"%dir
			else:
				print "N%d: %d"%(dir,self.neighbors[dir].id)	  
		if self.occupant != None:
			if self.occupant.type == OccupantType.road:
				self.occupant.debugInfo()
			elif self.occupant.type == OccupantType.building:
				self.occupant.debugInfo()
				
	def isBuildable(self,occType,tilesX,tilesY):
		if self.occupant == None:
			if occType == OccupantType.road:
				if self.type == TileType.water or self.type == TileType.grass:
					return True
			elif occType == OccupantType.building:				
				curTile = self
				firstCol = curTile
				for i in range(tilesY):					
					for j in range(tilesX):
						if curTile != None:
							if curTile.type != TileType.grass or curTile.occupant != None:
								return False
						else:
							return False
						curTile = curTile.neighbors[Direction.east]
					firstCol = firstCol.neighbors[Direction.south]
					curTile = firstCol			
			return True																									
		return False					
		
class TileOccupant:
	def __init__(self,tile,type,width=1,height=1):		
		self.height = height
		self.width = width
		self.tile = tile #upperleft corner
		self.tiles = []		
		firstInCol = self.tile
		thisTile = self.tile
		for i in range(self.height):			
			for j in range(self.width):				
				self.tiles.append(thisTile)
				thisTile = thisTile.neighbors[Direction.east]			
			firstInCol = firstInCol.neighbors[Direction.south]
			thisTile = firstInCol		
		self.type = type
		self.existant = True
		
	def changeSprite(self,newSprite):		
		self.tile.gameData.sprite = newSprite
		
	def newChangeSprite(self,newSprite):
		t = 0
		for i in range(self.height):
			for j in range(self.width):
				self.tiles[t].gameData.sprite = newSprite.getTileSpriteAt(j,i)
				t += 1	
		
	def construct(self):		
		raise("Call to unimplemented .construct() of TileOccupant.")
		
	def destroy(self):
		self.existant = False
		for t in self.tiles:
			t.clear()
		#raise("Call to unimplemented .destroy(). TileOccupant just containts a stub of this method!")
		
	def getTiles(self):
		return self.tiles
		
	def debugInfo(self):
		raise("Call to unimplemented .debugInfo() of TileOccupant.")
		
	def getInfoString(self):
		return "Some object occupying a tile... duh"
		
	def getTextLines(self):
		raise("Call to unimplemented .getTextLines() of TileOccupant.")				
	
class BuildingObject(TileOccupant):
	def __init__(self,tile,buildingType):
		self.state = BuildingState.normal
		self.buildingType = buildingType
		w = 1
		h = 1
		if self.buildingType == BuildingType.business:
			w = 2
			h = 1
		TileOccupant.__init__(self,tile,OccupantType.building,w,h)
		#self.roadConnections = [None,None,None,None]
		self.roadConnections = []
		#self.state = False
		
	def construct(self):
		self.tile.buildOpon(TileType.building,self)
		n = self.tile.neighbors
		for dir in range(4):			
			if n[dir] != None:
				if n[dir].occupant != None:
					if n[dir].occupant.type == OccupantType.road:
						if n[dir].occupant.onLand:
							#self.roadConnections[dir] = n[dir].occupant
							self.roadConnections.append(n[dir].occupant)
		self.setSprite()			
		self.visitRoadConnections()
		
	def newConstruct(self):
		for t in self.tiles:
			t.buildOpon(TileType.building,self)
			n = t.neighbors
			for dir in range(4):			
				if n[dir] != None:
					if n[dir].occupant != None:
						if n[dir].occupant.type == OccupantType.road:
							if n[dir].occupant.onLand:
								self.roadConnections.append(n[dir].occupant)
			self.setSprite()			
			self.visitRoadConnections()	
		
	def setSprite(self):
		if self.buildingType == BuildingType.house:
			if self.state == BuildingState.normal:
				self.changeSprite(tileSprites['building_house'])
			elif self.state == BuildingState.decay:
				self.changeSprite(tileSprites['building_house_bad'])
			elif self.state == BuildingState.abandoned:
				self.changeSprite(tileSprites['building_house_abandon'])
			elif self.state == BuildingState.condemned:
				self.changeSprite(tileSprites['building_house_condemned'])			
		elif self.buildingType == BuildingType.business:
			self.newChangeSprite(tileSprites['building_business'])
		elif self.buildingType == BuildingType.park:
			self.changeSprite(tileSprites['building_park'])		
		else:
			raise("Uknown Building Type")
		
	def visitRoadConnections(self):	
		for r in self.roadConnections:
			r.connectBuilding(self)
		#for dir in range(len(self.roadConnections)):
		#	if self.roadConnections[dir] != None:
		#		self.roadConnections[dir].connectBuilding(self)
		
	def roadBuilt(self, roadObject, direction):
		#self.roadConnections[direction] = roadObject
		self.roadConnections.append(roadObject)
		#if direction == Direction.north:
			#self.roadConnections[Direction.south] = roadObject
		#elif direction == Direction.east:
			#self.roadConnections[Direction.west] = roadObject
		#elif direction == Direction.south:
			#self.roadConnections[Direction.north] = roadObject
		#elif direction == Direction.west:
			#self.roadConnections[Direction.east] = roadObject
	
	def roadRemoved(self, roadObject):
		#self.roadConnections[direction] = None
		for r in self.roadConnections:
			if r == roadObject:
				self.roadConnections.pop(self.roadConnections.index(r))
				break
		
	def isIsolated(self):		
		if len(self.roadConnections) > 0:
			return False
		#for d in range(4):
		#	if self.roadConnections[d] != None:
		#		return False
		return True	
	
	def decay(self):
		if self.state == BuildingState.normal:
			self.state = BuildingState.decay
		elif self.state == BuildingState.decay:
			self.state = BuildingState.abandoned
		elif self.state == BuildingState.abandoned:
			self.state = BuildingState.condemned			
		self.setSprite()		
				
	def improve(self):
		if self.state == BuildingState.decay:
			self.state = BuildingState.normal
		elif self.state == BuildingState.abandoned:
			self.state = BuildingState.decay	
		self.setSprite()	
											
	def destroy(self):
		TileOccupant.destroy(self)
		#for d in range(4):
		#	if self.roadConnections[d] != None:
		#		self.roadConnections[d].disconnectBuilding(self)
		for r in self.roadConnections:
			r.disconnectBuilding(self)		
	
	def getConnectedBuildings(self):
		sets = set()
		for r in self.roadConnections:
			#if self.roadConnections[d] != None:
			sets = sets | r.destinations.getConnectedBuildingsSet()							
		return sets #sets[0] | sets[1] | sets[2] | sets[3]
				
	def debugInfo(self):				
		if self.buildingType == BuildingType.house:
			print self.getInfoString()
			print "Other reachable houses in this neighborhood:"
		buildingSet = self.getConnectedBuildings()			
		for b in buildingSet:
			if b.tile.id != self.tile.id:
				name = "-"
				if b.buildingType == BuildingType.house:
					name = b.familyName
				elif b.buildingType == BuildingType.business:
					name = b.businessName					
				print "- The %s %s @ Tile #%d"%(name,BuildingType.strings[b.buildingType],b.tile.id)
				
	def getInfoString(self):
		return "Some building"							
										
class House(BuildingObject):
	def __init__(self,tile):		
		BuildingObject.__init__(self,tile,BuildingType.house)
		self.familyName = self.pickFamilyName()
		self.employed = False
		self.workPlace = None
		self.habitable = True
		self.jobless = 0 #months
		self.inService = 0
		#neighborhood
		self.nearbySchool = False
		self.nearbyParks = 0
		self.policeProtection = False
		self.fireProtection = False
		self.hospitalAccess = False		
		
	def pickFamilyName(self):
		r = randint(0,len(familyLastNames)-1)
		return familyLastNames[r]
		
	def getInfoString(self):						
		return "This is the %s house."%self.familyName
		
	def employAt(self,business):
		self.employed = True
		self.jobless = 0
		self.workPlace = business

	def terminateEmployment(self):
		self.employed = False
		self.workPlace = None			
		self.inService = 0	
	
	def noJob(self):
		self.jobless += 1
		if self.jobless == 6:
			self.decay()			
		elif self.jobless == 12:
			self.decay()
		elif self.jobless == 18:
			self.decay()
			self.habitable = False	
			
	def hasJob(self):
		self.inService += 1
		if self.inService == 6:
			self.improve()
		if self.inService == 12:				
			self.improve()
					
	def debugInfo(self):
		BuildingObject.debugInfo(self)
		if self.employed:
			wp = self.workPlace
			print "-- Works @ %s store on tile %d"%(wp.businessName,wp.tile.id)
		else:	
			print "-- Unemployed"
			
	def collectTaxes(self):
		if self.employed:
			return baseTaxRevenue['house']
		return 0
		
	def getTextLines(self):
		textLines = []
		textLines.append("The %s family lives here."%self.familyName)
		wp = "None (unemployed)"
		if self.workPlace != None:
			wp = self.workPlace.getInfoString()			
		textLines.append("Workplace: %s"%wp)		
		textLines.append("House condition: %s"%BuildingState.strings[self.state])
		return textLines
								
		
class Business(BuildingObject):
	def __init__(self,tile):
		BuildingObject.__init__(self,tile,BuildingType.business)
		self.businessName = self.pickName()
		self.staff = 0
		self.staffless = False
		self.baseDemand = 1
		self.maxStaff = self.baseDemand		
		self.maxDemand = 6
		self.hasOwner = True
		
	def pickName(self):
		r = randint(0,len(businessNames)-1)
		return businessNames[r]
	
	def getInfoString(self):
		return "%s store."%self.businessName
		
	def hire(self):
		if self.staff < self.maxStaff:
			self.staff += 1
			if self.staffless:
				self.staffless = False
			return True
		return False
		
	def lostEmployee(self):
		self.staff -= 1
		if self.staff == 0:
			self.staffless = True			
		
	def adaptLaborDemand(self,nearbyHouses,customers):
		newDemand = customers // 2
		if newDemand > self.maxDemand:
			self.maxStaff = self.maxDemand			
			return
		elif newDemand <= self.baseDemand:
			self.maxStaff = self.baseDemand			
		else:
			self.maxStaff = newDemand
		if self.maxStaff < self.staff:
			toFire = self.staff - self.maxStaff			
			for i in range(toFire):
				self.fireEmployee(nearbyHouses)
							
	def fireEmployee(self,houses):
		for h in houses:
			if h.employed:
				if h.workPlace == self:
					print "%s Store @ %d had to fire employee"%(self.businessName,self.tile.id) 
					h.terminateEmployment()
					self.staff -= 1
					break							
	
	def collectTaxes(self):
		if self.staff > 0:
			return baseTaxRevenue['business']
		return 0		
	
	def debugInfo(self):
		BuildingObject.debugInfo(self)
		print "-- This business gives work to %d households"%self.staff
		
	def getTextLines(self):
		textLines = []
		textLines.append(self.getInfoString())				
		textLines.append("%d people work here."%self.staff)
		textLines.append("Building condition: %s"%BuildingState.strings[self.state])			
		return textLines						
							 				
class Park(BuildingObject):
	def __init__(self,tile):
		BuildingObject.__init__(self,tile,BuildingType.park)
								 				
class DestinationList:
	def __init__(self):
		self.dests = []
	
	def addConnection(self,buildingObj,newDist):
		if newDist < GameConsts.maxDistance:
			found = False
			for d in self.dests:
				if d[0] == buildingObj:
					found = True
					if newDist < d[1]:						
						index = self.dests.index(d)
						self.dests[index] = (d[0],newDist)						
						#self.dests.append((buildingObj,newDist))
						return True
					else:
						return False	
			if not found:
				self.dests.append((buildingObj,newDist))
				return True		
		return False
		
	def terminateConnection(self,buildingObj):		
		for d in self.dests:
				if d[0] == buildingObj:
					self.dests.pop(self.dests.index(d))
					return True										
		return False
					
	def getConnectedBuildingsSet(self):
		l = []
		for d in self.dests:
			l.append(d[0])
		return set(l)
	
	def getList(self):
		return self.dests	
		
class Road(TileOccupant):
	def __init__(self,tile):		
		TileOccupant.__init__(self,tile,OccupantType.road)
		self.destinations = DestinationList()
		self.neighborroads = [None,None,None,None]
		self.numNeighbors = 0
		self.onLand = True
		if self.tile.type == TileType.water:
			self.onLand = False
		
	def construct(self):
		t = self.tile
		t.buildOpon(TileType.road,self)			
		neighbors = t.neighbors
		for dir in range(4):
			if neighbors[dir] != None:
				if neighbors[dir].type == TileType.road:
					self.numNeighbors += 1
					self.neighborroads[dir] = neighbors[dir].occupant
				elif neighbors[dir].type ==	TileType.building:
					if self.onLand:
						buildingObj = neighbors[dir].occupant
						self.destinations.addConnection(buildingObj,0)
						buildingObj.roadBuilt(self,Direction.opposite[dir])					
		if not self.onLand:
			if self.numNeighbors == 1:
				pass
			elif self.numNeighbors == 2:
				for d in range(4):
					if self.neighborroads[d] != None:
						if self.neighborroads[Direction.opposite[d]] == None:
							return False
			else:
				return False		
				
				
		for dir in range(4):
			if self.neighborroads[dir] != None:
				if not self.neighborroads[dir].receiveRoadConnection(Direction.opposite[dir],self):
					self.numNeighbors -= 1
					self.neighborroads[dir] = None
		#if self.neighborroads[Direction.north] != None:
			#self.neighborroads[Direction.north].receiveConnection(Direction.south,self)
		#if self.neighborroads[Direction.east] != None:
			#self.neighborroads[Direction.east].receiveConnection(Direction.west,self)
		#if self.neighborroads[Direction.south] != None:
			#self.neighborroads[Direction.south].receiveConnection(Direction.north,self)
		#if self.neighborroads[Direction.west] != None:
			#self.neighborroads[Direction.west].receiveConnection(Direction.east,self)			
		self.determineRoadSprite()		
		self.importDestinations()
		self.exportDestinations()
		return True
		
	def newConstruct(self):
		self.construct()	
						
	def determineRoadSprite(self):
		sprite = None
		if not self.onLand:
			#Road NOT built on Land, bridge:
			if self.numNeighbors == 1:
				if self.neighborroads[Direction.north] != None or self.neighborroads[Direction.south] != None:
					sprite = tileSprites['road_bridge_NS']					
				elif self.neighborroads[Direction.east] != None or self.neighborroads[Direction.west] != None:					
					sprite = tileSprites['road_bridge_EW']
			elif self.numNeighbors == 2:
				if self.neighborroads[Direction.north] != None and self.neighborroads[Direction.south] != None:					
					sprite = tileSprites['road_bridge_NS']
				elif self.neighborroads[Direction.east] != None and self.neighborroads[Direction.west] != None:					
					sprite = tileSprites['road_bridge_EW']
				else:
					#raise error
					pass
			else:
				#raise error
				pass		
		else:	
			#Road IS built on land:
			if self.numNeighbors == 0:				
				sprite = tileSprites['road_lone']
			elif self.numNeighbors == 1:
				if self.neighborroads[Direction.north] != None:
					sprite = tileSprites['road_dead_S']
				elif self.neighborroads[Direction.east] != None:
					sprite = tileSprites['road_dead_W']
				elif self.neighborroads[Direction.south] != None:
					sprite = tileSprites['road_dead_N']
				elif self.neighborroads[Direction.west] != None:
					sprite = tileSprites['road_dead_E']		
			elif self.numNeighbors == 2:
				if self.neighborroads[Direction.north] != None and self.neighborroads[Direction.east] != None:					
					sprite = tileSprites['road_corner_NE']
				elif self.neighborroads[Direction.north] != None and self.neighborroads[Direction.south] != None:					
					sprite = tileSprites['road_NS']
				elif self.neighborroads[Direction.north] != None and self.neighborroads[Direction.west] != None:					
					sprite = tileSprites['road_corner_NW']
				elif self.neighborroads[Direction.east] != None and self.neighborroads[Direction.south] != None:					
					sprite = tileSprites['road_corner_ES']
				elif self.neighborroads[Direction.east] != None and self.neighborroads[Direction.west] != None:					
					sprite = tileSprites['road_EW']
				elif self.neighborroads[Direction.south] != None and self.neighborroads[Direction.west] != None:
					sprite = tileSprites['road_corner_SW']
			elif self.numNeighbors == 3:
				if self.neighborroads[Direction.north] == None:					
					sprite = tileSprites['road_tjunct_ESW']
				elif self.neighborroads[Direction.east] == None:					
					sprite = tileSprites['road_tjunct_NSW']
				elif self.neighborroads[Direction.south] == None:					
					sprite = tileSprites['road_tjunct_NEW']
				elif self.neighborroads[Direction.west] == None:					
					sprite = tileSprites['road_tjunct_NES']
			elif self.numNeighbors == 4:				
				sprite = tileSprites['road_xing']
		if sprite == None:
			print "Tile %d reports no roadsprite:"%self.tile.id
			print "Number of neigborroads: %d"%self.numNeighbors
			for i in range(4):
				if self.neighborroads[i] != None:
					print "Direction %d: Neighbortile = %d"%(i,self.neighborroads[i].tile.id) 
		self.changeSprite(sprite)
	
	def importDestinations(self):
		for d in range(4):
			n = self.neighborroads[d] 
			if n != None:
				destsFromNeighbor = n.destinations.getList()
				for nd in destsFromNeighbor:
					self.destinations.addConnection(nd[0],nd[1]+1) 
		
	def exportDestinations(self):
		l = self.destinations.getList()
		for d in range(4):
			n = self.neighborroads[d] 
			if n != None:
				for myDest in l:
					n.addDestination(Direction.opposite[d],(myDest[0],myDest[1]+1))
									
	def connectBuilding(self,buildingObj):
		self.destinations.addConnection(buildingObj,0)
		#destTuple = (buildingObj,0)
		#self.destinations.append(destTuple)
		for d in range(4):
			if self.neighborroads[d] != None:
				self.neighborroads[d].addDestination(Direction.opposite[d],(buildingObj,1))			
		#if self.neighborroads[Direction.north] != None:
			#self.neighborroads[Direction.north].addDestination(Direction.south,(destTuple[0],1))
		#if self.neighborroads[Direction.east] != None:
			#self.neighborroads[Direction.east].addDestination(Direction.west,(destTuple[0],1))
		#if self.neighborroads[Direction.south] != None:
			#self.neighborroads[Direction.south].addDestination(Direction.north,(destTuple[0],1))
		#if self.neighborroads[Direction.west] != None:
			#self.neighborroads[Direction.west].addDestination(Direction.east,(destTuple[0],1))			
	
	def disconnectBuilding(self,buildingObj):
		self.destinations.terminateConnection(buildingObj)
		for d in range(4):
			if self.neighborroads[d] != None:
				self.neighborroads[d].terminateDestination(buildingObj,Direction.opposite[d])
									
	def addDestination(self,comingFrom,destTuple):	
		distance = destTuple[1]				
		#if distance < GameConsts.maxDistance: 
		if self.destinations.addConnection(destTuple[0],distance):
			for d in range(4):
				if comingFrom != d and self.neighborroads[d] != None:
					self.neighborroads[d].addDestination(Direction.opposite[d],(destTuple[0],distance+1))
			#shorterRoute = True
			#alreadyInList = False			
			#for d in self.destinations:
				#if d[0] == destTuple[0]: 
					#alreadyInList = True
					#if d[1] <= distance:
						#shorterRoute = False
						#break
			#if not alreadyInList:
				#self.destinations.append(destTuple)			
			#if shorterRoute:
				#if comingFrom != Direction.north and self.neighborroads[Direction.north] != None:
					#self.neighborroads[Direction.north].addDestination(Direction.south,(destTuple[0],distance+1))
				#if comingFrom != Direction.east and self.neighborroads[Direction.east] != None:
					#self.neighborroads[Direction.east].addDestination(Direction.west,(destTuple[0],distance+1))
				#if comingFrom != Direction.south and self.neighborroads[Direction.south] != None:
					#self.neighborroads[Direction.south].addDestination(Direction.north,(destTuple[0],distance+1))
				#if comingFrom != Direction.west and self.neighborroads[Direction.west] != None:
					#self.neighborroads[Direction.west].addDestination(Direction.east,(destTuple[0],distance+1))
	
	def terminateDestination(self,buildingObj,comingFrom):
		if self.destinations.terminateConnection(buildingObj):
			for d in range(4):
				if d != comingFrom and self.neighborroads[d] != None:
					self.neighborroads[d].terminateDestination(buildingObj,Direction.opposite[d])
				
	def receiveRoadConnection(self,direction,roadObj):		
		if not self.onLand:
			if self.numNeighbors > 1:
				return False									 
		if direction == Direction.north:
			self.neighborroads[Direction.north] = roadObj
			self.numNeighbors += 1			
		elif direction == Direction.east:
			self.neighborroads[Direction.east] = roadObj
			self.numNeighbors += 1
		elif direction == Direction.south:
			self.neighborroads[Direction.south] = roadObj
			self.numNeighbors += 1
		elif direction == Direction.west:
			self.neighborroads[Direction.west] = roadObj
			self.numNeighbors += 1	
		self.determineRoadSprite()
		return True
		
	def terminateRoadConnection(self,direction):
		if direction == Direction.north:
			self.neighborroads[Direction.north] = None
			self.numNeighbors -= 1			
		elif direction == Direction.east:
			self.neighborroads[Direction.east] = None
			self.numNeighbors -= 1
		elif direction == Direction.south:
			self.neighborroads[Direction.south] = None
			self.numNeighbors -= 1
		elif direction == Direction.west:
			self.neighborroads[Direction.west] = None
			self.numNeighbors -= 1	
		self.determineRoadSprite()
	
	def getDestinationSet(self):
		pass
	
	def destroy(self):
		buildingsToCheck = []
		t = self.tile
		for d in range(4):
			if t.neighbors[d] != None:								
				if t.neighbors[d].occupant != None:
					if t.neighbors[d].occupant.type == OccupantType.building:
						#t.neighbors[d].occupant.roadRemoved(Direction.opposite[d])
						t.neighbors[d].occupant.roadRemoved(self)						
		s = self.destinations.getConnectedBuildingsSet()
		for i in s:
			for d in range(4):
				if self.neighborroads[d] != None:
					self.neighborroads[d].terminateDestination(i,Direction.opposite[d])			
		if self.neighborroads[Direction.north] != None:
			self.neighborroads[Direction.north].terminateRoadConnection(Direction.south)
		if self.neighborroads[Direction.east] != None:
			self.neighborroads[Direction.east].terminateRoadConnection(Direction.west)
		if self.neighborroads[Direction.south] != None:
			self.neighborroads[Direction.south].terminateRoadConnection(Direction.north)
		if self.neighborroads[Direction.west] != None:
			self.neighborroads[Direction.west].terminateRoadConnection(Direction.east)		
		for i in s:
			if not i.isIsolated():
				i.visitRoadConnections()
		TileOccupant.destroy(self)
			
	def debugInfo(self):
		print "Road on tile %d"%self.tile.id
		print "Destinations to be reached from here: "
		l = self.destinations.dests		
		if len(l) > 0:
			for d in l:
				print "Building on tile: %d in %d steps"%(d[0].tile.id,d[1])
		else:
			print "Destination unknown."		
	
	def getInfoString(self):
		n = self.numNeighbors
		if n == 0:
			return "It's an isolated road."
		elif n == 1:
			return "It's a dead-end road"
		elif n == 2:
			if self.onLand:
				return "It's road with two ends"
			else:
				return "It's a bridge"	
		elif n == 3:
			return "It's a T-junction"
		elif n == 4:
			return "It's a level crossing"
		else:
			raise("impossible number of Neighbors.")

def MouseInRect(pos,area):
	if pos[0] >= area[0]:
		if pos[0] <= (area[0] + area[2]):
			if pos[1] >= area[1]:
				if pos[1] <= (area[1] + area[3]):
					return True
	return False				


class InterfacePanel:
	def __init__(self,targetSurface,geometry,interface,border=False):
		self.targetSurface = targetSurface
		self.area = geometry
		self.border = border
		self.iface = interface
		self.setFonts()
		self.overlay = pygame.Surface((self.area[2],self.area[3]))
		self.overlay.set_alpha(192)
		self.overlay.fill((64,64,64))
	
	def setFonts(self):
		self.normalFont = pygame.font.Font(None,20)
		self.bigFont = pygame.font.Font(None,40)
		self.smallFont = pygame.font.Font(None,10)
		
	def hasMouse(self,pos):
		if MouseInRect(pos,self.area):
			return True
		return False
		
	def drawBorder(self):
		if self.border:
			r = self.area
			r1 = (r[0]-1,r[1]-1,r[2]+2,r[3]+2)
			pygame.draw.rect(self.targetSurface,(0,128,0),r1,1)			
			r2 = (r1[0]-1,r1[1]-1,r1[2]+2,r1[3]+2)
			pygame.draw.rect(self.targetSurface,(0,196,0),r2,1)
			r3 = (r2[0]-1,r2[1]-1,r2[2]+2,r2[3]+2)
			pygame.draw.rect(self.targetSurface,(0,255,0),r3,1)\
			
	def grayOut(self):
		self.targetSurface.blit(self.overlay,(self.area[0],self.area[1]))
			

class ToolWindow(InterfacePanel):
	def __init__(self,targetSurface,interface):
		InterfacePanel.__init__(self,targetSurface,(20,20,64,480),interface,True)
		self.drawBorder()
		self.menuImg = pygame.Surface((self.area[2],self.area[3]))
		#self.buttons = [Button(Sprites.buttons[Tool.select],(9,20),Tool.select),Button(Sprites.buttons[Tool.build],(9,60),Tool.build),Button(Sprites.buttons[Tool.destroy],(9,100),Tool.destroy)]				
		self.menu = None
		self.offsetX = (self.area[2]-32) // 2
		self.offsetY = 20
		self.margin = 10
		self.enter(MenuType.default)		
				
	def enter(self,m):
		self.menu = Menu.buttons[m]
		i = 0
		for b in self.menu:
			b.pos = (self.area[0] + self.offsetX, self.area[1] + self.offsetY + ((32 + self.margin) * i))
			i += 1
		self.draw()				
		
	def handleLeftClick(self, pos):
		for b in self.menu:
			if b.clicked(pos):
				print "button clicked"		
				return b.action
		return None
	
	def draw(self):
		self.menuImg.fill((128,128,128))
		for b in self.menu:
			pygame.draw.rect(self.menuImg,(0,0,255),((b.pos[0] - self.area[0])-1,(b.pos[1] - self.area[1])-1,b.image.get_width()+2,b.image.get_height()+2),1)
			self.menuImg.blit(b.image, (b.pos[0] - self.area[0],b.pos[1] - self.area[1]))					
		self.targetSurface.blit(self.menuImg,(self.area[0],self.area[1]))	

class GridWindow(InterfacePanel):
	def __init__(self,grid,targetSurface,interface):		
		InterfacePanel.__init__(self,targetSurface,(140,20,640,480),interface,True)
		self.grid = grid								
		self.scrolled = (0,0)
		origWidth = self.grid.gridImg.get_width()
		origHeight = self.grid.gridImg.get_height()
		maxX = origWidth - self.area[2]
		maxY = origHeight - self.area[3]
		if maxX < 0: 
			maxX = 0
		if maxY < 0: 
			maxY = 0
		self.maxScroll = (maxX,maxY)
		scrollEdge = 20
		self.scrollAreaLeft = (self.area[0],self.area[1],scrollEdge,self.area[3])
		self.scrollAreaRight = ((self.area[0] + self.area[2])-scrollEdge,self.area[1],scrollEdge,self.area[3])
		self.scrollAreaTop = (self.area[0],self.area[1],self.area[2],scrollEdge)
		self.scrollAreaBottom = (self.area[0],(self.area[1] + self.area[3])-scrollEdge,self.area[2],scrollEdge)
		self.scrollSpeed = 4
		self.hasScrolled = False
		self.drawBorder()
		self.popUp = InfoPopUp(self,targetSurface,interface)
		self.popUpActive = False
		
	def handleMouse(self,pos,buttons):
		if not self.popUpActive:
			self.hasScrolled = False
			if MouseInRect(pos, self.scrollAreaLeft):
				if self.scrolled[0] > 0:
					self.scrolled = (self.scrolled[0]-self.scrollSpeed,self.scrolled[1])
					self.hasScrolled = True
			else:		
				if MouseInRect(pos, self.scrollAreaRight):
					if self.scrolled[0] < self.maxScroll[0]:
						self.scrolled = (self.scrolled[0]+self.scrollSpeed,self.scrolled[1])
						self.hasScrolled = True
			if MouseInRect(pos, self.scrollAreaTop):
				if self.scrolled[1] > 0:				
					self.scrolled = (self.scrolled[0],self.scrolled[1]-self.scrollSpeed)
					self.hasScrolled = True
			else:		
				if MouseInRect(pos, self.scrollAreaBottom):	
					if self.scrolled[1] < self.maxScroll[1]:
						self.scrolled = (self.scrolled[0],self.scrolled[1]+self.scrollSpeed)
						self.hasScrolled = True
			#self.grid.highlightTile((pos[0] - self.area[0] + self.scrolled[0], pos[1] - self.area[1] + self.scrolled[1]))									
		
	def handleLeftClick(self,pos,toolTuple):			
		relpos = (pos[0] - self.area[0] + self.scrolled[0], pos[1] - self.area[1] + self.scrolled[1])
		t = self.grid.getTileFromCoords(relpos)
		#t.debugInfo()
		if t != None:			
			if toolTuple[0] == None:
				print "TileID = %d, Tile type= %d"%(t.id,t.type)
			else:
				#print "Apply tool with id %d on tile: %d"%(tool,t.id)
				result = self.grid.actOnTile(t.id,(toolTuple[0],toolTuple[1]))				
				self.drawVisibleGrid()
				if toolTuple[0] == CursorMode.destroy:
					if result: 
						self.iface.shout("Destroyed object on tile: %d."%t.id)
					else:
						self.iface.shout("No object to destroy!")
				elif toolTuple[0] == CursorMode.build:
					if result: 
						self.iface.shout("Built on tile:%d."%t.id)			
				elif toolTuple[0] == CursorMode.select:
					t.debugInfo()
					self.iface.shout(t.getInfoString())
					if not self.popUpActive:						
						if t.occupant != None:
							self.popUpActive = True
							self.grayOut()
							self.popUp.displayInfo(t.occupant)
					else:
						self.popUpActive = False	
		
	def drawVisibleGrid(self):
		if not self.popUpActive:
			visibleGrid = (self.scrolled[0],self.scrolled[1],self.area[2],self.area[3])		
			self.targetSurface.blit(self.grid.gridImg,(self.area[0],self.area[1]),visibleGrid)	
						
	def draw(self):		
		if self.hasScrolled:
			self.drawVisibleGrid()


class MessageWindow(InterfacePanel):
	def __init__(self, targetSurface, interface):			
		InterfacePanel.__init__(self,targetSurface,(340,520,440,64),interface,True)
		self.textSurface = pygame.Surface((self.area[2],self.area[3]))
		self.drawBorder() 
				
	def displayText(self,text):		
		textImage = self.normalFont.render(text,True,(255,196,0))
		r = textImage.get_rect()
		x = (self.area[2] - r[2]) // 2
		y = (self.area[3] - r[3]) // 2
		self.textSurface.fill((96,96,96))
		self.textSurface.blit(textImage,(x,y))
		self.targetSurface.blit(self.textSurface,(self.area[0],self.area[1]))

									
class TownInfoWindow(InterfacePanel):
	def __init__(self, targetSurface, interface, town):			
		InterfacePanel.__init__(self,targetSurface,(140,520,180,64),interface,True)
		self.textSurface = pygame.Surface((self.area[2],self.area[3]))
		self.myTown = town
		self.drawBorder()
				
	def updateInfo(self):
		balance = "$%d"%self.myTown.balance
		line1 = self.bigFont.render(balance,True,(255,196,0))
		line2 = self.normalFont.render(self.myTown.getDateString(),True,(255,196,0))
		r1 = line1.get_rect()
		r2 = line2.get_rect() 
		x = 20
		y = (self.area[3] - (r1[3] + r2[3] + 5)) // 2
		self.textSurface.fill((96,96,96))
		self.textSurface.blit(line1,(x,y))
		self.textSurface.blit(line2,(x,y+r1[3]+5))
		self.targetSurface.blit(self.textSurface,(self.area[0],self.area[1]))							

class SelectedToolWindow(InterfacePanel):
	def __init__(self,targetSurface,interface,initTool):
		InterfacePanel.__init__(self,targetSurface,(20,520,64,64),interface,True)
		self.tool = initTool
		self.drawBorder()
		
	def changeTool(self,tool):
		self.tool = tool
		pos = (self.area[0]+16,self.area[1]+16)
		if self.tool != None:
			if self.tool == CursorMode.select:
				self.targetSurface.blit(Sprites.button_select,pos)
			elif self.tool == CursorMode.destroy:
				self.targetSurface.blit(Sprites.button_destroy,pos)
			elif self.tool == CursorMode.build:
				self.targetSurface.blit(Sprites.button_build,pos)

class InfoPopUp(InterfacePanel):
	def __init__(self,projectedOn,targetSurface,interface):
		x = projectedOn.area[0] + 15
		y = projectedOn.area[1] + 15
		w = projectedOn.area[2] - 30
		h = projectedOn.area[3] - 30
		InterfacePanel.__init__(self,targetSurface,(x,y,w,h),interface,True)
		self.textSurface = pygame.Surface((w,h))		
	
	def displayInfo(self,object):
		self.textSurface.fill((64,64,64))
		lineDistance = 5
		texts = self.getInfoText(object)		
		lines = []
		#i = 0
		for t in texts:
			fSurface = self.normalFont.render(t,True,(255,128,0))
			lines.append(fSurface)										
		y = 0
		for l in lines:
			y += (l.get_height() + lineDistance)
			x = (self.area[2] - l.get_width()) // 2
			self.textSurface.blit(l,(x,y))
		self.targetSurface.blit(self.textSurface,(self.area[0],self.area[1]))
		self.drawBorder()
		pass
		
	def getInfoText(self,object):
		texts = []
		if object.type == OccupantType.building:
			texts = object.getTextLines()
			"""
			if object.buildingType == BuildingType.house:
				texts.append("Family: %s"%object.familyName)
				jobString = "No"
				if object.employed:
					jobString = "Yes"
				texts.append("Has Job: %s"%jobString)
			elif object.buildingType == BuildingType.business:
				texts.append("This is a(n) %s store."%object.businessName)
				texts.append("Number of employees: %d"%object.staff)
			"""	
		return texts								
			
class InterFace:
	def __init__(self,town,surface):
		self.surface = surface
		self.myTown = town
		self.gridWin = GridWindow(self.myTown.grid,surface,self)
		self.gridWin.drawVisibleGrid()
		self.toolWin = ToolWindow(surface,self)
		self.toolWin.draw()
		self.townWin = TownInfoWindow(surface,self,self.myTown)
		self.townWin.updateInfo()
		self.selectedToolWin = SelectedToolWindow(surface,self,None)
		self.messageWin = MessageWindow(surface,self)
		self.mode = None
		self.tool = None
		
		self.cursorBackground = pygame.Surface((16,16))
		self.cursorBackground.fill((255,0,255))
		self.cursorBackground.set_colorkey((255,0,255))
		self.cursorBgSet = False
		self.cursorPos = (0,0)
		self.oldCursorPos = (0,0)
						
	def handleMouseClick(self,pos,button):		
		if self.gridWin.hasMouse(pos):
			if button == 1:
				self.gridWin.handleLeftClick(pos,(self.mode,self.tool))			
		elif self.toolWin.hasMouse(pos):
			if button == 1:
				action = self.toolWin.handleLeftClick(pos)
				if action != None:
					if action.type == ActionType.enterMenu:
						self.toolWin.enter(action.value)
						self.changeMode()
					elif action.type == ActionType.changeMode:
						self.mode = action.value
						self.changeMode()					 	
					elif action.type == ActionType.setTool:
						self.tool = action.value
						self.mode = CursorMode.build
						if self.tool == Tool.build_road:
							self.shout("Build roads. ($%d)"%constructionCosts['road'])
						elif self.tool == Tool.build_house:
							self.shout("Build houses. ($%d)"%constructionCosts['house'])
						elif self.tool == Tool.build_business:
							self.shout("Build businesses. ($%d)"%constructionCosts['business'])
						elif self.tool == Tool.build_park:
							self.shout("Build parks. ($%d)"%constructionCosts['park'])
						self.changeMode()				
					else:
						raise("Unknown return value from button")										
					self.displayTool()				
		self.townWin.updateInfo()
					
	def handleMouse(self,pos,rel,buttons):
		self.cursorPos = pos
		self.oldCursorPos = (pos[0]-rel[0],pos[1]-rel[1])
		if self.gridWin.hasMouse(pos):
			self.gridWin.handleMouse(pos,buttons)
		elif self.toolWin.hasMouse(pos):			
			pass			
					
	def displayTool(self):
		self.selectedToolWin.changeTool(self.mode)				
		
	def drawMouseCursor(self):
		if self.cursorBgSet:
			self.surface.blit(self.cursorBackground,self.oldCursorPos)
		self.cursorBackground.blit(self.surface,(0,0),(self.cursorPos[0],self.cursorPos[1],16,16))
		self.cursorBgSet = True
		self.surface.blit(Sprites.cursor,self.cursorPos)
	
	def changeMode(self):	
		if self.mode == CursorMode.destroy:
			setCursor(CursorType.destruct)
		elif self.mode == CursorMode.select:
			setCursor(CursorType.question)
		elif self.mode == CursorMode.build:
			setCursor(CursorType.build)
		else:	
			setCursor(CursorType.normal)
			
	def	refresh(self):
		self.gridWin.draw()		
		#self.drawMouseCursor()
		
	def shout(self,text):
		self.messageWin.displayText(text)


class Starter(PygameHelper):
    def __init__(self):							
		fullScreen = False
		if len(sys.argv) > 1:
			if sys.argv[1] == "--full":
				fullScreen = True
		
		self.w, self.h = 800, 600       
		PygameHelper.__init__(self, size=(self.w, self.h), fill=((0,0,0)), full=fullScreen, programName="TownGrid")			
	
		self.town = Town(25,20)
		self.interface = InterFace(self.town,self.screen)
						
		self.ticksSinceLastAnimation = 0
		self.ticks = 0
		setCursor()
				
    def update(self):		
		self.ticks += 1
		if self.ticks == 40:
			self.town.clock.tick()
			self.interface.townWin.updateInfo()
			self.ticks = 0
			
		self.ticksSinceLastAnimation += 1
		if self.ticksSinceLastAnimation > GameConsts.aniFreq:
			self.ticksSinceLastAnimation = 0
			self.town.grid.animateTileSprites()
			self.interface.gridWin.drawVisibleGrid()
							
		self.interface.handleMouse(pygame.mouse.get_pos(),pygame.mouse.get_rel(),pygame.mouse.get_pressed())
        
    def keyDown(self, key):
		pass
				   
    def keyUp(self, key):
		pass
        
    def mouseUp(self, button, pos):
        self.interface.handleMouseClick(pos, button)
        pass        
        
    def mouseMotion(self, buttons, pos, rel):
		pass
						        
    def draw(self):
        self.interface.refresh()
      		
s = Starter()
s.mainLoop(40)
