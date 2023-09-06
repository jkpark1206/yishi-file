import time
import os


class Timer:
        imax = 0
        def __init__(self):
                self.start = time.time()
                #print("imax=%d" % self.imax)

        def restart(self):
                self.start = time.time()

        def get_elapsedtime_inminutes(self):
                end = time.time()
                m, s = divmod(end - self.start, 60)
                return int(m)

        def get_elapsedtime_inseconds(self):
                end = time.time()
                #m, s = divmod(end - self.start, 60)
                return int(end - self.start)

        def is_timeupminutes(self, imax):
                #print("elapsed=%d"% self.get_elapsedtime_inminutes())
                #print("imax=%d" % self.imax)
                return self.get_elapsedtime_inminutes() >= imax
        
        def is_timeupseconds(self, imax):
                #print("elapsed=%d"% self.get_elapsedtime_inminutes())
                #print("imax=%d" % self.imax)
                return self.get_elapsedtime_inseconds() >= imax

def get_datetimestring():
    now = int(time.time())     
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
    return otherStyleTime
            
def run_fast_scandir(dir, ext, notext):    # dir: str, ext: list, notext: list
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if(len(ext) > 0 ):
                if os.path.splitext(f.name)[1].lower() in ext:
                    files.append(f.path)
            if(len(notext) > 0):
                if os.path.splitext(f.name)[1].lower() not in notext:
                    files.append(f.path)
    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir, ext, notext)
        subfolders.extend(sf)
        files.extend(f)
    for index in range(len(files)):
        files[index] = files[index].replace("/", "\\")
    return subfolders, files

#subfolders, files = run_fast_scandir("//fengxiaoyang/Share/FW Samples/新下载", [], [".txt", ".html"])
#print(*files, sep='\n')
