import dbus
import gobject

class DeviceListener:
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.hal_manager_obj = self.bus.get_object(
            "org.freedesktop.Hal",
            "/org/freedesktop/Hal/Manager")
        self.hal_manager = dbus.Interface(
            self.hal_manager_obj,
            "org.freedesktop.Hal.Manager")

        self.hal_manager.connect_to_signal("DeviceAdded", self.filter_volumes(self.added))
        self.hal_manager.connect_to_signal("DeviceRemoved", self.filter_volumes(self.removed))

    def filter_volumes(self, callback):
        def _filter(udi):
            device_obj = self.bus.get_object ("org.freedesktop.Hal", udi)
            device = dbus.Interface(device_obj, "org.freedesktop.Hal.Device")

            if device.QueryCapability("volume"):
                return callback(device)
        return _filter
    
    def removed(self, volume):
        print "Storage device removed"

    def added(self, volume):
        device_file = volume.GetProperty("block.device")
        label = volume.GetProperty("volume.label")
        fstype = volume.GetProperty("volume.fstype")
        mounted = volume.GetProperty("volume.is_mounted")
        mount_point = volume.GetProperty("volume.mount_point")
        try:
            size = volume.GetProperty("volume.size")
        except:
            size = 0

        print "New storage device detected:"
        print "  device_file: %s" % device_file
        print "  label: %s" % label
        print "  fstype: %s" % fstype

        if mounted:
            print "  mount_point: %s" % mount_point
        else:
            print "  not mounted"
        print "  size: %s (%.2fGB)" % (size, float(size) / 1024**3)

if __name__ == '__main__':
    from dbus.mainloop.glib import DBusGMainLoop
    DBusGMainLoop(set_as_default=True)
    loop = gobject.MainLoop()
    DeviceListener()
    loop.run()
