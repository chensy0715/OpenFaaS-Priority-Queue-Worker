import random, threading, time, requests
#
success = 0
fail = 0
execute_time = []

def test():
    start_time = time.time()
    temp = random.randint(0, 100)
    # print(temp)
    global success, fail
    try:
        a = requests.post('http://127.0.0.1:8080/function/figlet', data=str(temp)).text
        print(a)
        success += 1
        execute_time.append(time.time() - start_time)
        # print('success', success)
    except Exception as e:
        fail += 1
        # print('fail', fail)
        # count += 1

if __name__ == '__main__':

    t = []
    for i in range(500):
        t1 = threading.Thread(target=test)
        t.append(t1)

    for i in t:
        i.start()

    for i in t:
        i.join()

    print(success, fail, execute_time)
    print(sum(execute_time)/len(execute_time))