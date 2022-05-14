from kivy.app import App
from kivy.utils import platform
from kivy_garden.mapview import MapView
from tennismarker import TennisMarker
from tennismapview import TennisMapView
from kivymd.uix.dialog import MDDialog


class GpsHelper():
    has_centered_map = False
    def run(self):
        tmv = TennisMapView()
        #Reference GpsBlinker
        gps_blinker = App.get_running_app().root.ids.mapview.ids.blinker
        gps_blinker.blink()

        # Request permission on Android
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            def callback(permission, results):
                if all([res for res in results]):
                    print("All permissions recieved")
                else:
                    print("Did not recieve permissions")

            request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION], callback)

        #Configure GPS
        if platform == 'android' or platform == "ios":
            from plyer import gps
            for tc in TennisMapView.get_tcs_in_fov(self).tcs:
                tennisc = tc
            gps.configure(on_location=self.update_blinker_position(),
                          on_status=self.on_auth_status,
                          change_occupation_status=self.change_occupation_status(tennisc))
            gps.start(minTime=1000, minDistance=0)


    def update_blinker_position(self, *args, **kwargs):
        my_lat = kwargs['lat']
        my_lon = kwargs['lon']

        print("GPS POSITION", my_lat, my_lon)
        #Update GpsBlinker position
        gps_blinker = App.get_running_app().root.ids.mapview.ids.blinker
        gps_blinker.lat = my_lat
        gps_blinker.lon = my_lon

        #Center map on gps
        if not self.has_centered_app:
            map = App.get_running_app().root.ids.mapview
            map.center_on(my_lat, my_lon)
            self.has_centered_map = True


    def change_occupation_status(self, tc, **kwargs):
        my_lat = kwargs['lat']
        my_lon = kwargs['lon']

        lat, lon = tc[1], tc[2]
        occupation = tc[3]
        marker = TennisMarker(lat=lat, lon=lon, occupation=occupation)
        marker.tc_data = tc
        if ((my_lat <= (lat + 0.000164)) or (my_lat >= (lat - 0.000164))) and (
                (my_lon <= (lon + 0.000108)) or (my_lon >= (lon - 0.000108))):
            occupation = "yes"
            TennisMarker.source = 'ClosedMarker.png'

    def on_auth_status(self, general_status, status_message):
        if general_status == 'provider-enabled':
            pass
        else:
            self.open_gps_access_popup()

    def open_gps_access_popup(self):
        dialog = MDDialog(title="No GPS Access", text="In order for this app to function, your location services and GPS access is needed")
        dialog.size_hint = [.8, .8]
        dialog.pos_hint = {'center_x': .5, 'center_y': .5}
        dialog.open()
