from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import threading, time
import random, requests
from socketserver import ThreadingMixIn


class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class ReadWriteLock(object):

    def __init__(self):
        self.__monitor = threading.Lock()
        self.__exclude = threading.Lock()
        self.readers = 0

    def acquire_read(self):
        with self.__monitor:
            self.readers += 1
            if self.readers == 1:
                self.__exclude.acquire()

    def release_read(self):
        with self.__monitor:
            self.readers -= 1
            if self.readers == 0:
                self.__exclude.release()

    def acquire_write(self):
        self.__exclude.acquire()

    def release_write(self):
        self.__exclude.release()

class Server:
    def __init__(self):
        self.requestQueue = []
        self.lock = ReadWriteLock()
        self.d = {}

    def sortbyTime(self):
        self.lock.acquire_write()
        temp = self.requestQueue.copy()
        self.requestQueue = []
        self.lock.release_write()
        print(temp)
        temp.sort(key=lambda x: x[2])
        print(temp)
        for i in temp:
            self.openfaasRequest(i)
        # if temp != []:
        #     print(temp[0], temp[-1])

    def openfaasRequest(self, req):
        self.d[req[3]]['lock'].acquire()
        self.d[req[3]]['value'] = requests.post(req[1], data=str(req[2])).text
        print(self.d)
        self.d[req[3]]['lock'].notify()
        self.d[req[3]]['lock'].release()

    def timer(self):
        while True:
            time.sleep(1)
            self.sortbyTime()

    def addRequest(self, item):
        unique = time.time()
        item.append(str(unique))
        print(item, unique)
        self.lock.acquire_read()
        self.requestQueue.append(item)
        tempLock = threading.Condition()
        tempLock.acquire()
        self.d[str(unique)] = {'value': None, 'lock': tempLock}
        self.lock.release_read()
        tempLock.wait()
        tempLock.release()
        temp = self.d[str(unique)]['value']
        self.d.pop(str(unique))
        print(temp)
        return temp


# def client(a):
#     for i in range(1000):
#         time.sleep(0.01)
#         s.addRequest([a, i, random.randint(0, 100)])
#         # s.addRequest(i)

if __name__ == '__main__':
    myServer = Server()
    t1 = threading.Thread(target=myServer.timer)
    # t2 = threading.Thread(target=client, args=['A'])
    # t3 = threading.Thread(target=client, args=['B'])
    t1.start()
    # t2.start()
    # t3.start()

    svr = SimpleThreadedXMLRPCServer(("", int(6666)), allow_none=True)
    # regisrer functions
    svr.register_function(myServer.addRequest)
    # run server
    svr.serve_forever()