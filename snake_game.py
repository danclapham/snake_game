import pygame, sys, random, time

# check for initialising errors
check_errors = pygame.init()
if check_errors[1] > 0:
	print("(!) Had {0} initialising errors, exiting...".format(check_errors[1]))
	sys.exit(-1)
else: 
	print("(+) PyGame successfully initialised!")

# play surface
play_surface = pygame.display.set_mode((720, 460))
pygame.display.set_caption('Snake game!')

# colours 
red   = pygame.Color(200, 0, 0)			# game over
green = pygame.Color(0, 200, 0)			# snake 
black = pygame.Color(0, 0, 0)			# score 
white = pygame.Color(255, 255, 255)		# background
brown = pygame.Color(165, 42, 42)		# food

# FPS controller
fps_controller = pygame.time.Clock()

# important variables
snake_pos = [100, 50]
snake_body = [[100,50], [90,50], [80,50]]

food_pos = [random.randrange(1,72)*10, random.randrange(1,46)*10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

# game over function
def game_over():
	my_font = pygame.font.SysFont('monaco', 84)
	GO_surface = my_font.render('Game over!', True, red)
	GO_rect = GO_surface.get_rect()
	GO_rect.midtop = (360, 15)
	play_surface.blit(GO_surface, GO_rect)
	show_score(0)
	pygame.display.flip()
	time.sleep(4)
	pygame.quit()
	sys.exit()

# score
def show_score(choice=1):
	my_font = pygame.font.SysFont('monaco', 28)
	score_surface = my_font.render('Score: {0}'.format(score), True, black)
	score_rect = score_surface.get_rect()
	if choice == 1:
		score_rect.midtop = (80, 10)
	else:
		score_rect.midtop = (360, 120)
	play_surface.blit(score_surface, score_rect)
	pygame.display.flip()

# main logic of the game
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT or event.key == ord('d'):
				change_to = 'RIGHT'
			if event.key == pygame.K_LEFT or event.key == ord('a'):
				change_to = 'LEFT'
			if event.key == pygame.K_UP or event.key == ord('w'):
				change_to = 'UP'
			if event.key == pygame.K_DOWN or event.key == ord('s'):
				change_to = 'DOWN'
			if event.key == pygame.K_ESCAPE:
				pygame.event.post(pygame.event.Event(pygame.QUIT))

	# validation of direction
	if change_to == 'RIGHT' and not direction == 'LEFT':
		direction = 'RIGHT'
	if change_to == 'LEFT' and not direction == 'RIGHT':
		direction = 'LEFT'
	if change_to == 'UP' and not direction == 'DOWN':
		direction = 'UP'
	if change_to == 'DOWN' and not direction == 'UP':
		direction = 'DOWN'
	
	# update snake position
	if direction == 'RIGHT':
		snake_pos[0] += 10
	if direction == 'LEFT':
		snake_pos[0] -= 10
	if direction == 'UP':
		snake_pos[1] -= 10
	if direction == 'DOWN':
		snake_pos[1] += 10
	
	# snake body mechanism
	snake_body.insert(0, list(snake_pos))
	if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
		score += 1
		food_spawn = False
	else:
		snake_body.pop()

	# food spawn
	if food_spawn == False:
		food_pos = [random.randrange(1,72)*10, random.randrange(1,46)*10]
		food_spawn = True

	# background
	play_surface.fill(white)

	# draw snake
	for pos in snake_body:
		pygame.draw.rect(play_surface, green, 
			pygame.Rect(pos[0], pos[1], 10, 10))

	pygame.draw.rect(play_surface, brown,
		pygame.Rect(food_pos[0], food_pos[1], 10, 10))

	# bound
	if snake_pos[0] > 710 or snake_pos[0] < 0:
		game_over()
	if snake_pos[1] > 450 or snake_pos[1] < 0:
		game_over()

	for block in snake_body[1:]:
		if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
			game_over()

	show_score()
	pygame.display.flip()	
	fps_controller.tick(23)

