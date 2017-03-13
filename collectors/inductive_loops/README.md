### Inductive loops

The data is similar to traffic counters except for the location which is
mostly inside Ljubljana highway ring. The data is generously provided by
the [Timon project](https://gitlab-timon.xlab.si/).

**Data source:** 
http://10.30.1.132:9200/_plugin/hq/

**WARNING:** 
Source is located on Arcture Openstack. You need to connect with OpenVPN. 
More information on [wiki](https://wiki.xlab.si/robert_plestenjak/openstack-arctur).

**JSON data:**
```json
{
  "id": "0018-11",
  "title": "-, Celovška cesta : Tivolska cesta - Ruska ul. (r)",
  "region": "Ljubljana",
  "location": 18,
  "locationDescription": "Celovška cesta",
  "deviceX": 46.057694,
  "deviceY": 14.500324,
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
  "updated": "2017-03-02T10:00:00Z"
}
``` 

**Image of inductive loops location:**
![test](image/inductive.png)