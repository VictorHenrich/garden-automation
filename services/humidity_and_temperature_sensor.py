from machine import Pin
from dht import DHT11
from utils.patterns import BaseService, ServiceResponse
from utils.exceptions import ServiceError
from utils import config


class HumidityAndTemperatureSensorService(BaseService):
    def __init__(self, analog_port=config.HUM_AND_TEMP_SENSOR_PORT, sensor_class=DHT11):
        pin = Pin(analog_port, Pin.IN)

        self.__sensor = sensor_class(pin)

    def __get_humidity_and_temperature(self):
        try:
            self.__sensor.measure()

            temperature = self.__sensor.temperature()

            humidity = self.__sensor.humidity()

            return humidity, temperature

        except Exception as error:
            raise ServiceError(
                self, "Falha ao realizar captura de umidade e temperatura!", error
            )

    def execute(self):
        humidity, temperature = self.__get_humidity_and_temperature()

        return ServiceResponse(
            mqtt_topic=config.TOPIC_SENDING_HUM_AND_TEMP_SENSOR_DATA,
            mqtt_data={"humidity": humidity, "temperature": temperature},
            display_message=f"Humidade: {humidity}%\nTemperatura: {temperature}C°",
        )
