#!/usr/bin/env python3
import sys
import threading
import time

def read_input(file):
    for line in file:
        line = line.strip()
        yield line.split(', ')

def run(readfile, writefile):
    file = open(readfile)
    write = open(writefile, 'w')
    lines = read_input(file)
    with write as f:
        for words in lines:
            for word in words:
                f.write("{},{}\n".format(word, 1))

if __name__ == '__main__':
    t1 = threading.Thread(target=run('source01', 'map01'), args=("t1",))
    t2 = threading.Thread(target=run('source02', 'map02'), args=("t2",))
    t3 = threading.Thread(target=run('source03', 'map03'), args=("t3",))
    t4 = threading.Thread(target=run('source04', 'map04'), args=("t4",))
    t5 = threading.Thread(target=run('source05', 'map05'), args=("t5",))
    t6 = threading.Thread(target=run('source06', 'map06'), args=("t6",))
    t7 = threading.Thread(target=run('source07', 'map07'), args=("t7",))
    t8 = threading.Thread(target=run('source08', 'map08'), args=("t8",))
    t9 = threading.Thread(target=run('source09', 'map09'), args=("t9",))
    start = time.clock()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t1.join()
    print("t1 cost %s s" % (time.clock()-start))
    t2.join()
    print("t2 cost %s s" % (time.clock() - start))
    t3.join()
    print("t3 cost %s s" % (time.clock() - start))
    t4.join()
    print("t4 cost %s s" % (time.clock() - start))
    t5.join()
    print("t5 cost %s s" % (time.clock() - start))
    t6.join()
    print("t6 cost %s s" % (time.clock() - start))
    t7.join()
    print("t7 cost %s s" % (time.clock() - start))
    t8.join()
    print("t8 cost %s s" % (time.clock() - start))
    t9.join()
    print("t9 cost %s s" % (time.clock() - start))