import requests

url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YzBhMWU1NzcxOTMxM2ZlYzgyYzA3NzI0M2Y4ZjMxYiIsIm5iZiI6MTc0MjE5ODgxOS44NjA5OTk4LCJzdWIiOiI2N2Q3ZDgyMzE5MTg2OGM1NGZmMWMwOWIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.d-IUNeHmoALNyUtgOoTs-AU2vW87guSX1eNzcLdyTUc"
}

response = requests.get(url, headers=headers)

print(response.text)