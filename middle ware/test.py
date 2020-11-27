# # from xmlrpclib import ServerProxy
from xmlrpc.client import ServerProxy
import random, threading, time
#
success = 0
fail = 0
execute_time = []

def test(svr):
    start_time = time.time()
    temp = random.randint(0, 100)
    # print(temp)
    global success, fail
    try:
        a = svr.addRequest(['A', 'http://127.0.0.1:8080/function/figlet', temp]) #Remote invoking the server's function
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
        svr = ServerProxy("http://0.0.0.0:6666")  # connect to server
        t1 = threading.Thread(target=test, args=[svr])
        t.append(t1)

    for i in t:
        i.start()

    for i in t:
        i.join()

    print(success, fail, execute_time)
    print(sum(execute_time)/len(execute_time))

    # a = svr.addRequest(['A', 1, random.randint(0, 100)])  # Remote invoking the server's function
    # print(a)

# import xmlrpc.client
# from concurrent.futures import ThreadPoolExecutor, as_completed
#
# def submit_sleep():
#    server = xmlrpc.client.ServerProxy("http://localhost:6666/", allow_none=True)
#    return server.addRequest(['A', 1, random.randint(0, 100)])
#
# with ThreadPoolExecutor() as executor:
#     sleeps = {executor.submit(submit_sleep) for _ in range(6)}
#     for future in as_completed(sleeps):
#         sleep_time = future.result()
#         print(sleep_time)