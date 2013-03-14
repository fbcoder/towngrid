#!/usr/bin/env python
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
