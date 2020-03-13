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

![Test Image 6](master/img/diffTime.png)