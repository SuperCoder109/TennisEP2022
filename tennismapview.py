from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivy.app import App
from tennismarker import TennisMarker

class TennisMapView(MapView):
    getting_tcs_timer = None
    tc_names = []
    tcs = []
    def start_getting_tcs_in_fov(self):
        #After One second get tennis courts in field of view
        try:
            self.getting_tcs_timer.cancel()
        except:
            pass

        self.getting_tcs_timer = Clock.schedule_once(self.get_tcs_in_fov, 1)

    def get_tcs_in_fov(self, *args):
        min_lat, min_lon, max_lat, max_lon = self.get_bbox()
        app = App.get_running_app()
        sql_statement = "SELECT * FROM first name WHERE latitude > %s AND latitude < %s AND longitude > %s AND longitude < %s "%(min_lat, max_lat, min_lon, max_lon)
        app.cursor.execute(sql_statement)
        tcs = app.cursor.fetchall()
        print(tcs)
        for tc in tcs:
            name = tc[0]
            if name in self.tc_names:
                continue
            else:
                self.add_tc(tc)
                tcs.append(tc)


    def add_tc(self, tc):
        # Create TennisMarker
        lat, lon = tc[1], tc[2]
        marker = TennisMarker(lat=lat, lon=lon)
        marker.tc_data = tc
        # Add the TennisMarker to map
        self.add_widget(marker)
        # Keep track of marker name
        name = tc[0]

