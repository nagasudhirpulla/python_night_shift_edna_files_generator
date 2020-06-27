import datetime as dt
from subprocess import Popen, PIPE, TimeoutExpired


def fetchEdnaHistData(pnt, startTime, endTime, type='snap', secs=60, includeQuality=False):
    # get timestamp from datetime
    startMs = dt.datetime.timestamp(startTime)*1000
    endMs = dt.datetime.timestamp(endTime)*1000

    command = ["./EdnaConsoleAdapter.exe", "--from_time", str(int(startMs)),
               "--to_time", str(int(endMs)),
               "--type", type,
               "--secs", str(int(secs)),
               "--meas_id", pnt]
    
    if includeQuality == True:
        command.append("--include_quality")
    
    proc = Popen(command, stdout=PIPE)
    try:
        outs, errs = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
    resp = outs.decode("utf-8")
    # split the response by comma
    respSegs = resp.split(',')
    if len(respSegs) < 2:
        return None
    else:
        histData = []
        step = 2
        if includeQuality == True:
            step = 3
        for respIter in range(0, len(respSegs), step):
            sampleObj = {
                't': dt.datetime.fromtimestamp(
                    float(respSegs[respIter])/1000),
                'v': float(respSegs[respIter+1])
            }
            if includeQuality == True:
                sampleObj['q'] = int(respSegs[respIter+2])
            histData.append(sampleObj)
        return histData