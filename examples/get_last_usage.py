from agso.client import AgsoClient

username = input("Enter your AGSO username: ")
password = input("Enter your AGSO password: ")

client = AgsoClient(username, password)
print(client.get_current_meter_reading())