import mmap
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt


def formatToPlot(values):
    with mmap.mmap(-1, length=150000) as f:
        r = list(range(len(values)))
        plt.figure(figsize=[12, 8])
        plt.plot(r, [v[1] for v in values])

        s = slice(0, len(values), len(values)//10)
        plt.xticks(r[s], (v[0].strftime("%Y-%m-%d %H:%M") for v in values[s]), size='small', rotation='12')

        plt.savefig(f)

        size = f.tell()
        f.seek(0)
        bytesOfFile = f.read(size)
        f.close()

    return bytesOfFile


def formatToHtmlTable(values, req):
    req.write("<table border='1'>\n")
    for r in values:
        req.write("\t<tr>\n")
        for c in r:
            req.write('\t\t<td>{}</td>\n'.format(c))
        req.write("\t</tr>\n")
    req.write("</table>")


if __name__ == '__main__':
    import datetime

    now = datetime.datetime.now()
    data = [[now + datetime.timedelta(minutes=i * 10), i] for i in range(100)]
    with open("temp.html", "w") as f:
        formatToHtmlTable(data, f)
    with open("temp.png", "wb") as f:
        f.write(formatToPlot(data))
        f.close()
