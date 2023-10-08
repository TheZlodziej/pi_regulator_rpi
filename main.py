import paho.mqtt.client as mqtt
from threading import Thread
from json import loads, dumps
from time import sleep
import RPi.GPIO as GPIO
from bmp280 import BMP280
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

def main():
    sim_config = {
        'tp': 1.0, # s
        'temp_set': 22.0, # deg
        'u_sat': 1,
        'kp': 0.6413,
        'ti': 35.3150
    }

    prev_sim_vals = {
        'e(n-1)': 0,
        'u(n-1)': 0
    }

    mqtt_config = {
        'hostname': 'localhost',
        'set_topic': 'uC/set',
        'get_topic': 'uC/get',
        'port': 1883,
        'keep_alive': 60
    }

    sens_values = {
        'temp': None
    }

    # hardware
    bus = SMBus(1)
    bmp280 = BMP280(i2c_dev=bus)
    print("BMP280 ready")

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    pwm_pin = 12
    GPIO.setup(pwm_pin, GPIO.OUT)
    pwm = GPIO.PWM(pwm_pin, 1000)
    pwm.start(0)
    print("PWM ready")
    #

    def on_message(client, userdata, msg):
        # parse message format:
        #
        # {
        #   "uset": <float>
        # }
        #  
        # update values
        parsed_msg = loads(msg.payload)
        print(parsed_msg)
        if parsed_msg['temp_set'] is not None:
            sim_config['temp_set'] = parsed_msg['temp_set']
        

    def pub_thread_fn():
        print("Publishing thread ready")
        while True:
            # publish current sensor values in format:
            #
            # {
            #   "temp_set": <float>,
            #   "temp": <float>,
            # }
            #
            client.publish("uC/get", dumps({
                'temp_set': sim_config['temp_set'],
                'temp': sens_values['temp']
            }))
            print("publishing...")
            sleep(sim_config['tp'])

    def update_sensor_data():
        # read sensor data and save to sens_values
        sens_values['temp'] = bmp280.get_temperature()

    def reg_thread_fn():
        print("Regulator thread ready")
        while True:
            # update sensor data
            update_sensor_data()

            # get saved values
            Et = sim_config['temp_set'] - sens_values['temp']
            Kp = sim_config['kp']
            Tp = sim_config['tp']
            Ti = sim_config['ti']
            Ut_prev = prev_sim_vals['u(n-1)']
            Et_prev = prev_sim_vals['e(n-1)']

            # calculate new U
            Ut = Ut_prev + Kp * (1 + Tp/Ti) * Et - Kp * Et_prev
            # saturation
            Ut = max(min(Ut, sim_config['u_sat']), 0)
            # set PWM duty
            pwm.ChangeDutyCycle(Ut*100)

            # set prev
            prev_sim_vals['e(n-1)'] = Et
            prev_sim_vals['u(n-1)'] = Ut

            # sleep for dt - time taken
            # TODO: ...
            sleep(sim_config['tp'])

    client = mqtt.Client()
    client.on_message = on_message
    client.connect(mqtt_config['hostname'], mqtt_config['port'], mqtt_config['keep_alive'])
    client.subscribe(mqtt_config['set_topic'])
    print("MQTT client ready")

    # update sensor data before reg start
    update_sensor_data()

    thread_pool = [Thread(target=pub_thread_fn), Thread(target=reg_thread_fn)]
    for th in thread_pool:
        th.start()

    client.loop_forever()

if __name__ == '__main__':
    main()

