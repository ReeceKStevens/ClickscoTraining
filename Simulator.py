import requests

#Boilerplate code for threaded timer which repeats function on it's own thread
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

#Function to execute on each timer tick
def on_tick():
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

    try:
        #Posts a request to secondAD endpoint
        requests.post('http://127.0.0.1:5000/secondAD', json = {'keywords' : 'Fruit Mango'})
        print('Second Ad Request Success!')
    except Exception as err:
        print('Failure, ' + str(err))
    finally:
        print('')
#Start timer with a random interval between 0.1 and 1 second
for x in range(120):
    on_tick()
