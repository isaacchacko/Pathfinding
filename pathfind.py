# imports
import pygame
import random
import sys

WIN_SIZE = 500
BLIT_MULT = 5

# COLORS 
BLACK = (0,0,0)
BLUE = (63, 72, 204)
GREEN = (34, 177, 76)
ACTIVE = (232, 81, 81)
SEARCHED = (44, 159, 191)
PATH = (255, 247, 0)

# FUNCTIONS
def findPos(color, image):
	color = (color[0], color[1], color[2], 255)
	size = image.get_size()[0]
	for y in range(size):
		for x in range(size):
			if image.get_at((x,y)) == color:
				return (x,y)

findAdjacent = lambda pos, xdif, ydif: (pos[0] + xdif, pos[1] + ydif)

# INITALIZATION ----------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption('Pathfinding')
clock = pygame.time.Clock()
terrain = pygame.image.load('terrain.png')
ter_size = terrain.get_size()[0]
finish = findPos(GREEN, terrain)
start = findPos(BLUE, terrain)

# tuples will be (position, mother, ifActive, ifDrawn)
hounds = [[start, None, True, False]]
new = []
searched = [start]
path = []
path_found = False

# GAME LOOP --------------------------------------------------------------------
running = True
while running:
	
	# GENERAL ------------------------------------------------------------------
	clock.tick(20)

	# INPUT --------------------------------------------------------------------
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# UPDATE -------------------------------------------------------------------
	if path_found == False:
		for hound in hounds:
			if hound[2]: # if active
				if hound[0] != start:
					hound[2] = False # deactivate it
				north = findAdjacent(hound[0], 0, -1)
				south = findAdjacent(hound[0], 0, 1)
				east = findAdjacent(hound[0], 1, 0)
				west = findAdjacent(hound[0], -1, 0)
				for pos in [west,east,north,south]:
					try:
						color = terrain.get_at(pos)
					except:
						pass
					else:
						if color != BLACK and pos not in searched:
							hounds.append([pos, hound[0], False, False])
							searched.append(pos)
							new.append(pos)
	else:
		lastKnownPath = path[-1][0]
		for hound in hounds:
			if hound[0] == lastKnownPath:
				if hound[1] == None:
					pass
				else:
					path.append([hound[1], False])

	# set new positions to True, this is done afterwards so it is not iterated
	for pos in new:
		for hound in hounds:
			if hound[0] == pos:
				hound[2] = True
	new = []

	# set running to False if it hit the target
	if path_found == False:
		for hound in hounds:
			if hound[0] == finish:
				path_found = True
				path.append([finish, False])

	# RENDER -------------------------------------------------------------------
	screen.fill(BLACK)

	# set image colors
	for hound in hounds:
		if hound[3] == False: # if cell hasnt been drawn before
			if hound[2]:
				terrain.set_at(hound[0], ACTIVE)
			else:
				terrain.set_at(hound[0], SEARCHED)
				hound[3] = True

	for path_cell in path:
		if path_cell[1] == False:
			path_cell[1] = True
			terrain.set_at(path_cell[0], PATH)
	screen.blit(pygame.transform.scale(terrain, (ter_size*BLIT_MULT, ter_size*BLIT_MULT)), (0,0))
	pygame.display.flip()

pygame.quit()
sys.exit()
