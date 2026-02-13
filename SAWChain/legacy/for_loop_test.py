import numpy as np

N=10
rep = 0

orderedArray = np.arange(1,N)

print(orderedArray)

while rep < N:
    shuffledArray = np.random.permutation(orderedArray)
    print(shuffledArray)
    for i in range(N-1):
        print(shuffledArray[i])
    rep+=1

