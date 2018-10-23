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
#Start timer with a random interval between 0.1 and 1 second
while 1:
    for x in range(120):
        thread1 = Thread(target = req_1)
        thread2 = Thread(target = req_2)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    time.sleep(random.randint(5, 30))
