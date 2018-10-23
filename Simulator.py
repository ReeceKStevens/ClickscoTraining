import requests, time, random
from threading import Thread

def req_1():
    #Each request is wrapped in a try block in case of connection failure
    try:
        #Try posting a keyword request for Ad 1
        requests.post('http://127.0.0.1:5000/', json = {'keyinput' : 'Fruit Mango'})
        print('First Ad Request Sucess!')
    #If connection fails then provide error message and continue
    except Exception as err:
        print('Failure, ' + str(err))
    #Line break for readability
    finally:
        print('')

def req_2():
    try:
        #Posts a request to secondAD endpoint
        requests.post('http://127.0.0.1:5000/secondAD', json = {'keywords' : 'Fruit Mango'})
        print('Second Ad Request Success!')
    except Exception as err:
        print('Failure, ' + str(err))
    finally:
        print('')

#Run Forever
while 1:
    #Repeat 120 times, just an arbitrary number
    for x in range(120):
        #Open up two new threads and place the requests using that thread1
        #This should allow us to throw out new requests before the previous
        #One is even handled, which could theoretically overload the server
        thread1 = Thread(target = req_1)
        thread2 = Thread(target = req_2)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    #Start a new batch of requests in 5-30 seconds
    time.sleep(random.randint(5, 30))
