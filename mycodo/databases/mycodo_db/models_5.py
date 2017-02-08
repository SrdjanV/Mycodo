# -*- coding: utf-8 -*-
import bcrypt
import datetime
from flask_sqlalchemy import SQLAlchemy
from RPi import GPIO

db = SQLAlchemy()

# TODO Build a BaseConditional that all the conditionals inherit from


class AlembicVersion(db.Model):
    __tablename__ = "alembic_version"
    version_num = db.Column(db.String(32),
                            primary_key=True, nullable=False,
                            default='6a5508a5f078')


#
# User Table
#

class Users(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.VARCHAR(64), unique=True, index=True)
    user_password_hash = db.Column(db.VARCHAR(255))
    user_email = db.Column(db.VARCHAR(64), unique=True, index=True)
    user_restriction = db.Column(db.VARCHAR(64))
    user_theme = db.Column(db.VARCHAR(64))

    def __repr__(self):
        output = "<User: <name='{name}', email='{email}' is_admin='{isadmin}'>"
        return output.format(name=self.user_name,
                             email=self.user_email,
                             isadmin=bool(self.user_restriction == 'admin'))

    def set_password(self, new_password):
        self.user_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def check_password(password, hashed_password):
        hashes_match = bcrypt.hashpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        return hashes_match


#
# Mycodo settings tables
#

class CameraStill(db.Model):
    __tablename__ = "camerastill"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    relay_id = db.Column(db.Integer, db.ForeignKey('relay.id'), default=None)  # Relay to turn on while capturing
    hflip = db.Column(db.Boolean, default=False)  # Horizontal flip image
    vflip = db.Column(db.Boolean, default=False)  # Vertical flip image
    rotation = db.Column(db.Integer, default=0)  # Rotation degree (0-360)
    cmd_pre_camera = db.Column(db.Text, default='')  # Command to execute before capture
    cmd_post_camera = db.Column(db.Text, default='')  # Command to execute after capture


class CameraStream(db.Model):
    __tablename__ = "camerastream"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    relay_id = db.Column(db.Integer, db.ForeignKey('relay.id'), default=None)  # Relay to turn on while capturing
    hflip = db.Column(db.Boolean, default=False)  # Horizontal flip image
    vflip = db.Column(db.Boolean, default=False)  # Vertical flip image
    rotation = db.Column(db.Integer, default=0)  # Rotation degree (0-360)
    cmd_pre_camera = db.Column(db.Text, default='')  # Command to execute before capture
    cmd_post_camera = db.Column(db.Text, default='')  # Command to execute after capture


class CameraTimelapse(db.Model):
    __tablename__ = "cameratimelapse"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    relay_id = db.Column(db.Integer, db.ForeignKey('relay.id'), default=None)  # Relay to turn on while capturing
    hflip = db.Column(db.Boolean, default=False)  # Horizontal flip image
    vflip = db.Column(db.Boolean, default=False)  # Vertical flip image
    rotation = db.Column(db.Integer, default=0)  # Rotation degree (0-360)
    cmd_pre_camera = db.Column(db.Text, default='')  # Command to execute before capture
    cmd_post_camera = db.Column(db.Text, default='')  # Command to execute after capture


class DisplayOrder(db.Model):
    __tablename__ = "displayorder"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    graph = db.Column(db.Text, default='')
    lcd = db.Column(db.Text, default='')
    pid = db.Column(db.Text, default='')
    relay = db.Column(db.Text, default='')
    remote_host = db.Column(db.Text, default='')
    sensor = db.Column(db.Text, default='')
    timer = db.Column(db.Text, default='')


class Graph(db.Model):
    __tablename__ = "graph"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.Text, default='')
    pid_ids_measurements = db.Column(db.Text, default='')  # store IDs and measurements to display
    relay_ids_measurements = db.Column(db.Text, default='')  # store IDs and measurements to display
    sensor_ids_measurements = db.Column(db.Text, default='')  # store IDs and measurements to display
    width = db.Column(db.Integer, default=100)  # Width of page (in percent)
    height = db.Column(db.Integer, default=400)  # Height (in pixels)
    x_axis_duration = db.Column(db.Integer, default=1440)  # X-axis duration (in minutes)
    refresh_duration = db.Column(db.Integer, default=120)  # How often to add new data and redraw graph
    enable_navbar = db.Column(db.Boolean, default=False)  # Show navigation bar
    enable_rangeselect = db.Column(db.Boolean, default=False)  # Show range selection buttons
    enable_export = db.Column(db.Boolean, default=False)  # Show export menu
    use_colors_custom = db.Column(db.Boolean, default=False)  # Enable custom colors of graph series
    custom_colors = db.Column(db.Text, default='')  # Custom hex color values (csv)


class LCD(db.Model):
    __tablename__ = "lcd"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.Text, default='')
    is_activated = db.Column(db.Boolean, default=False)
    period = db.Column(db.Integer, default=30)
    location = db.Column(db.Text, default='')
    multiplexer_address = db.Column(db.Text, default='')
    multiplexer_channel = db.Column(db.Integer, default=0)
    x_characters = db.Column(db.Integer, default=16)
    y_lines = db.Column(db.Integer, default=2)
    line_1_sensor_id = db.Column(db.Text, default='')
    line_1_measurement = db.Column(db.Text, default='')
    line_2_sensor_id = db.Column(db.Text, default='')
    line_2_measurement = db.Column(db.Text, default='')
    line_3_sensor_id = db.Column(db.Text, default='')
    line_3_measurement = db.Column(db.Text, default='')
    line_4_sensor_id = db.Column(db.Text, default='')
    line_4_measurement = db.Column(db.Text, default='')


class Method(db.Model):
    __tablename__ = "method"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.Text, default='')
    method_type = db.Column(db.Text, default='')
    method_order = db.Column(db.Text, default='')


class MethodData(db.Model):
    __tablename__ = "method_data"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    method_id = db.Column(db.Integer, db.ForeignKey('method.id'), default=None)
    time_start = db.Column(db.Text, default=None)
    time_end = db.Column(db.Text, default=None)
    duration_sec = db.Column(db.Integer, default=None)
    relay_id = db.Column(db.Integer, db.ForeignKey('relay.id'), default=None)
    relay_state = db.Column(db.Text, default=None)
    relay_duration = db.Column(db.Float, default=None)
    setpoint_start = db.Column(db.Float, default=None)
    setpoint_end = db.Column(db.Float, default=None)
    amplitude = db.Column(db.Float, default=None)
    frequency = db.Column(db.Float, default=None)
    shift_angle = db.Column(db.Float, default=None)
    shift_y = db.Column(db.Float, default=None)
    x0 = db.Column(db.Float, default=None)
    y0 = db.Column(db.Float, default=None)
    x1 = db.Column(db.Float, default=None)
    y1 = db.Column(db.Float, default=None)
    x2 = db.Column(db.Float, default=None)
    y2 = db.Column(db.Float, default=None)
    x3 = db.Column(db.Float, default=None)
    y3 = db.Column(db.Float, default=None)


class Misc(db.Model):
    __tablename__ = "misc"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    dismiss_notification = db.Column(db.Boolean, default=False)  # Dismiss login page license notice
    force_https = db.Column(db.Boolean, default=True)  # Force web interface to use SSL/HTTPS
    hide_alert_info = db.Column(db.Boolean, default=False)
    hide_alert_success = db.Column(db.Boolean, default=False)
    hide_alert_warning = db.Column(db.Boolean, default=False)
    language = db.Column(db.Text, default=None)  # Force the web interface to use a specific language
    login_message = db.Column(db.Text, default='')  # Put a message on the login screen
    relay_stats_cost = db.Column(db.Float, default=0.05)  # Energy cost per kWh
    relay_stats_currency = db.Column(db.Text, default='$')  # Energy cost currency
    relay_stats_dayofmonth = db.Column(db.Integer, default=15)  # Electricity billing day of month
    relay_stats_volts = db.Column(db.Integer, default=120)  # Voltage the alternating current operates
    stats_opt_out = db.Column(db.Boolean, default=False)  # Opt not to send anonymous usage statistics


class PID(db.Model):
    __tablename__ = "pid"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.Text)
    is_activated = db.Column(db.Boolean, default=False)
    is_preset = db.Column(db.Boolean, default=False)  # Is config saved as a preset?
    preset_name = db.Column(db.Text, default='')  # Name for preset
    period = db.Column(db.Integer, default=30)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), default=None)
    measurement = db.Column(db.Text, default='')  # What condition is the controller regulating?
    direction = db.Column(db.Text, default='Raise')  # Direction of regulation (raise, lower, both)
    setpoint = db.Column(db.Float, default=30.0)  # PID setpoint
    method_id = db.Column(db.Integer, db.ForeignKey('method.id'), default=None)
    p = db.Column(db.Float, default=1.0)  # Kp gain
    i = db.Column(db.Float, default=0.0)  # Ki gain
    d = db.Column(db.Float, default=0.0)  # Kd gain
    integrator_min = db.Column(db.Float, default=-100.0)
    integrator_max = db.Column(db.Float, default=100.0)
    raise_relay_id = db.Column(db.Integer, db.ForeignKey('relay.id'), default=None)  # Relay to raise the condition
    raise_min_duration = db.Column(db.Integer, default=0)
    raise_max_duration = db.Column(db.Integer, default=0)
    lower_relay_id = db.Column(db.Integer, db.ForeignKey('relay.id'), default=None)  # Relay to lower the condition
    lower_min_duration = db.Column(db.Integer, default=0)
    lower_max_duration = db.Column(db.Integer, default=0)


class Relay(db.Model):
    __tablename__ = "relay"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.Text, default='')
    pin = db.Column(db.Integer, default=0)
    amps = db.Column(db.Float, default=0.0)  # The current drawn by the device connected to the relay
    trigger = db.Column(db.Boolean, default=True)  # GPIO output to turn relay on (True=HIGH, False=LOW)
    on_at_start = db.Column(db.Boolean, default=False)  # Turn relay on when daemon starts?
    on_until = db.Column(db.DateTime, default=None)  # Stores time to turn off relay (if on for a duration)
    last_duration = db.Column(db.Float, default=None)  # Stores the last on duration (seconds)
    on_duration = db.Column(db.Boolean, default=None)  # Stores if the relay is currently on for a duration

    @staticmethod
    def _is_setup():
        """
        This function checks to see if the GPIO pin is setup and ready to use.  This is for safety
        and to make sure we don't blow anything.

        # TODO Make it do that.

        :return: Is it safe to manipulate this relay?
        :rtype: bool
        """
        return True

    def setup_pin(self):
        """
        Setup pin for this relay

        :rtype: None
        """
        # TODO add some extra checks here.  Maybe verify BCM?
        GPIO.setup(self.pin, GPIO.OUT)

    def turn_off(self):
        """
        Turn this relay off

        :rtype: None
        """
        if self._is_setup():
            self.on_duration = False
            self.on_until = datetime.datetime.now()
            GPIO.output(self.pin, not self.trigger)

    def turn_on(self):
        """
        Turn this relay on

        :rtype: None
        """
        if self._is_setup():
            GPIO.output(self.pin, self.trigger)

    def is_on(self):
        """
        :return: Whether the relay is currently "ON"
        :rtype: bool
        """
        return self.trigger == GPIO.input(self.pin)


class RelayConditional(db.Model):
    __tablename__ = "relayconditional"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.Text, default='')
    is_activated = db.Column(db.Boolean, default=False)
    if_relay_id = db.Column(db.Integer, db.ForeignKey('relay.id'), default=None)  # Watch this relay for action
    if_action = db.Column(db.Text, default='')  # What action to watch relay for
    if_duration = db.Column(db.Float, default=0.0)
    do_relay_id = db.Column(db.Integer, db.ForeignKey('relay.id'), default=None)  # Actuate relay if conditional triggered
    do_action = db.Column(db.Text, default='')  # what action, such as email, execute command, flash LCD
    do_action_data = db.Column(db.Text, default='')  # string, such as email address, command, or duration


class Remote(db.Model):
    __tablename__ = "remote"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    is_activated = db.Column(db.Boolean, default=False)
    host = db.Column(db.Text, default='')
    username = db.Column(db.Text, default='')
    password_hash = db.Column(db.Text, default='')


class Sensor(db.Model):
    __tablename__ = "sensor"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.Text, default='')
    is_activated = db.Column(db.Boolean, default=False)
    is_preset = db.Column(db.Boolean, default=False)  # Is config saved as a preset?
    preset_name = db.Column(db.Text, default=None)  # Name for preset
    device = db.Column(db.Text, default='')  # Device name, such as DHT11, DHT22, DS18B20
    period = db.Column(db.Float, default=15.0)  # Duration between readings
    i2c_bus = db.Column(db.Integer, default='')  # I2C bus the sensor is connected to
    location = db.Column(db.Text, default='')  # GPIO pin or i2c address to communicate with sensor
    power_pin = db.Column(db.Integer, default=0)  # GPIO pin to turn HIGH/LOW to power sensor
    power_state = db.Column(db.Boolean, default=True)  # State that powers sensor (True=HIGH, False=LOW)
    measurements = db.Column(db.Text, default='')  # Measurements separated by commas
    multiplexer_address = db.Column(db.Text, default=None)
    multiplexer_bus = db.Column(db.Integer, default=1)
    multiplexer_channel = db.Column(db.Integer, default=0)
    switch_edge = db.Column(db.Text, default='rising')
    switch_bouncetime = db.Column(db.Integer, default=50)
    switch_reset_period = db.Column(db.Integer, default=10)
    pre_relay_id = db.Column(db.Integer, db.ForeignKey('relay.id'), default=False)  # Relay to turn on before sensor read
    pre_relay_duration = db.Column(db.Float, default=0.0)  # Duration to turn relay on before sensor read
    sht_clock_pin = db.Column(db.Integer, default=None)
    sht_voltage = db.Column(db.Text, default='3.5')

    # Analog to digital converter options
    adc_channel = db.Column(db.Integer, default=0)
    adc_gain = db.Column(db.Integer, default=1)
    adc_resolution = db.Column(db.Integer, default=18)
    adc_measure = db.Column(db.Text, default='Condition')
    adc_measure_units = db.Column(db.Text, default='unit')
    adc_volts_min = db.Column(db.Float, default=None)
    adc_volts_max = db.Column(db.Float, default=None)
    adc_units_min = db.Column(db.Float, default=0)
    adc_units_max = db.Column(db.Float, default=10)

    def is_active(self):
        """
        :return: Whether the sensor is currently activated
        :rtype: bool
        """
        return self.is_activated


class SensorConditional(db.Model):
    __tablename__ = "sensorconditional"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.Text, default='')
    is_activated = db.Column(db.Integer, default=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), default=None)
    period = db.Column(db.Integer, default=30)
    measurement = db.Column(db.Text, default='')  # which measurement to monitor
    edge_select = db.Column(db.Text, default='')  # monitor Rising, Falling, or Both switch edges
    gpio_state = db.Column(db.Boolean, default=False)
    edge_detected = db.Column(db.Text, default='')
    direction = db.Column(db.Text, default='')  # 'above' or 'below' setpoint
    setpoint = db.Column(db.Float, default=30)
    relay_id = db.Column(db.Integer, db.ForeignKey('relay.id'), default=None)
    relay_state = db.Column(db.Text, default='')  # 'on' or 'off'
    relay_on_duration = db.Column(db.Float, default=0.0)
    execute_command = db.Column(db.Text, default='')
    email_notify = db.Column(db.Text, default='')
    flash_lcd = db.Column(db.Text, default='')
    camera_record = db.Column(db.Text, default='')


class SMTP(db.Model):
    __tablename__ = "smtp"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    host = db.Column(db.Text, default='smtp.gmail.com')
    ssl = db.Column(db.Boolean, default=1)
    port = db.Column(db.Integer, default=465)
    user = db.Column(db.Text, default='email@gmail.com')
    passw = db.Column(db.Text, default='password')
    email_from = db.Column(db.Text, default='email@gmail.com')
    hourly_max = db.Column(db.Integer, default=2)


class Timer(db.Model):
    __tablename__ = "timer"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.Text, default='')
    is_activated = db.Column(db.Boolean, default=False)
    timer_type = db.Column(db.Text, default=None)
    relay_id = db.Column(db.Integer, db.ForeignKey('relay.id'), default=None)
    state = db.Column(db.Text, default=None)  # 'on' or 'off'
    time_start = db.Column(db.Text, default=None)
    time_end = db.Column(db.Text, default=None)
    duration_on = db.Column(db.Float, default=None)
    duration_off = db.Column(db.Float, default=None)