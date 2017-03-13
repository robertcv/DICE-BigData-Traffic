### LPP traffic

LPP company runs the city bus traffic in Ljubljana. They have stations 
all over the city. Their data is collected combined with station static 
arrival time. Those arrival times are predicted in advance by LPP if 
there is no traffic. But because this is not the case one can also get 
live prediction on arrival data. The data is generously provided by the 
Timon project.

**Data source:** 
http://jozefstefaninstitute.github.io/LPPServer/

#### LPP live arrival 

**JSON data:**
```json
{
  "station_int_id": 2097,
  "route_int_id": 1564,
  "arrival_time": "2017-03-02 11:15:33.000"
}
```


#### LPP static arrival

**JSON data:**
```json
{
  "station_int_id": 3261,
  "route_int_id": 911,
  "arrival_time": "2017-03-02T21:13:00.000Z"
}
```


#### LPP stations data 

**JSON data:**
```json
{
  "station_int_id": 4236,
  "station_name": "Na Žale",
  "station_direction": "",
  "station_ref_id": 203232,
  "station_lat": 46.0716188375998,
  "station_lng": 14.529913754516,
  "route_int_id": 1579,
  "route_num": 19,
  "route_num_sub": "B",
  "route_name": "TOMAČEVO",
  "scraped": "2017-03-10T00:00:00+00:00"
}
```
