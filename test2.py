import json

data = json.loads('{"lat":444, "lon":555}')
print(data)
for key, value in data.items():
    print( value)