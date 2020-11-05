"""A very simple Snake game om Pygame.
Snake can only collide with itself not the walls."""

import pygame
import random
import sys

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 520
SCREEN_SQUARE = 40
SCREEN_COLOR = (155,186,90)
SNAKE_COLOR = (39,47,23)
DEAD_COLOR = (119,142,71)
GRID_COLOR = SCREEN_COLOR
FOOD_COLOR = (232, 238, 23)
ACTIVE_COLOR = (255,255,255)
SA_COLOR = ACTIVE_COLOR
Q_COLOR = SNAKE_COLOR


class Snake:
	def __init__(self):
		self.color = SNAKE_COLOR
		self.pattern_color = SCREEN_COLOR
		self.width = SCREEN_SQUARE
		self.pattern_width = 8
		self.head_pos = (int(SCREEN_WIDTH / 2 - SCREEN_SQUARE), int(SCREEN_HEIGHT / 2 - SCREEN_SQUARE / 2))
		self.coords = [(),(),()]
		self.dir = 'stop'  #at the start snake won't move until you press right

		for i in range(len(self.coords)):
			(x,y) = self.head_pos
			x -= i * self.width
			self.coords[i] = (x,y)

	def update(self):
		for i in range(len(self.coords) - 1, 0, -1):
			self.coords[i] = self.coords[i-1]
		self.change_head_pos()

	def change_head_pos(self):
		(x,y) = self.head_pos
		if self.dir == 'right':
			if x == SCREEN_WIDTH - SCREEN_SQUARE:
				x = 0
			else:
				x += SCREEN_SQUARE
		elif self.dir == 'left':
			if x == 0:
				x = SCREEN_WIDTH - SCREEN_SQUARE
			else:
				x -= SCREEN_SQUARE
		elif self.dir == 'up':
			if y == 0:
				y = SCREEN_HEIGHT - SCREEN_SQUARE
			else:
				y -= SCREEN_SQUARE
		elif self.dir == 'down':
			if y == SCREEN_HEIGHT - SCREEN_SQUARE:
				y = 0
			else:
				y += SCREEN_SQUARE
		self.head_pos = (x,y)
		self.coords[0] = self.head_pos

	def hits_itself(self):
		for coord in self.coords[1:]:
			(x,y) = coord
			(x0, y0) = self.head_pos

			if self.dir == 'right':
				if y0 == y and x0 == x - self.width:
					return True
			elif self.dir == 'left':
				if y0 == y and x0 == x + self.width:
					return True
			elif self.dir == 'up':
				if x0 == x and y0 == y + self.width:
					return True
			else:
				if x0 == x and y0 == y - self.width:
					return True
		return False

	def draw(self,surface):
		# snake base color drawing
		for tuple in self.coords:
			sq = (tuple, (self.width, self.width))
			surface.fill(self.color,sq)

		# snake pattern drawing
		for tuple in self.coords[1:]:  #for every snake square except for head
			pat_sq_num = int(self.width / self.pattern_width)  #number of pattern squares per snake square
			(x0,y0) = tuple

			for i in range(pat_sq_num):
				x = x0 + self.pattern_width * i
				y = y0 + self.width - self.pattern_width * (i+1)
				pat_sq = ((x,y),(self.pattern_width, self.pattern_width))
				surface.fill(self.pattern_color,pat_sq)

		#eyes drawing
		(x0,y0) = self.head_pos
		if self.dir in ('right','left','stop'):
			x = x0 + self.width * 1/3
			y1 = y0 + self.width * 1/6
			y2 = y0 + self.width - self.width * 1/6 - self.pattern_width
			eye1 = ((x,y1),(self.pattern_width,self.pattern_width))
			eye2 = ((x, y2), (self.pattern_width, self.pattern_width))
		else:
			y = y0 + self.width - self.width * 1/3 - self.pattern_width
			x1 = x0 + self.width * 1/6
			x2 = (x0 + self.width - self.width * 1/6 - self.pattern_width)
			eye1 = (x1, y), (self.pattern_width, self.pattern_width)
			eye2 = (x2, y), (self.pattern_width, self.pattern_width)
		surface.fill(self.pattern_color,eye1)
		surface.fill(self.pattern_color,eye2)

	def grow(self):
		self.coords.append(())


class Food:
	def __init__(self):
		self.color = SNAKE_COLOR
		self.width = SCREEN_SQUARE
		self.coords = ()

	def update(self,grid_coords,snake_coords):
		self.coords = random.choice(grid_coords)
		while self.coords in snake_coords:
			self.coords = random.choice(grid_coords)

	def draw(self,surface):
		food = (self.coords,(self.width, self.width))
		surface.fill(self.color,food)


	def on_screen(self):
		return self.coords != ()



def show_message(surface, text, pos = (100,100),  font_size = 75, color = SNAKE_COLOR):
	msg_font = pygame.font.SysFont('Arial', font_size)
	msg = msg_font.render(text, True, color)
	surface.blit(msg, pos)

def main():
	pygame.init()
	clock = pygame.time.Clock()
	main_screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	snake = Snake()
	food = Food()
	game_over = False

	while True:
		"""main cycle"""

		while not game_over:
			"""not game over cycle"""

			#button pushing hadling
			ev = pygame.event.poll()
			if ev.type == pygame.QUIT:
				break
			if ev.type == pygame.KEYDOWN:
				if snake.dir != 'stop':  # we can only start the game with the 'right' button
					if ev.dict['key'] == 273 and snake.dir != 'down': # double conditions for no reverse
						snake.dir = 'up'
					elif ev.dict['key'] == 274 and snake.dir != 'up':
						snake.dir = 'down'
					elif ev.dict['key'] == 276 and snake.dir != 'right':
						snake.dir = 'left'
				if ev.dict['key'] == 275 and snake.dir != 'left':
					snake.dir = 'right'
				elif ev.dict['key'] == 27:  #escape
					break
				elif ev.dict['key'] == 32:  #space for debugging
					game_over = True


			# game screen drawing
			grid_coords = []
			for row in range(int(SCREEN_HEIGHT / SCREEN_SQUARE)):
				for col in range(int(SCREEN_WIDTH / SCREEN_SQUARE)):
					sq = (col * SCREEN_SQUARE, row * SCREEN_SQUARE, SCREEN_SQUARE, SCREEN_SQUARE)
					gr = (col * SCREEN_SQUARE + 1, row * SCREEN_SQUARE + 1, SCREEN_SQUARE - 2, SCREEN_SQUARE - 2)
					main_screen.fill(GRID_COLOR, sq)
					main_screen.fill(SCREEN_COLOR, gr)
					grid_coords.append((col * SCREEN_SQUARE, row * SCREEN_SQUARE))

			# snake drawing
			if snake.dir != 'stop':
				snake.update()
			snake.draw(main_screen)

			# collision check
			if snake.hits_itself():
				pygame.display.flip()
				game_over = True

			# food drawing
			if not food.on_screen():
				food.update(grid_coords, snake.coords)
			elif snake.head_pos == food.coords:
				food.update(grid_coords, snake.coords)
				snake.grow()
			food.draw(main_screen)

			pygame.display.flip()
			clock.tick(7)

		while game_over:
			global SA_COLOR,Q_COLOR

			"""game over cycle"""
			# Events
			ev = pygame.event.poll()
			if ev.type == pygame.QUIT:
				break
			if ev.type == pygame.KEYDOWN:
				if ev.dict['key'] == 274 or ev.dict['key'] == 273:   # down or up|
					SA_COLOR, Q_COLOR = Q_COLOR, SA_COLOR
				elif ev.dict['key'] == 13:   # enter
					if SA_COLOR == ACTIVE_COLOR:   # restart
						snake = Snake()
						main()
					elif Q_COLOR == ACTIVE_COLOR:   # quit
						break

			# new color snake and food drawing
			snake.color = food.color = DEAD_COLOR
			snake.draw(main_screen)
			food.draw(main_screen)

			# game over screen drawing
			show_message(main_screen,'Game over')
			show_message(main_screen, f"Your score: {len(snake.coords) - 3}",font_size=32, pos=(100,175))
			show_message(main_screen, "Start again", font_size=40, pos=(100, 207), color = SA_COLOR)
			show_message(main_screen, "Quit", font_size=40, pos=(100, 239), color = Q_COLOR)

			pygame.display.flip()

		pygame.quit()
		sys.exit()

if __name__ == '__main__':
	main()