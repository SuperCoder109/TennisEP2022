from kivy_garden.mapview import MapMarkerPopup

class TennisMarker(MapMarkerPopup):
    source = 'OpenMarker.png'
    tc_data = []

    def on_release(self):
        pass