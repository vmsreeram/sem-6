from mrjob.job import MRJob
from mrjob.step import MRStep

class Ratings(MRJob):
	def steps(self):
		return [
			MRStep(mapper=self.mapr,reducer=self.redr)
			]
	def mapr(self,_,l):
		uId,mID,R,t = l.split('\t')
		R=int(R)
		mID=int(mID)	
		yield (R,1)
	def redr(self,k,v):
		v=list(v)
		yield (k,sum(v))

if __name__=='__main__':
	Ratings.run()
