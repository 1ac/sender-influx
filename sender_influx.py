import os

import pandas as pd

# import requests
# import gzip
# import argparse
import csv
import datetime
from pytz import timezone

from influxdb import InfluxDBClient

epoch_naive = datetime.datetime.utcfromtimestamp(0)
epoch = timezone('UTC').localize(epoch_naive)


def unix_time_millis(dt):
    return int((dt - epoch).total_seconds() * 1000)


def isfloat(value):
    """
    Check if data type of field is float
    :param value:
    :return:
    """
    try:
        float(value)
        return True
    except:
        return False


def isbool(value):
    """
    Check if data type of field is bool
    :param value:
    :return:
    """
    try:
        return value.lower() in ('true', 'false')
    except:
        return False


def str2bool(value):
    '''String to lower true'''
    return value.lower() == 'true'


def isinteger(value):
    """
    Check if data type of field is int
    :param value:
    :return:
    """
    try:
        if (float(value).is_integer()):
            return True
        else:
            return False
    except:
        return False


def loadCsv(inputfilename, servername, user, password, dbname, metric,
            timecolumn, timeformat, tagcolumns, fieldcolumns, usegzip,
            delimiter, batchsize, datatimezone, usessl):

    """

    :param inputfilename:
    :param servername:
    :param user:
    :param password:
    :param dbname:
    :param metric:
    :param timecolumn:
    :param timeformat:
    :param tagcolumns:
    :param fieldcolumns:
    :param usegzip:
    :param delimiter:
    :param batchsize:
    :param datatimezone:
    :param usessl:
    :return:
    """

    host = servername[0:servername.rfind(':')]
    port = int(servername[servername.rfind(':') + 1:])
    client = InfluxDBClient(host, port, user, password, dbname, ssl=usessl)

    client.switch_user(user, password)

    if tagcolumns:
        tagcolumns = tagcolumns.split(',')
    if fieldcolumns:
        fieldcolumns = fieldcolumns.split(',')

    datapoints = []
    # for x in os.listdir('/Users/eb/Downloads/golog/'):

    inputfile = open(inputfilename, 'r')
    count = 0
    with inputfile as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            datetime_naive = datetime.datetime.strptime(row[timecolumn], timeformat)

            if datetime_naive.tzinfo is None:
                datetime_local = timezone(datatimezone).localize(datetime_naive)
            else:
                datetime_local = datetime_naive

            timestamp = unix_time_millis(datetime_local) * 1000000  # in nanoseconds

            tags = {}
            for t in tagcolumns:
                v = 0
                if t in row:
                    v = row[t]
                tags[t] = v

            fields = {}
            for f in fieldcolumns:
                v = 0
                if f in row:
                    if isfloat(row[f]):
                        v = float(row[f])
                    elif isbool(row[f]):
                        v = str2bool(row[f])
                    else:
                        v = row[f]
                fields[f] = v

            point = {"measurement": metric, "time": timestamp, "fields": fields, "tags": tags}

            datapoints.append(point)
            count += 1

            if len(datapoints) % batchsize == 0:
                print('Read %d lines' % count)
                print('Inserting %d datapoints...' % (len(datapoints)))
                response = client.write_points(datapoints)

                if not response:
                    print('Problem inserting points, exiting...')
                    exit(1)

                print("Wrote %d points, up to %s, response: %s" % (len(datapoints), datetime_local, response))

                datapoints = []

    if len(datapoints) > 0:
        print('Read %d lines' % count)
        print('Inserting %d datapoints...' % (len(datapoints)))
        response = client.write_points(datapoints)

        if response == False:
            print('Problem inserting points, exiting...')
            exit(1)

        print("Wrote %d, response: %s" % (len(datapoints), response))

    print('Done')

def start_timer():
    request.start_time = time.time()

if __name__ == '__main__':
    read_csv_param = dict(low_memory=False, na_values=[' ', '', 'null'], )
    # for x in os.listdir('/Users/eb/Downloads/golog/'):
    #     print(x)

    li = []
    all_files = ('/Users/eb/Downloads/golog/res1.csv', '/Users/eb/Downloads/golog/res2.csv')

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)
    print(df.columns)
    print('df:  ', df['host'].unique())
    # print('df2:  ', df2['host'].unique())
    # df.merge(df2, how='left')
    # print('df.append:  ', df['host'].unique())

    df['measurement'] = 'omni'
    df['SimpleCount'] = int(1)
    df['ErrorCount'] = int(0)
    df["DateTime"] = pd.to_datetime(df["DateTime"], format="%d.%m.%Y %H:%M:%S.%f")
    df['timestamp'] = df.DateTime.values.astype(pd.np.int64) // 1
    df.set_index('timestamp')

    df.to_csv(
        "results_table.csv",
        index=False,
        columns=["DateTime", "Method", "host", "DiffTime", "measurement", "SimpleCount", "ErrorCount"],
    )

    labels_list_request = set()
    labels_list_transaction = set()


    def _get_unique_label():
        ''' списки уникальных лейблов '''
        labels_list = df['Method'].unique()
        for _ in labels_list:
            if 'tc_' in _:
                labels_list_transaction.add(_)
            else:
                labels_list_request.add(_)


    _get_unique_label()
    # print(labels_list_request)
    # print(len(labels_list_request))

    ok = df
    ok['timeStamp_round'] = [round(a / 1) * 1 for a in ok.index]
    df_elapsed = ok.pivot_table(
        columns=['Method'], index='timeStamp_round', values='DiffTime', aggfunc=pd.np.mean)

    # print(df_elapsed.head(1))
    print("\n---Таблица времени отклика:")
    print('label,max,pct99.9,pct99,pct98,pct90,pct75,pct50,pct25,min,std.dev')
    results_string = None

    for label in labels_list_request:
        try:
            print("{},{},{},{},{},{},{},{},{},{},{}".format(
                label,
                int(df_elapsed[label].max()),
                int(df_elapsed[label].quantile(0.999)),
                int(df_elapsed[label].quantile(0.99)),
                int(df_elapsed[label].quantile(0.98)),
                int(df_elapsed[label].quantile(0.95)),
                int(df_elapsed[label].quantile(0.90)),
                int(df_elapsed[label].quantile(0.75)),
                int(df_elapsed[label].quantile(0.50)),
                int(df_elapsed[label].quantile(0.25)),
                int(df_elapsed[label].min()),
                int(df_elapsed[label].std()))
            )
        except:
            pass

    loadCsv(
        batchsize=5000,
        dbname='omni_results',
        delimiter=',',
        fieldcolumns='DiffTime,SimpleCount,ErrorCount,ErrorCount',
        usegzip=False,
        inputfilename='results_table.csv',
        metric='omni',
        password='root',
        servername='localhost:8086',
        usessl=False,
        tagcolumns='Method,host',
        timecolumn='DateTime',
        timeformat='%Y-%m-%d %H:%M:%S.%f',
        datatimezone='UTC',
        user='root'
    )
