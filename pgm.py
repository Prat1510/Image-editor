# name: File path of the pgm image file
# Output is a 2D list of integers
import math
def readpgm(name):
	image = []
	with open(name) as f:
		lines = list(f.readlines())
		if len(lines) < 3:
			print("Wrong Image Format\n")
			exit(0)

		count = 0
		width = 0
		height = 0
		for line in lines:
			if line[0] == '#':
				continue

			if count == 0:
				if line.strip() != 'P2':
					print("Wrong Image Type\n")
					exit(0)
				count += 1
				continue

			if count == 1:
				dimensions = line.strip().split(' ')
				print(dimensions)
				width = dimensions[0]
				height = dimensions[1]
				count += 1
				continue

			if count == 2:	
				allowable_max = int(line.strip())
				if allowable_max != 255:
					print("Wrong max allowable value in the image\n")
					exit(0)
				count += 1
				continue

			data = line.strip().split()
			data = [int(d) for d in data]
			image.append(data)
	return image	

# img is the 2D list of integers
# file is the output file path
def writepgm(img, file):
	with open(file, 'w') as fout:
		if len(img) == 0:
			pgmHeader = 'p2\n0 0\n255\n'
		else:
			pgmHeader = 'P2\n' + str(len(img[0])) + ' ' + str(len(img)) + '\n255\n'
			fout.write(pgmHeader)
			line = ''
			for i in img:
				for j in i:
					line += str(j) + ' '
				line += '\n'
			fout.write(line)

def pv(i,j,image):
	if len(image)-1>i>0 and len(image[0])-1>j>0:
		return int(round((image[i-1][j-1]+image[i-1][j]+image[i-1][j+1]+image[i][j- 1]+image[i][j]+image[i][j+1]+image[i+1][j-1]+ image[i+1][j]+image[i+1][j+1])/9))
	else:
		return image[i][j]

def averagingfilter(img):
	col=len(img)
	row=len(img[0]) 
	M=[[0 for i in range(row)] for i in range(col)]
	for i in range (0,col):
		for j in range (0,row):
			M[i][j]=pv(i,j,img)
	return M	


def edgedetection(image):
	col=len(image)
	row=len(image[0]) 
	grad=[[0 for i in range(row)] for i in range(col)]
	for i in range (1,col-1):
		for j in range (1,row-1):
			hdif=(image[i-1][j-1]-image[i-1][j+1]) + 2*(image[i][j-1]-image[i][j+1]) + (image[i+1][j-1]- image[i+1][j+1])
			vdif=(image[i-1][j-1]-image[i+1][j-1]) + 2*(image[i-1][j]-image[i+1][j]) + (image[i-1][j+1]- image[i+1][j+1])
			b=round(math.sqrt(hdif**2 + vdif**2))
			grad[i][j]=b
	
	for j in range(1,row-1):
		i=0
		hdif= 2*(image[i][j-1]-image[i][j+1]) + (image[i+1][j-1]- image[i+1][j+1])
		vdif=(-image[i+1][j-1]) + 2*(-image[i+1][j]) + (- image[i+1][j+1])
		b=round(math.sqrt(hdif**2 + vdif**2))
		grad[0][j]=b
	for j in range (1,row-1):
		i=col-1
		hdif=(image[i-1][j-1]-image[i-1][j+1]) + 2*(image[i][j-1]-image[i][j+1]) 
		vdif=image[i-1][j-1] + 2*(image[i-1][j]) + (image[i-1][j+1])
		b=round(math.sqrt(hdif**2 + vdif**2))
		grad[-1][j]=b
	for i in range(1,col-1):
		j=0
		hdif=(-image[i-1][j+1]) + 2*(-image[i][j+1]) + (- image[i+1][j+1])
		vdif=2*(image[i-1][j]-image[i+1][j]) + (image[i-1][j+1]- image[i+1][j+1])
		b=round(math.sqrt(hdif**2 + vdif**2))
		grad[i][0]=b
	for i in range (1,col-1):
		j=row-1
		hdif=(image[i-1][j-1]) + 2*(image[i][j-1]) + (image[i+1][j-1])
		vdif=(image[i-1][j-1]-image[i+1][j-1]) + 2*(image[i-1][j]-image[i+1][j]) 
		b=round(math.sqrt(hdif**2 + vdif**2))
		grad[i][-1]=b
	i,j=0,0
	grad[0][0]=round(math.sqrt(((2*(-image[i][j+1]))+(-image[i+1][j+1]))**2 + (2*(-image[i+1][j]) + (- image[i+1][j+1]))**2)) 
	i,j=0,len(image[0])-1
	grad[0][-1]=round(math.sqrt(((2*(image[i][j-1]))+(image[i+1][j-1]))**2 + (2*(-image[i+1][j]) + (- image[i+1][j-1]))**2))
	i,j=len(image)-1,0
	grad[-1][0]=round(math.sqrt(((2*(-image[i][j+1]))+(-image[i-1][j+1]))**2 + (2*(image[i-1][j]) + (image[i-1][j+1]))**2))
	i,j=len(image)-1,len(image[0])-1
	grad[-1][-1]=round(math.sqrt(((2*(image[i][j-1]))+(image[i-1][j-1]))**2 + (2*(image[i-1][j]) + (image[i-1][j-1]))**2))
	max=grad[0][0]
	for i in range (0,col):
		for j in range (0,row):
			if grad[i][j]>max:
				max=grad[i][j]	
	for i in range (0,col):
		for j in range (0,row):
			grad[i][j]=int((round((grad[i][j]*255)/max)))		
	return grad



def colormin(i,j,image):
	
	
	if i==0:
		return 
	else:
		if 0<j<len(image[0])-1:
			a=min(image[i-1][j-1], image[i-1][j], image[i-1][j+1])
			if image[i-1][j-1]==a:
				if (i-1,j-1) not in M:
					M.add((i-1,j-1))
					colormin(i-1,j-1,image)
			if image[i-1][j]==a:
				if (i-1,j) not in M:
					M.add((i-1,j))
					colormin(i-1,j,image)
			if image[i-1][j+1]==a:
				if (i-1,j+1) not in M:
					M.add((i-1,j+1))
					colormin(i-1,j+1,image)		
		elif j==0:
			a=min(image[i-1][j], image[i-1][j+1])
			if image[i-1][j]==a:
				if (i-1,j) not in M:
					M.add((i-1,j))
					colormin(i-1,j,image)
			if image[i-1][j+1]==a:
				if (i-1,j+1) not in M:
					M.add((i-1,j+1))
					colormin(i-1,j+1,image)
		else:
			a=min(image[i-1][j-1], image[i-1][j])
			if image[i-1][j-1]==a:
				if (i-1,j-1) not in M:
					M.add((i-1,j-1))
					colormin(i-1,j-1,image)
			if image[i-1][j]==a:
				if (i-1,j) not in M:
					M.add((i-1,j))
					colormin(i-1,j,image)

def MinimumEnergy(img,Image):
	image=[[0 for i in range(len(img[0]))] for i in range(len(img))]
	for j in range(0,len(image[0])):	
		image[0][j]=img[0][j]
	for i in range (1,len(image)):
		for j in range(1,len(image[0])-1):
			image[i][j]=img[i][j] + min(image[i-1][j-1], image[i-1][j], image[i-1][j+1])
		image[i][0]=img[i][0] + min(image[i-1][0], image[i-1][1])
		image[i][-1]=img[i][-1] + min(image[i-1][-1], image[i-1][-2])
	Min=min(image[-1])
	L=[image[-1].index(Min)]
	for j in range(L[0]+1,len(image[0])):
		if image[-1][j]==Min:
			L.append(j)
	global M
	M=set([])
	for j in L:
		colormin(len(image)-1,j,image)
		Image[-1][j]=255
	for i in M:
		a=i[0]
		b=i[1]
		Image[a][b]=255			
	return Image

########## Function Calls ##########
x = readpgm('test.pgm')			# test.pgm is the image present in the same working directory
writepgm(x, 'test_o.pgm')		# x is the image to output and test_o.pgm is the image output in the same working directory
###################################
y= averagingfilter(x)
writepgm(y,'average.pgm')
###################################
z=edgedetection(x)
writepgm(z,'edge.pgm')
###################################
x=readpgm('test.pgm')
writepgm(MinimumEnergy(z,x),'minenergy.pgm')
##############################################
##############################################
x = readpgm('test1.pgm')			# test.pgm is the image present in the same working directory
writepgm(x, 'test_o1.pgm')		# x is the image to output and test_o.pgm is the image output in the same working directory
###################################
y= averagingfilter(x)
writepgm(y,'average1.pgm')
###################################
z=edgedetection(x)
writepgm(z,'edge1.pgm')
###################################
x=readpgm('test1.pgm')
writepgm(MinimumEnergy(z,x),'minenergy1.pgm')
