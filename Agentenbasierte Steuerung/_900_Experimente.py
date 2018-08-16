import time 

def Warteschleife(q):
    print("Warteschleife läuft")

    while True:
        if q.empty() is False:
            print("Moving >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>: " + str(q.get()))
        time.sleep(2)