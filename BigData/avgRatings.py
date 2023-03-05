from mrjob.job import MRJob
from mrjob.step import MRStep

class avgRating(MRJob):
	def steps(self):
		return [
			MRStep(mapper=self.mapper,reducer=self.reducer)
			]
	def mapper(self,_,l):
		uID,mID,Rat,ts = l.split('\t')
		mID = int(mID)
		Rat = int(Rat)
		yield (mID,Rat)
	def reducer(self,k,v):
		v = list(v)
		yield (k,sum(v)/len(v))

if __name__=='__main__':
	avgRating.run()
