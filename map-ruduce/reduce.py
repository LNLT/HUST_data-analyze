import sys
import threading
import time

def run(readfile, writefile):
    file = open(readfile)
    write = open(writefile, 'w')
    count_dict = {}
    for line in file:
        line = line.strip()
        word, count = line.split(',', 1)
        try:
            count = int(count)
        except ValueError:
            continue
        if word in count_dict.keys():
            count_dict[word] = count_dict[word] + count
        else:
            count_dict[word] = count

    count_dict = sorted(count_dict.items(), key=lambda x: x[0], reverse=False)
    for key, v in count_dict:
        write.write("{},{}\n".format(key, v))

if __name__ == '__main__':
    t1 = threading.Thread(target=run('shuffle1', 'reduce01'), args=("t1",))
    t2 = threading.Thread(target=run('shuffle2', 'reduce02'), args=("t2",))
    t3 = threading.Thread(target=run('shuffle3', 'reduce03'), args=("t3",))
    start = time.clock()
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    print("t1 cost %s s" % (time.clock() - start))
    t2.join()
    print("t2 cost %s s" % (time.clock() - start))
    t3.join()
    print("t3 cost %s s" % (time.clock() - start))