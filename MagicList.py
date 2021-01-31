class MagicList :
	def __init__(self):
		self.data = [0]

	def findMin(self):
		M = self.data
		''' you need to find and return the smallest
			element in MagicList M.
			Write your code after this comment.
		'''
		if len(M)>1:
			return M[1]
		else:
			return None	
	
	def insert(self, E):
		M = self.data
		''' you need to insert E in MagicList M, so that
			properties of the MagicList are satisfied. 
			Return M after inserting E into M.
			Write your code after this comment.
		'''
		M.append(E)
		a=len(M)-1
		for i in range(a,0,-1) :
			j=i
			while  M[j]<M[j//2] and j>0:
				M[j],M[j//2]=M[j//2],M[j]
				j=j//2
		return M	

	def deleteMin(self):
		M = self.data
		''' you need to delete the minimum element in
			MagicList M, so that properties of the MagicList
			are satisfied. Return M after deleting the 
			minimum element.
			Write your code after this comment.
		'''
		E2=M[-1]
		M[1],M[-1]=M[-1],M[1]
		M.pop()
		j=1
		while 2*j < len(M): 
			if 2*j+1<len(M):
				if M[2*j]<=M[2*j+1]<=M[j]:
					M[j],M[2*j]=M[2*j],M[j]
					j=2*j
				elif M[2*j+1]<=M[2*j]<=M[j]:
					M[j],M[2*j+1]=M[2*j+1],M[j]
					j=2*j+1			
				elif M[2*j]<=M[j]<=M[2*j+1]:
					M[j],M[2*j]=M[2*j],M[j]
					j=2*j
				elif M[2*j+1]<=M[j]<=M[2*j]:
					M[j],M[2*j+1]=M[2*j+1],M[j]
					j=2*j +1
				else:
					break
			else:
				if M[j]>M[2*j]:
					M[j],M[2*j]=M[2*j],M[j]
				break			
		return M


def K_sum(L,K):
	''' you need to find the sum of smallest K elements
		of L using a MagicList. Return the sum.
		Write your code after this comment.
	'''
	M = MagicList() 
	for i in L : 
		M.insert(i) 
	sum=0
	for i in range(K):
		sum+=M.findMin()
		M.deleteMin()	
	return sum

if __name__ == "__main__" :
	'''Here are a few test cases'''
	
	'''insert and findMin'''
	M = MagicList()
	M.insert(4)
	M.insert(3)
	M.insert(5)
	x = M.findMin()
	if x == 3 :
		print("testcase 1 : Passed")
	else :
		print("testcase 1 : Failed")
		
	'''deleteMin and findMin'''
	M.deleteMin()
	x = M.findMin()
	if x == 4 :
		print("testcase 2 : Passed")
	else :
		print("testcase 2 : Failed")
		
	'''k-sum'''
	L = [2,5,8,3,6,1,0,9,4]
	K = 4
	x = K_sum(L,K)
	if x == 6:
		print("testcase 3 : Passed")
	else :
		print("testcase 3 : Failed")

	'''extra testcase'''
	A=[1,5,6,8,2,6,1,3,4,6,7,9,2,1,4,0,2,2]
	K=6
	x=K_sum(A,K)
	if x==7:
		print("testcase 4 : Passed")
	else :
		print("testcase 4 : Failed")	



