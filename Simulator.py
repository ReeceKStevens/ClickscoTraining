import requests, threading, random

def on_tick():
    try:
        requests.post('http://127.0.0.1:5000/', json = {'keyinput' : 'Fruit Mango'})
        print('First Ad Request Sucess!')
    except Exception as err:
        print('Failure, ' + str(err))
    finally:
        print('')

    try:
        requests.post('http://127.0.0.1:5000/secondAD', json = {'keywords' : 'Fruit Mango'})
        print('Second Ad Request Success!')
    except Exception as err:
        print('Failure, ' + str(err))
    finally:
        print('')

    threading.Timer (random.uniform(0.1, 1), on_tick, args = ()).start()

threading.Timer (random.uniform(0.1, 1), on_tick, args = ()).start()
