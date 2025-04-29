class DisplayManager:
    @staticmethod
    def display_fail(senseHat): # Red dots in bottom corners
        senseHat.set_pixel(7, 7, 254, 0, 0)
        senseHat.set_pixel(0, 7, 254, 0, 0)

    @staticmethod
    def display_success(senseHat): # Green dots in bottom corners
        senseHat.set_pixel(7, 7, 0, 254, 0)
        senseHat.set_pixel(0, 7, 0, 254, 0)