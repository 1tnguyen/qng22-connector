import requests

class DevSimulator (object):

    token = ""

    def __init__(self, token: str = ""):
        self.token = token
        self.URL = "https://qng22-sim.azurewebsites.net/dev/"

    def authentication(self, token: str):
        """Updates the access token used by the simulator connector"""
        self.token = token

    def simulate(self, pulse: list[int], measure: list, example: int) -> float:
        """
        Runs the provided configuration into the simulator and returns a normalised signal as a float
        
        Keyword arguments:
        pulse -- paired list with start and end of pulse in us (0-500,000)
        measure -- list with start and end of the measurement window in us (0-500 000) and phase in radians
        example -- id of example chosen for the simulation (0-999)
        """
        #creates JSON form data for HTTP request
        payload = {"pulsestart":pulse[0], "pulseend":pulse[1], "measurestart":measure[0], "measureend":measure[1], "phase":measure[2]}
        
        #sends data to site, stores in variable r
        r = self.post(payload, str(example))

        #return to user the actual value of the request, removing header and online data that is unneeded
        return r.json()['signal']

    #Directly calls dev_data() in qe_radar
    def dataset(self, example) -> list:
        """Requests the Rabi, Detuning, and Time of Flight for the chosen example target."""
        #sends data to site, stores in variable r
        r = self.get(str(example))

        data = r.json()
    
        #return to user the actual value of the request, removing header and online data that is unneeded
        return [data['Rabi'], data['Detuning'], data['T_Flight']]

    def validate_config(self, configs: list) -> str:
        
        payload = {"configuration":configs}

        r = self.post(payload, "config")
        return r.text

    def validate_estimate(self, estimates: list) -> str:
        
        payload = {"estimates":estimates}

        r = self.post(payload, "estimate")
        return r.text

    def post(self, payload, ref=""):
        return requests.post(self.URL+ref, data=payload, headers={'Authentication': self.token})

    def get(self, ref=""):
        return requests.get(self.URL+ref, headers={'Authentication': self.token})

class TestSimulator(object):
    def __init__(self, token: str = "") -> None:
        self.token = token
        self.URL = "https://qng22-sim.azurewebsites.net/test/"

    def authentication(self, token: str):
        self.token = token

    def simulate(self, pulse: list[int], measure:list, example:int):
        #creates JSON form data for HTTP request
        payload = {"pulsestart":pulse[0], "pulseend":pulse[1], "measurestart":measure[0], "measureend":measure[1], "phase":measure[2]}
        
        #sends data to site, stores in variable r
        r = self.post(payload)

        #return to user the actual value of the request, removing header and online data that is unneeded
        return r.json()['signal']

    def score(self, configs:list, estimates:int):
        payload = {"configuration":configs, "estimates":estimates}
        r = self.post(payload, "score")

    def post(self, payload, ref=""):
        return requests.post(self.URL+ref, data=payload, headers={'Authentication': self.token})

    def get(self, ref=""):
        return requests.get(self.URL+ref, headers={'Authentication': self.token})