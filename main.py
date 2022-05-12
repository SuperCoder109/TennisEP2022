from kivymd.app import MDApp
from tennismapview import TennisMapView
import sqlite3
from gpshelper import GpsHelper

class MainApp(MDApp):
    connection = None
    cursor = None
    search_menu = None

    def on_start(self):
        self.connection = None
        self.cursor = None
        # Initialize GPS
        GpsHelper().run()
        # Connect to database
        self.connection = sqlite3.connect("TennisCourts.db")
        self.cursor = self.connection.cursor()

        print()

        # Instantiate SearchPopupMenu

MainApp().run()

