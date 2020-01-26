def find_p(grid,n):
	for i in range(n):
		if 'p' in grid[i]:
			x = i
			y = grid[i].index('p')
			return x,y

def manhathan_distance(x1,y1,x2,y2):
	return abs(x1-x2) + abs(y1-y2)

def nextMove(n,r,c,grid):
	x_p,y_p = find_p(grid,n)
	x_m,y_m = r,c
	options = [
		[(x_m+1,y_m),"DOWN"],
		[(x_m-1,y_m),"UP"],
		[(x_m,y_m+1),"RIGHT"],
		[(x_m,y_m-1),"LEFT"],
	]
	results=[]
	for positions,direction in options:
		x,y  = positions
		if not (x<0 or x > n-1 or y<0 or y> n-1):
			results.append((manhathan_distance(x_p,y_p,x,y),direction))
	best = min(results)
	return best[1] # best[0] direction positions, best[1] direction string

n = int(input())
r,c = [int(i) for i in input().strip().split()]
grid = []
for i in range(0, n):
	grid.append(input())

print(nextMove(n,r,c,grid))