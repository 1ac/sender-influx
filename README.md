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

