import math
import random
import pygame
import pygame.gfxdraw

frameRate = 30
frameDelay = 1000 / frameRate
speed = 400
maxTime = 10
time = 0.0

class Ball:
	def __init__(self, mass, x, y, velocityX, velocityY):
		self.x = float(x)
		self.y = float(y)
		self.velocityX = float(velocityX)
		self.velocityY = float(velocityY)
		self.mass = float(mass)
		self.radius = math.sqrt(mass/math.pi)
	def update(self):
		global speed
		self.x += self.velocityX / speed
		self.y += self.velocityY / speed
	def draw(self):
		pygame.gfxdraw.aacircle(screen, 320 + int(round(self.x * 10)), 240 + int(round(self.y * 10)), int(round(self.radius * 10)), (255,255,255))

balls = []
for x in range(-5, 5):
	for y in range(-5, 5):
		balls.append(Ball(random.randrange(3,6), x * 5, y * 5, random.randrange(-20,20), random.randrange(-20,20)))
balls.append(Ball(150, 0, -40, 0, 180))
balls.append(Ball(150, 0, 40, 0, -180))

screenWidth = 640
screenHeight = 480
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
done = False

def handleCollision(ball1, ball2):
	ballOverlap = ball1.radius + ball2.radius - math.hypot(ball1.y - ball2.y, ball1.x - ball2.x)
	if ballOverlap > 0:		# balls are touching
		if ball1.y - ball2.y == 0:
			# if the balls are vertical to each other
			if (ball1.x < ball2.x):
				ball1Velocity = ball1.velocityX
				ball2Velocity = -ball2.velocityX
			else:
				ball1Velocity = -ball1.velocityX
				ball2Velocity = ball2.velocityX
			newVelocity = (2 * -ball2.mass) * (ball1Velocity + ball2Velocity) / (ball1.mass + ball2.mass) + ball1Velocity
			newVelocity2 = (2 * -ball1.mass) * (ball2Velocity + ball1Velocity) / (ball2.mass + ball1.mass) + ball2Velocity
			ball1.velocityX = ball1.velocityX / abs(ball1.velocityX) * newVelocity
			ball2.velocityX = ball2.velocityX / abs(ball2.velocityX) * newVelocity2
		elif ball1.x - ball2.x == 0:
			# if the balls are horizontal to each other
			if (ball1.y < ball2.y):
				ball1Velocity = ball1.velocityY
				ball2Velocity = -ball2.velocityY
			else:
				ball1Velocity = -ball1.velocityY
				ball2Velocity = ball2.velocityY
			newVelocity = (2 * -ball2.mass) * (ball1Velocity + ball2Velocity) / (ball1.mass + ball2.mass) + ball1Velocity
			newVelocity2 = (2 * -ball1.mass) * (ball2Velocity + ball1Velocity) / (ball2.mass + ball1.mass) + ball2Velocity
			ball1.velocityY = ball1.velocityY / abs(ball1.velocityY) * newVelocity
			ball2.velocityY = ball2.velocityY / abs(ball2.velocityY) * newVelocity2
		else:
			# break the velocity vector into x and y components based on the tangent line to the collision
			slope = (ball1.y - ball2.y) / (ball1.x - ball2.x)
			tangentSlope = 1/-slope
			tangentIntercept = ball1.velocityY - tangentSlope * ball1.velocityX
			ball1VectorX = tangentIntercept / (slope - tangentSlope)
			ball1VectorY = tangentSlope * ball1VectorX + tangentIntercept
			if (
				(ball1.velocityY > tangentSlope * ball1.velocityX and
				ball2.y - ball1.y > tangentSlope * (ball2.x - ball1.x)) or
				(ball1.velocityY < tangentSlope * ball1.velocityX and
				ball2.y - ball1.y < tangentSlope * (ball2.x - ball1.x))):
				ball1Velocity = math.hypot(ball1VectorX, ball1VectorY)
			else:
				ball1Velocity = -math.hypot(ball1VectorX, ball1VectorY)

			tangentIntercept = ball2.velocityY - tangentSlope * ball2.velocityX
			ball2VectorX = tangentIntercept / (slope - tangentSlope)
			ball2VectorY = tangentSlope * ball2VectorX + tangentIntercept
			if (
				(ball2.velocityY > tangentSlope * ball2.velocityX and
				ball1.y - ball2.y > tangentSlope * (ball1.x - ball2.x)) or
				(ball2.velocityY < tangentSlope * ball2.velocityX and
				ball1.y - ball2.y < tangentSlope * (ball1.x - ball2.x))):
				ball2Velocity = math.hypot(ball2VectorX, ball2VectorY)
			else:
				ball2Velocity = -math.hypot(ball2VectorX, ball2VectorY)

			# figure out how much time would be required to back the balls up to right before they started touching
			collisionVelocity = ball1Velocity + ball2Velocity
			timeRequired = ballOverlap / collisionVelocity
			ball1.x -= (ball1.velocityX / speed) * timeRequired
			ball1.y -= (ball1.velocityY / speed) * timeRequired
			ball2.x -= (ball2.velocityX / speed) * timeRequired
			ball2.y -= (ball2.velocityY / speed) * timeRequired

			# calculate new velocities of the balls away from each other
			newVelocity = (2 * -ball2.mass) * (ball1Velocity + ball2Velocity) / (ball1.mass + ball2.mass) + ball1Velocity
			newVelocity2 = (2 * -ball1.mass) * (ball2Velocity + ball1Velocity) / (ball2.mass + ball1.mass) + ball2Velocity

			# break down the new velocity into x and y vectors
			distance = math.hypot(ball1.y - ball2.y, ball1.x - ball2.x)
			ball1.velocityX += -ball1VectorX + newVelocity * (ball2.x - ball1.x) / distance
			ball1.velocityY += -ball1VectorY + newVelocity * (ball2.y - ball1.y) / distance
			ball2.velocityX += -ball2VectorX + newVelocity2 * (ball1.x - ball2.x) / distance
			ball2.velocityY += -ball2VectorY + newVelocity2 * (ball1.y - ball2.y) / distance

lastFrame = pygame.time.get_ticks()
while not done:
	screen.fill((0, 0, 0))
	for i in balls:
		i.update()
	for i in range(0, len(balls)):
		for j in range(i + 1, len(balls)):
			handleCollision(balls[i], balls[j])
	for i in balls:
		i.draw()
	thisFrame = pygame.time.get_ticks()
	frameDifference = thisFrame - lastFrame
	if frameDifference < frameDelay:
		pygame.time.delay(frameDelay - frameDifference)
	lastFrame = pygame.time.get_ticks()
	pygame.display.flip()
	time += 1 / speed
	if time > maxTime:
		break
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
