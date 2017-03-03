# Kafka topics:

### bt_json

podatki bluetooth senzorejv na semaforjih

**Source:**  https://datacloud-timon.xlab.si/data_access/

```json
{
  "id": "58b7eca0c0a6834de255eb5c",
  "fromBtId": "BTR0201",
  "fromBtLoc": {
    "lng": 14.50808,
    "lat": 46.06354
  },
  "toBtId": "BTR0202",
  "toBtLoc": {
    "lng": 14.50978,
    "lat": 46.06826
  },
  "distance": 500,
  "allCount": 31,
  "avgSpeed": 46.015692307692305,
  "avgTravelTime": 0.015192307692307698,
  "count": 26,
  "timestampFrom": "2017-03-02T10:35:00+01:00",
  "timestampTo": "2017-03-02T10:50:00+01:00"
}
```

![test](bt/image/bt_lj.png)

### inductive_json

podatki iz indukcijskih zank (znotraj lj)

**Source:**  http://10.30.1.132:9200/_plugin/hq/
 
```json
{
  "id": "0018-11",
  "title": "-, Celovška cesta : Tivolska cesta - Ruska ul. (r)",
  "region": "Ljubljana",
  "location": 18,
  "locationDescription": "Celovška cesta",
  "deviceX": "46,057694",
  "deviceY": "14,500324",
  "point": "46,057694 14,500324",
  "direction": 11,
  "directionDescription": "Tivolska cesta - Ruska ul.",
  "laneDescription": "(r)",
  "roadSection": "-",
  "roadDescription": "-",
  "StatusDescription": "Normal traffic",
  "numberOfVehicles": 444,
  "gap": 7.3,
  "vmax": 50,
  "avgSpeed": 61,
  "occ": 56,
  "chainage": 0,
  "stat": 1,
  "time": "11:00:00",
  "date": "02/03/2017",
  "pkgdate": "2017-03-02T10:00:19Z",
  "updated": "2017-03-02T10:00:00Z",
  "summary": "-, Celovška cesta : Tivolska cesta - Ruska ul. (r) - Normal traffic (444 vehicles/h, avg. speed=61km/h, avg. gap=7.3s, occupancy=5.6%)",
}
``` 

![test](inductive/image/inductive.png)

### lpp_live_json 
trenutne napovedi prihodov lpp

**Source:**  http://jozefstefaninstitute.github.io/LPPServer/

```json
{
  "station_int_id": 2097,
  "route_int_id": 1564,
  "arrival_time": "2017-03-02 11:15:33.000"
}
```


### lpp_static_json 
vozni red lpp

**Source:**  http://jozefstefaninstitute.github.io/LPPServer/

```json
{
  "station_int_id": 3261,
  "route_int_id": 911,
  "arrival_time": "2017-03-02T21:13:00.000Z"
}
```


### lpp_station_json 
podatki o postajh in linijah

**Source:**  http://jozefstefaninstitute.github.io/LPPServer/

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
  "route_name": "TOMAČEVO"
}
```


### counter_json 
podatki iz števcev prometa (obvoznica in izven lj)

**Source:**  https://github.com/zejn/prometapi

```json
{
  "Id": "0178-21",
  "Title": "AC-A1, LJ (južna obvoznica)",
  "Description": "AC-A1, LJ (južna obvoznica)",
  "stevci_lokacijaOpis": "LJ (južna obvoznica)",
  "stevci_cestaOpis": "AC-A1",
  "stevci_smerOpis": "Barjanska - Peruzzijeva",
  "stevci_pasOpis": "(v)",
  "x_wgs": 14.51818035950113,
  "y_wgs": 46.01962915242322,
  "CrsId": "EPSG:2170",
  "Y": 97385.0,
  "X": 463074.0,
  "stevci_statOpis": "Zgoščen promet",
  "stevci_stev": "1056",
  "stevci_hit": "95",
  "stevci_gap": "3,0",
  "stevci_stat": "3",
  "ContentName": "stevci",
  "Icon": "res/icons/stevci/stevec_3.png",
  "ModifiedTime": "2017-03-03T10:19:14.2723429Z",
}
```

### pollution_json 
podtaki o koncentraciji snovi v zraku (bezigrad in vosnjakova-tivolska )

**Source:**  http://www.ljubljana.si/si/zivljenje-v-ljubljani/okolje-prostor-bivanje/stanje-okolja/zrak/

```json
{
  "location": "bezigrad",
  "co": "0.48",
  "no": "52.3",
  "no2": "44.5",
  "nox": "124.45",
  "pm": "44.33",
  "so2": "9.7",
  "solar_radiation": "172",
  "ozone": None,
  "temperature": "4.3",
  "pressure": "979.5",
  "humidity": "84",
  "windspeed": "1.1",
  "wind_direction": "SV",
  "hour": "10:00",
  "scraped": "2017-03-02"
}
```

```json
{
  "location": "vosnjakova-tivolska",
  "no": "179",
  "no2": "70",
  "pm": "50",
  "so2": "4",
  "tolulene": "7",
  "paraxylene": "5",
  "benzene": "3",
  "hour": "08:00",
  "scraped": "2017-03-02"
}
```
