import os;


def start():
    timer = getTimeInput()
    sure = ""
    while sure.lower() != "y" and sure.lower() != "n":
        sure = areYouSure(timer)

    if sure.lower() == "y":
        cmd = "shutdown /s /t " + str(getSeconds(timer))
        os.system("shutdown /s /t " + str(getSeconds(timer)))
        print("Computer will shutdown in " + printTime(timer))
    else:
        start()


def getTimeInput():
    timer = 0
    while timer <= 0 or not isinstance(timer, float):
        inputTime = input("Timer (Minutes): ")
        try:
            timer = float(inputTime)
        except Exception as e:
            print("input cannot be converted to float!")
    return timer


def getSeconds(time):
    return int(time * 60.0)


def areYouSure(time):
    ans=""
    while ans.lower() != "y" and ans.lower() != "n":
        ans = input("Are you sure want to shutdown computer in " + printTime(time) + "? y/n ")
    return ans

def printTime(time):
    return str(time) + " minutes (" + str(getSeconds(time)) + " s)"

if __name__ == '__main__':
    start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
