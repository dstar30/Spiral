import sys, random, argparse
import numpy as np 
import turtle
import math
# Pillow, a Python IMaging Library for saving the spiro images
from PIL import Image
from datetime import datetime
from fractions import gcd



#d draw the circle using turtle
# def drawCircleTurtle(x, y, r):
# 	# move to the start of a circle
# 	# .up takes the "pen off the virtual paper" so it won't draw as you move the turtle
# 	turtle.up()
# 	turtle.setpos(x+r, y)
# 	turtle.down()

# 	# draw the circle
# 	for i in range(0, 365, 5):
# 		# convert degree to radins (most computer programs require radians for angle-based calculations)
# 		a = math.radians(i)
# 		turtle.setpos(x + r*math.cos(a), y + r*math.sin(a))

# drawCircleTurtle(100, 100, 50)

# # mainloop() keeps the tkinter window open so you can see the circle
# # tkinter is the default GUI library used by Python
# turtle.mainloop()

class Spiro:
	# constructor
	def __init__(self, xc, yc, col, R, r, l):

		self.t = turtle.Turtle() # turtle object
		self.t.shape('turtle') # cursor shape
		self.step = 5 # step in degrees
		self.drawingComplete = False

		# parameters
		self.setparams(xc, yc, col, R, r, l)

		self.restart()

	def setparams(self, xc, yc, col, R, r, l):
		self.xc = xc
		self.yc = yc
		self.col = col
		self.R = int(R)
		self.r = int(r)
		self.l = l

		# reduce r/R to smallest form
		gcdVal = gcd(self.r, self.R)
		self.nRot = self.r//gcdVal

		self.k = r/float(R)
		self.t.color(*col)

		# current angle
		self.a = 0

	def restart(self):
		self.drawingComplete = False
		self.t.showturtle()
		self.t.up()

		R, k, l = self.R, self.k, self.l
		a = 0.0

		x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
		y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))
		self.t.setpos(self.xc + x, self.yc + y)
		self.t.down()

	def draw(self):
		# draw the rest of the points
		R, k, l = self.R, self.k, self.l
		for i in range(0, 360*self.nRot + 1, self.step):
			a = math.radians(i)
			x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
			y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))
			self.t.setpos(self.xc + x, self.yc + y)

			# done drawing
		self.t.hideturtle()

	# update one step
	def update(self):
		if self.drawingComplete:
			return

		self.a += self.step
		R, k, l = self.R, self.k, self.l
		a = math.radians(self.a)
		x = self.R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
		y = self.R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))
		self.t.setpos(self.xc + x, self.yc + y)

		# set flag if drawing is complete
		if self.a >= 360 * self.nRot:
			self.drawingComplete = True
			self.hideturtle()

	def clear(self):
		self.t.clear()


class SpiroAnimator:

	def __init__(self, N):
		self.deltaT = 10

		self.width = turtle.window_width()
		self.height = turtle.window_height()

		self.spiros = []
		for i in range(N):
			# generate random parameters
			rparams = self.genRandomParams()
			spiro = Spiro(*rparams)
			self.spiros.append(spiro)
			turtle.ontimer(self.update, self.deltaT)

	def genRandomParams(self):
		width, height = self.width, self.height
		R = random.randint(50, min(width, height)//2)
		# set r between 10 and 90% of R
		r = random.randint(10, 9*R//10)
		# random fraction between 0.1 and 0.9
		l = random.uniform(0.1, 0.9)
		# find random (x,y) as center
		xc = random.randint(-width//2, width//2)
		yc = random.randint(-height//2, height//2)
		col = (random.random(), random.random(), random.random())
		return (xc, yc, col, R, r, l)


	# restart spiro drawing
	def restart(self):
		for spiro in self.spiros:
			spiro.clear()
			rparams = self.genRandomParams()
			spiro.setparams(*rparams)
			spiro.restart()

	def update(self):
		nComplete = 0
		for spiro in self.spiros:
			spiro.update()
			if spiro.drawingComplete:
				nComplete += 1

		if nComplete == len(self.spiros):
			self.restart()

		turtle.ontimer(self.update, self.deltaT)

	# toggle the turtle cursor on and off to make the drawing go faster
	def toggleTurtles(self):
		for spiro in self.spiros:
			if spiro.t.isvisible():
				spiro.t.hideturtle()
			else:
				spiro.t.showturtle()


# save as PNG
def saveDrawing():
	turtle.hideturtle()
	dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
	fileName = 'spiro-' + dateStr
	print('Saving drawing to %s.eps/png' % fileName)

	# get the tkinter canvas and save the window in the Embedded PostScript (EPS) file format
	# EPS is vector based
	canvas = turtle.getcanvas()
	canvas.postscript(file = fileName + '.eps')

	img = Image.open(fileName + '.eps')
	img.save(fileName + '.png', 'png')

	turtle.showturtle()


def main():
	print('generating spirograph...')
	descStr = """This program draws Spirographs using the Turtle module.
	When run with no arguments, this program draws random spirographs."
	"""

	parser = argparse.ArgumentParser(description = descStr)
	parser.add_argument('--sparams', nargs = 3, dest = 'sparams', required = False, help = "The three arguments in sparams: R, r, l.")

	args = parser.parse_args()

	turtle.setup(width = 0.8)
	turtle.shape('turtle')
	turtle.title("Spirographs!")
	turtle.onkey(saveDrawing, "s")
	turtle.listen()

	turtle.hideturtle()

	if args.sparams:
		params = [float(x) for x in args.sparams]
		col = (0.0, 0.0, 0.0)
		spiro = Spiro(0, 0, col, *params)
		spiro.draw()
	else:
		spiroAnimator = SpiroAnimator(4)
		turtle.onkey(spiroAnimator.toggleTurtles, "t")
		turtle.onkey(spiroAnimator.restart, "space")

	turtle.mainloop()

if __name__ == '__main__':
	main()

