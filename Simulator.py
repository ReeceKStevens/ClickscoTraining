import requests, sched, time, random

scheduler = sched.scheduler(time.time, time.sleep)

def on_tick(timer):

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

    scheduler.enter(random.uniform(0.1, 1), 1, on_tick, (scheduler,))
    return

scheduler.enter(random.uniform(0.1, 1), 1, on_tick, (scheduler,))
scheduler.run()
