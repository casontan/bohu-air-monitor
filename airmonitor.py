import socket
import threading
from urllib import parse
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    
    pm1 = PM1Senser()
    pm25 = PM25Senser()
    pm10 = PM10Senser()
    hoco = HOCOSenser()
    co2 = CO2Sensor()
    add_devices([AirMonitorSenser(pm1,pm25,pm10,hoco,co2),pm1,pm25,pm10,hoco,co2])


class BaseSenser(Entity):
    """BaseSensor."""
    
    def __init__(self):
        """Initialize the sensor."""
        self._state = 0
        self._valuess = 0

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Temperature'

    @property
    def valuess(self):
        """Return the value of the sensor."""
        return self._valuess

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        
        self._state = self._valuess


# Socket and default senser
class AirMonitorSenser(BaseSenser):
    """Representation of a Sensor."""
    
    def __init__(self,pm1,pm25,pm10,hoco,co2):
        """Initialize the sensor."""
        self._state = 0
        self._valuess = 0
        self._pm1 = pm1;
        self._pm25 = pm25;
        self._pm10 = pm10;
        self._hoco = hoco;
        self._co2 = co2;
        t = threading.Thread(target = self.server_start,args=())
        t.start()

    def server_start(self):
        """Fetch new state data for the sensor.
        """
        s = socket.socket()
        host = '192.168.31.111'
        port = 9960
        s.bind((host, port))
        s.listen(5)
        while True:
            c, addr = s.accept()
            data = c.recv(1024)
            url_str = str(data, encoding = "utf-8")  
            parseResult = parse.urlparse(url_str)
            param_dict = parse.parse_qs(parseResult.query)

            if param_dict['idx'][0] == '1': 
                self._pm1._valuess = int(param_dict['svalue'][0].split(' ')[0])
                self._pm1.update()
            elif param_dict['idx'][0] == '2': 
                self._pm25._valuess = int(param_dict['svalue'][0].split(' ')[0])
                self._pm25.update()
            elif param_dict['idx'][0] == '3': 
                self._pm10._valuess = int(param_dict['svalue'][0].split(' ')[0])
                self._pm10.update()
            elif param_dict['idx'][0] == '4': 
                self._hoco._valuess = int(param_dict['svalue'][0].split(' ')[0]) * 10
                self._hoco.update()
            elif param_dict['idx'][0] == '5': 
                 # 搞特殊，无语
                self._co2._valuess = int(param_dict['nvalue'][0].split(' ')[0])
                self._co2.update()
            elif param_dict['idx'][0] == '6': 
                self._valuess = int(param_dict['svalue'][0])
                self.update()

            # c.send("")
            c.close()

# idx 1
class PM1Senser(BaseSenser):
    '''
    PM1Senser
    '''
    @property
    def name(self):
        """Return the name of the sensor."""
        return 'PM1'
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'ug/m3'

# idx 2   
class PM25Senser(BaseSenser):
    '''
    PM25Senser
    '''
    @property
    def name(self):
        """Return the name of the sensor."""
        return 'PM2.5'
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'ug/m3'

#idx 3
class PM10Senser(BaseSenser):
    '''
    PM25Senser
    '''
    @property
    def name(self):
        """Return the name of the sensor."""
        return 'PM10'

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'ug/m3'       

#idx 4
class HOCOSenser(BaseSenser):
    '''
    HOCOSenser
    '''
    @property
    def name(self):
        """Return the name of the sensor."""
        return 'HOCO'

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'ug/m3' 

# idx 5
class CO2Sensor(BaseSenser):
    """Representation of a Sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'CO2'

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'ppm'



