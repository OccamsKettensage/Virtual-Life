def Magic(func, param): #magic's the program which determines if the func will terminate with param as the input, ie solution to halting problem
	return "the boolean if func stops with param"

def P(J):
	if Magic(J, J) == True: #stops
		while True:
			print "P is not stopping"
	else: #doesn't stop
		print "P stops"

print P(P)

"Write an program that identifies (from the video of the fight) & plots mma footwork, recognizes the patterns, and predicts movement"