from xmlrpc.server import SimpleXMLRPCServer

class Forecast(object):
    description: str 
    wind_force: float 
    temperature: float

    def __init__(self, description: str, wind_force: float, temperature: float):
        self.description = description
        self.wind_force = wind_force
        self.temperature = temperature

    def get_list(self): 
        return [self.description, self.wind_force, self.temperature]

class ForecastCalendar(object):
    forecasts: dict[str, Forecast]
    password: str

    def __init__(self, initial_values: dict[str, Forecast], password: str):
        self.forecasts = initial_values
        self.password = password

    def get_forecast(self, date: str):
        if date in self.forecasts:
            return self.forecasts[date].get_list()
        return "No forecast"

    def update_forecast(self, password: str, date: str, description: str, wind_force: float, temperature: float):
        if (self.password != password):
            return "No update"
        self.forecasts[date] = Forecast(description, wind_force, temperature)
        return self.forecasts[date].get_list()
        
        
if __name__ == "__main__":
    initial_state: dict[str, Forecast] = {
        "2012-11-05": Forecast('desc1', 1.0, 10.0),
        "2012-11-06": Forecast('desc2', 2.0, 20.0),
        "2012-11-07": Forecast('desc3', 3.0, 30.0),
        "2012-11-08": Forecast('desc4', 4.0, 40.0),
    }

    fcalendar = ForecastCalendar(initial_state, password = "master-of-weather")

    server_address = ('localhost', 10001)
    server = SimpleXMLRPCServer(server_address)
    server.register_instance(fcalendar)
    server.register_introspection_functions()
    print("Starting Weather XML-RPC server, use <Ctrl-C> to stop")
    server.serve_forever()


