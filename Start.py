import time
import os

def main():
    data = os.system("Source.py")
    if data == 1:
        print "[ERROR] Port Error, restart in 10 seconds"
        time.sleep(10)
        os.system("cls")
        main()
    elif data in [5,1280]:
        print "[INFO] Server Stopped!"
        raw_input("")
    elif data in [11,2816]:
        print "[ERROR] Server Port error, restarting server in 10 seconds"
        time.sleep(1)
        print "[ERROR] Server Port error, restarting server in 9 seconds"
        time.sleep(1)
        print "[ERROR] Server Port error, restarting server in 8 seconds"
        time.sleep(1)
        print "[ERROR] Server Port error, restarting server in 7 seconds"
        time.sleep(1)
        print "[ERROR] Server Port error, restarting server in 6 seconds"
        time.sleep(1)
        print "[ERROR] Server Port error, restarting server in 5 seconds"
        time.sleep(1)
        print "[ERROR] Server Port error, restarting server in 4 seconds"
        time.sleep(1)
        print "[ERROR] Server Port error, restarting server in 3 seconds"
        time.sleep(1)
        print "[ERROR] Server Port error, restarting server in 2 seconds"
        time.sleep(1)
        print "[ERROR] Server Port error, restarting server in 1 seconds"
        time.sleep(1)
        os.system("cls")
        main()
    else:
        print "[ERROR] Server Crashed, restart in 20 seconds."
        time.sleep(20)
        os.system("cls")
        main()

if __name__=="__main__":
    main()
