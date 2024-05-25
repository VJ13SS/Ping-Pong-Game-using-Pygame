import pygame

#In the code 1 means the items at the bottom and 2 means the items at the top

#initialization
pygame.init()

HEIGHT = 2160
WIDTH = 1060

#window
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
WIN_COLOR = (255,255,255)

#score parameters
#scorefont
S_FONT = pygame.font.SysFont('comicsans',150)
COLOR = (255,85,0)
SCORE_X = 50#X coordinate
#Ycoordinates
SCORE_Y_1 = HEIGHT //2 +50
SCORE_Y_2 = HEIGHT //2 -150


#button parameters
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 150
BUTTON_COLOR = (58, 232, 7)
BUTTON_FONT = pygame.font.SysFont('comicsans',100)
BUTTON_X = 100# Starting x coordinate
BUTTON_Y = 70# Starting y coordinate
BUTTON_GAP_X = 750#horizontal seperation between buttons
BUTTON_GAP_Y = 1900#vertical seperation between buttons

#paddle parameters
PADDLE_WIDTH = 270
PADDLE_HEIGHT = 70
PADDLE_COLOR = (10,8,6)
PADDLE_X = 60
L_P_Y = 250#y coordinate of left paddle(1 paddle)
PADDLE_GAP = 1600#Gap between both the paddles



#control buttons
class buttons:
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		
	def draw_button(self,WIN):
		pygame.draw.rect(WIN,BUTTON_COLOR,(self.x,self.y,self.width,self.height))
		
	def write_text(self,WIN,text,flip_h,flip_v):
		text = BUTTON_FONT.render(f'{text}',1,(255,0,5))
		text_label = pygame.transform.flip(text,flip_h,flip_v)
		
		pos_x = (self.width//2 + self.x) - 20
		pos_y = (self.height//2 + self.y) - 20
		
		WIN.blit(text_label,(pos_x,pos_y))


#to control the paddles
class paddles:
	VEL = 10#Velocity
	def  __init__(self,x,y,width,height):
		self.x = x #x coordinate
		self.y = y #y coordinate
		self.width = width #width of rectangle
		self.height = height #height of rectangle
		
	def draw_paddles(self,WIN):	
		pygame.draw.rect(WIN,PADDLE_COLOR,(self.x,self.y,self.width,self.height))
		
	def move_paddles(self,WIN,forward):	
		if forward and self.x <= 780:
			self.x += self.VEL
		elif not(forward) and self.x >=40:
			self.x -= self.VEL

#Ball
class Ball:
	X_VEL = 7#velocity of X axis
	Y_VEL = 5#velocity of y axis
	RADIUS = 30
	def __init__(self,x,y):
		#coordinates at the centet
		self.x = x + self.RADIUS
		self.y = y + self.RADIUS
	
	def draw(self,WIN):
		pygame.draw.circle(WIN,(80,150,180),(self.x,self.y),self.RADIUS)
		
	def reset(self):
		self.x = WIDTH//2
		self.y = HEIGHT//2
	def move(self,paddle_1,paddle_2):
		self.y += self.Y_VEL
		self.x += self.X_VEL
		
		#Border collissions
		#After collission the ball moves in oppossite direction the directions of the ball is influenced by the change made on the velocities and will continue till the next updation
		#has some complicated logic understand it by writing/sketching on a paper
		
		#self.VEL values are gives by considering their previous states
		if self.x >= WIDTH or self.x < 30:
			self.X_VEL *=-1#change direction
			#self.x_Velocity multiplied by -1 - makes it +ve if was negative and makes it -ve if was positive
		elif self.y >= HEIGHT or self.y <=0:			
			self.Y_VEL *=-1
		
		#self.VEL values are gives by considering their previous states which allows the ball to moves in either a clockwise or anticlockwise direction
		#paddle 1 - bottom paddle
		elif self.y == paddle_1.y and paddle_1.x <= self.x <= paddle_1.x + PADDLE_WIDTH:		
			self.Y_VEL *=-1#change direction
			
		#paddle 2 top paddle
		#the rectangle is drawn from top to bottom...so to get the bottom part of the top paddle where the bapl collides we need to add the paddle height with its coordinates
		elif self.y == paddle_2.y  + PADDLE_HEIGHT and paddle_2.x <= self.x <= (paddle_2.x + PADDLE_WIDTH):
			self.Y_VEL *=-1#change direction

#draw board
def draw_board(WIN):
	#statically determined the coordinates
	pygame.draw.line(WIN,(0,0,255),(30,HEIGHT//2),(WIDTH,HEIGHT//2),10)
	pygame.draw.line(WIN,(0,0,255),(30,10),(WIDTH,10),10)
	pygame.draw.line(WIN,(0,0,255),(30,HEIGHT),(WIDTH,2160),10)
	pygame.draw.line(WIN,(0,0,255),(30,10),(30,HEIGHT),10)
	pygame.draw.line(WIN,(0,0,255),(WIDTH,10),(WIDTH,HEIGHT),10)

#draw circle at center
def draw_circle(WIN,color,radius):
	pygame.draw.circle(WIN,color,(WIDTH//2 + 10,HEIGHT//2),radius)
	
#write scores
def write_score(WIN,text,X,Y,flip_h,flip_v):
	#flip_h --> Set  True  to rotate text horizontally
	#flip_v --> Set  True  to rotate text vertically
	#To inverse the text set flip_h and flip_v to true
	text = S_FONT.render(f'{text}',1,COLOR)
	text_label = pygame.transform.flip(text,flip_h,flip_v)
	WIN.blit(text_label,(X,Y))

def main():
	run = True#variable to control the loop
	
	#initializing scores
	score_1 = 0
	score_2 =  0

	#ball
	ball = Ball(WIDTH//2,HEIGHT//2)
	
	#paddles
	paddle_2 = paddles(PADDLE_X,L_P_Y,PADDLE_WIDTH,PADDLE_HEIGHT)
	paddle_1 = paddles(PADDLE_X,(L_P_Y + PADDLE_GAP),PADDLE_WIDTH,PADDLE_HEIGHT)
	
	#left buttons
	left_button_1_y = BUTTON_Y +BUTTON_GAP_Y
	left_button_1 = buttons(BUTTON_X,left_button_1_y,BUTTON_WIDTH,BUTTON_HEIGHT)#bottom left corner button
	
	left_button_2_x =BUTTON_X +BUTTON_GAP_X
	left_button_2 = buttons(left_button_2_x,BUTTON_Y,BUTTON_WIDTH,BUTTON_HEIGHT)#top right corner button
	
	#right buttons
	right_button_1_x = BUTTON_X +BUTTON_GAP_X
	right_button_1_y = BUTTON_Y +BUTTON_GAP_Y
	right_button_1 = buttons(right_button_1_x,right_button_1_y,BUTTON_WIDTH,BUTTON_HEIGHT)#bottom right corner button
	
	right_button_2 = buttons(BUTTON_X,BUTTON_Y,BUTTON_WIDTH,BUTTON_HEIGHT)#Top left corner button
	
	clock = pygame.time.Clock()
	
	#initializing movement
	move = None
	
	while run:
		clock.tick(160)#the process runs at 160 FPS per second
		
		WIN.fill(WIN_COLOR)
		
		#drawing a line
		draw_board(WIN)
		
		#drawing circles
		#statically determined the coordinates
		draw_circle(WIN,(0,0,255),150)
		draw_circle(WIN,(255,255,255),140)
		draw_circle(WIN,(0,0,255),80)
		draw_circle(WIN,(255,255,255),70)
		
		#writing scores
		write_score(WIN,score_1,SCORE_X,SCORE_Y_1,False,False)
		
		write_score(WIN,score_2,SCORE_X,SCORE_Y_2,True,True)
		
		#drawing the ball
		ball.draw(WIN)
		
		#drawing paddles
		paddle_1.draw_paddles(WIN)#At the bottom
		paddle_2.draw_paddles(WIN)#At the top
		
		#drawing buttons
		#Bottom Buttons --> Button 1
		#Top Buttons --> Button 2
		left_button_1.draw_button(WIN)
		left_button_2.draw_button(WIN)
		
		right_button_1.draw_button(WIN)
		right_button_2.draw_button(WIN)
		
		#Drawing text on buttons
		right_button_1.write_text(WIN,'R',False,False)
		left_button_1.write_text(WIN,'L',False,False)
		left_button_2.write_text(WIN,'L',True,True)
		right_button_2.write_text(WIN,'R',True,True)
		
		#moving the ball
		ball.move(paddle_1,paddle_2)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x,mouse_y = pygame.mouse.get_pos()
				move = True
			if event.type == pygame.MOUSEBUTTONUP:
				move = False
				
		if move:			
			#bottom left corner button
			if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and left_button_1_y <= mouse_y <= left_button_1_y + BUTTON_HEIGHT:
				#move paddle 1 left
				paddle_1.move_paddles(WIN,False)
			
			#bottom right corner button
			elif right_button_1_x <= mouse_x <= right_button_1_x + BUTTON_WIDTH and right_button_1_y <= mouse_y <= right_button_1_y + BUTTON_HEIGHT:
				#move paddle 1 right
				paddle_1.move_paddles(WIN,True)				
			#Top left corner button
			elif BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
				#move paddle 2 right
				paddle_2.move_paddles(WIN,False)
			
			#Top right corner button
			elif left_button_2_x <= mouse_x <= left_button_2_x + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
				#move paddle 2 left
				paddle_2.move_paddles(WIN,True)
				
		#updating the scores if the ball crosses the paddles
		if ball.y >(paddle_1.y + PADDLE_HEIGHT):
			score_2+=1#updatig score of paddle 2
			
			ball.reset()#Reseting the ball position
		elif ball.y < paddle_2.y:
			score_1+=1#updatig score of paddle 1
		
			ball.reset()
				
		pygame.display.update()
				
	pygame.quit()
	
if __name__ == '__main__':
	main()