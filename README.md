# influxdb:
- *db*: omni_results
- *user*: root
- *password*: root

# log:
- *file*: results_table.csv
- *header*:DateTime,Method,DiffTime,measurement,SimpleCount,ErrorCount
- *fieldcolumns*='DiffTime,SimpleCount,ErrorCount,ErrorCount',
- *tagcolumns*='Method',
- *timecolumn*='DateTime',
- *timeformat*='%Y-%m-%x %H:%M:%S.%f',

# grafana:
dush: grafana.json

![diffTime](https://github.com/1ac/sender-influx/blob/master/img/diffTime.png)
![rps_all](https://github.com/1ac/sender-influx/blob/master/img/rps_all.png)
![rps_method](https://github.com/1ac/sender-influx/blob/master/img/rps_method.png)

### example results analiz
```bash
---Таблица времени отклика:
label,max,pct99.9,pct99,pct98,pct90,pct75,pct50,pct25,min,std.dev
mobilebank/service/serverCapabilities,485,337,232,211,176,153,130,116,107,91
mobilebank/service/announcements,247,221,129,102,68,53,39,32,25,17
```