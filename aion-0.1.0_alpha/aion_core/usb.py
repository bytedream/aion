#!/usr/bin/python3

import pyudev, psutil
from os import system


class USB:

    def __init__(self) -> None:
        """
        :return: None

        :since: 0.1.0
        """
        pass

    class _DeviceInfos:
        """
        base class for usb infos

        :since: 0.1.0
        """

        def __init__(self, action: str) -> None:
            """
            :param action: str
                name of the action
                syntax: <action name>
                example: "add"
            :return: None

            :since: 0.1.0
            """
            self.action = action
            self.add = False
            self.remove = False

            if self.action == "add":
                self.add = True
                self.remove = False
            elif action == "remove":
                self.remove = True
                self.add = False

        def __iter__(self):
            return self

    @staticmethod
    def mount() -> None:
        """
        mounts a usb device

        :return: None

        :since: 0.1.0
        """
        pass

    def listen(self) -> _DeviceInfos:
        """
        listen permanent to usb ports for actions etc.

        :return: None

        :since: 0.1.0
        """
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem="usb")

        removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if device.attributes.asstring('removable') == "1"]
        for device in removable:
            partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
            print("All removable partitions: {}".format(", ".join(partitions)))
            print("Mounted removable partitions:")
            for p in psutil.disk_partitions():
                if p.device in partitions:
                    print("  {}: {}".format(p.device, p.mountpoint))

        for device in iter(monitor.poll, None):
            if device.action == "add":
                yield self._DeviceInfos("add")
            elif device.action == "remove":
                yield self._DeviceInfos("remove")
            print([device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition')])

    @staticmethod
    def umount() -> None:
        """
        unmount usb device

        :return: None

        :since: 0.1.0
        """
        system("sudo umount /mnt/usbstick")


if __name__ == '__main__':
    print([device.device_node for device in pyudev.Context().list_devices(subsystem='block', DEVTYPE='partition')])
    for action in USB().listen():
        pass
