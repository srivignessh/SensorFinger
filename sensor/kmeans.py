import math
import random
import numpy as np

def load_data(infile):
	data=open(infile);
	lines=data.readlines()
	samples=[];
	for line in lines:
		line=line.strip()
		line=line.split(' ')
		line=filter(None,line)
		line=map(float,line)
		value=(line) 
		samples.append(line)
	return samples

def euclideanDistance(sample, center, dim,i):
	distance = 0
	for x in range(dim):
		distance += pow((sample[x] - center[x]), 2)
	return math.sqrt(distance)

def sumsqr(sample,C,dim):
	sumsq=0;
	for x in range(dim):
		sumsq += pow((sample[x] - C[x]), 2)
	return sumsq

def kmeans(samples, k, maxIter,TOL):
	
	C = random.sample(samples, k)
	Iter = 0;
	SS_p=0;
	vectors_num=len(samples)
	P=[0]*vectors_num
	dim=len(samples[0])
	while 1:
		# find closest point
		for i in range(vectors_num):
			minIdx = 0;
			minVal = euclideanDistance(samples[i],C[0],dim,i)
			for j in range(k):
				dist = euclideanDistance(samples[i],C[j],dim,i)
				if (dist < minVal):
					minIdx = j;
					minVal = dist;
			# assign point to the closter center
			P[i] = minIdx;

		for j in range(k):
			coords=[samples[i] for i in range(len(P)) if P[i]==j]
			unzipped = zip(*coords)
			num=len(coords)
			C[j] = [math.fsum(dList)/num for dList in unzipped]
		SS_error = 0;
		
		for idx in range(vectors_num):
			SS_error = SS_error + sumsqr(samples[idx],C[P[idx]],dim);
			
		Iter = Iter + 1;
		delta=abs(SS_error-SS_p);

		if (delta < TOL):
			break;
		
		SS_p=SS_error;
		if Iter > maxIter:
			Iter = Iter - 1;
			break;
		

	SSE=SS_error;
	return SSE

AVGSSE=[0]*3;
samples=load_data("seeds.txt");
k=[3,5 ,7];
Tol=0.001;
Iter=100;
for t in range(3):
	TSSE=0;
	for i in range(10):
		SSE = kmeans(samples, k[t], Iter,Tol)
		TSSE =TSSE + SSE;

	AVGSSE[t]=TSSE/10;
print AVGSSE;