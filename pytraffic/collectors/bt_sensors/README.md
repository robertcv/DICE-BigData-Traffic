### Bluetooth sensors

On some traffic lights in Ljubljana there are bluetooth sensors. They 
collect ids of bluetooth devices that drive near them. If the same 
device is detected on a different locations the average speed can be 
calculated based on the distance and travel time. The data is generously
provided by the [Timon project](https://gitlab-timon.xlab.si/).

**Data source:**
https://datacloud-timon.xlab.si/data_access/

**JSON data:**
```json
{
  "id": "58b7eca0c0a6834de255eb5c",
  "fromBtId": "BTR0201",
  "fromBtLng": 14.50808,
  "fromBtLat": 46.06354,
  "toBtId": "BTR0202",
  "toBtLng": 14.50978,
  "toBtLat": 46.06826,
  "distance": 500,
  "allCount": 31,
  "avgSpeed": 46.015692307692305,
  "avgTravelTime": 0.015192307692307698,
  "count": 26,
  "timestampFrom": "2017-03-02T10:35:00+01:00",
  "timestampTo": "2017-03-02T10:50:00+01:00"
}
```

**Image of sensors location:**
![image](image/bt_lj.png)