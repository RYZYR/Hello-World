from .models import *
class TupleClass:
    weekdayTuple = ((1,'周一'),(2,'周二'),(3,'周三'),(4,'周四'),(5,'周五'))

    def weekTuple():
        count = 1
        weekList=[]
        while count<=18:
            weekList.append((count,"第{}周".format(count)))
            count+=1
        return tuple(weekList)

    def secTuple():
        count = 1
        secList=[]
        while count<=14:
            secList.append((count,"第{}节".format(count)))
            count+=1
        return tuple(secList)