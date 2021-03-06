# coding=utf-8
import logging
import os
from .base_sensor import AbstractSensor

logger = logging.getLogger("mycodo.sensors.raspi_freespace")


class RaspberryPiFreeSpace(AbstractSensor):
    """ A sensor support class that monitors the free space of a path """

    def __init__(self, path):
        super(RaspberryPiFreeSpace, self).__init__()
        self.path = path
        self._disk_space = 0.0

    def __repr__(self):
        """  Representation of object """
        return "<{cls}(disk_space={disk_space})>".format(
            cls=type(self).__name__,
            disk_space="{0:.2f}".format(self._disk_space))

    def __str__(self):
        """ Return CPU load information """
        return "Free space: {disk_space}".format(
            disk_space="{:.2f}".format(self._disk_space))

    def __iter__(self):  # must return an iterator
        """ RaspberryPiFreeSpace iterates through free space readings """
        return self

    def next(self):
        """ Get next free space reading """
        if self.read():  # raised an error
            raise StopIteration  # required
        return dict(disk_space=float('{0:.2f}'.format(self._disk_space)))

    def info(self):
        conditions_measured = [
            ("Free Space", "disk_space", "float", "0.00",
             self._disk_space, self.disk_space)
        ]
        return conditions_measured

    @property
    def disk_space(self):
        """ Free space of self.path """
        if not self._disk_space:  # update if needed
            self.read()
        return self._disk_space

    def get_measurement(self):
        """ Gets the free space """
        f = os.statvfs(self.path)
        return (f.f_bsize * f.f_bavail) / 1000000.0

    def read(self):
        """
        Takes a reading and updates the self._disk_space value

        :returns: None on success or 1 on error
        """
        try:
            self._disk_space = self.get_measurement()
            return  # success - no errors
        except Exception as e:
            logger.error("{cls} raised an exception when taking a reading: "
                         "{err}".format(cls=type(self).__name__, err=e))
        return 1
