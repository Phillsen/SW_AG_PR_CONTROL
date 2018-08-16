import multiprocessing
import _900_Experimente
import time
import random


if __name__ == '__main__':
    q = multiprocessing.Queue()
    Test = multiprocessing.Process(target=_900_Experimente.Warteschleife, args=(q,))
    Test.start()
    
    while True:
        Randomnumber = random.randrange(1,50)
        print("in >>>>>>>>>>>>>>>>>>>>>>>" + str(Randomnumber))
        q.put(Randomnumber)
        time.sleep(random.randrange(0,4))

