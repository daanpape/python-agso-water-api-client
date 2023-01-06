import AgsoClient

api = AgsoClient("username", "password")
print(api.get_current_meter_reading())