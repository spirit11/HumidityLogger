import cgi
import RequestHandler
import sys
import datetime


def parseDateTimeString(s, isBeginning):
    year = int(s[:4])
    month = int(s[4:6])
    day = int(s[6:8])

    if len(s) == 8:
        if isBeginning:
            hour = 0
            minute = 0
            second = 0
        else:
            hour = 23
            minute = 59
            second = 59
    else:
        hour = int(s[8:10])
        minute = int(s[10:12])
        second = int(s[12:14])

    return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)


# ----------------main-------------------------
form = cgi.FieldStorage()

range_query = 'from' in form and 'to' in form
last_query = 'last' in form

if not range_query and not last_query:
    print('Content-type: text/html\n')
    print('<title>Reply Page</title>')
    print('<h1>select from and to range or last(hour,day)</h1>')
else:
    try:
        import DatabaseConfig

        if range_query:
            fromTime = parseDateTimeString(form['from'].value, True)
            toTime = parseDateTimeString(form['to'].value, False)
        else:
            toTime = datetime.datetime.now()
            dt = datetime.timedelta(days=1) if form['last'] == 'hour' else datetime.timedelta(hours=1)
            fromTime = toTime - dt

        data = DatabaseConfig.db.getValues(fromTime, toTime)

        plot = RequestHandler.formatToPlot(data)
        print('Content-type: image/png\n')
        sys.stdout.buffer.write(plot)

    except Exception as e:
        print('Content-type: text/html\n')
        print(e)
