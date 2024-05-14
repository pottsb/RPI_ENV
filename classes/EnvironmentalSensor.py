class EnvironmentalSensor:
    def __init__(self):
        self.temperatures_previous = {}
        self.humidity_previous = None
        self.pressure_previous = None

    def update_temperature(self, name, current_temperature):
        if name not in self.temperatures_previous:
            self.temperatures_previous[name] = current_temperature
            return self.check_temperature(current_temperature, current_temperature)
        else:
            previous_temperature = self.temperatures_previous[name]
            error = self.check_temperature(previous_temperature, current_temperature)
            self.temperatures_previous[name] = current_temperature
            return error

    def update_humidity(self, current_humidity):
        if self.humidity_previous is None:
            self.humidity_previous = current_humidity
            return self.check_humidity(current_humidity, current_humidity)
        else:
            error = self.check_humidity(self.humidity_previous, current_humidity)
            self.humidity_previous = current_humidity
            return error

    def update_pressure(self, current_pressure):
        if self.pressure_previous is None:
            self.pressure_previous = current_pressure
            return self.check_pressure(current_pressure, current_pressure)
        else:
            error = self.check_pressure(self.pressure_previous, current_pressure)
            self.pressure_previous = current_pressure
            return error

    def check_temperature(self, previous, current):
        if abs(current - previous) > 5:
            print("Temperature rapid change detected.")
            return False
        elif -10 <= current <= 55:
            print("Temperature is within the normal range.")
            return True
        else:
            print("Temperature out of expected range!")
            return False

    def check_humidity(self, previous, current):
        if abs(current - previous) > 5:
            print("Humidity rapid change detected.")
            return False
        elif 5 <= current <= 100:
            print("Humidity is within the normal range.")
            return True
        else:
            print("Humidity out of expected range!")
            return False

    def check_pressure(self, previous, current):
        if abs(current - previous) > 10:
            print("Pressure rapid change detected.")
            return False
        elif 900 <= current <= 1100:
            print("Pressure is within the normal range.")
            return True
        else:
            print("Pressure out of expected range!")
            return False

# Example usage:
#sensor = EnvironmentalSensor()
#print(sensor.update_temperature('sensor1', 20))
#print(sensor.update_temperature('sensor2', 22))
#print(sensor.update_humidity(50))
#print(sensor.update_pressure(1000))
