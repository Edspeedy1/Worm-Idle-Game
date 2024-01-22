import random, math

def doStreak(runLength, totalLength):
    streak = 0
    previos = 0
    for i in range(totalLength):
        flip = random.randint(0, 1)
        if flip == previos:
            streak += 1
            if streak == runLength: return 1
        else: 
            streak = 1
            previos = flip
    return 0

trials = 100000
count = 0
for _ in range(trials):
    count += doStreak(10,100)
print(count/trials)