import subprocess
import datetime

DEST = ["10.0.8.1", "45.95.45.254", "45.95.45.138"]


def create_result_template():
    """
    Function that returns string of formatted datetime stamp prepared for other tests to append its results to this
    string
    """
    result = ""
    time_now = datetime.datetime.now()
    time_now = str(time_now).split(".")[0]
    result += time_now + "\n"

    return result


def ping_test(destinations: list):
    """
    Function that makes ping test for all destinations passed as parameter.
    It appends each result to formatted string that is appended to text file.
    """
    # initial message
    print("Probíhá test ping...")

    result = create_result_template()

    # ping all destinations, and populates string result
    for dest in destinations:
        try:
            ping = subprocess.check_output(f"ping {dest}")
            ping = "".join(map(chr, ping))
        except subprocess.CalledProcessError:
            ping = f"ping not available for {dest}"

        result += ping + "\n"

    # writes result to a file
    with open("log.txt", mode="a") as file:
        file.write(result)

    # final message
    print("Test ping ukončen.")
    print("------------------")


def tracert_test(destinations: list):
    """
    Function that makes tracert test for all destinations passed as parameter.
    It appends each result to formatted string that is appended to text file.
    """
    print("Probíhá test traceroute")

    result = create_result_template()
    for dest in destinations:
        tracert = subprocess.check_output(f"tracert -h 10 {dest}")
        tracert = "".join(map(chr, tracert))

        result += tracert + "\n"

    with open("log.txt", mode="a") as file:
        file.write(result)
    print("Test traceroute ukončen.")
    print("------------------------")


print("========================================================")
print("Monitoring sítě je spuštěný, prosím nevypínej toto okno!")
print("========================================================")

start_ping = datetime.datetime.now()
start_tracert = start_ping

while True:

    now = datetime.datetime.now()

    if now - start_tracert > datetime.timedelta(minutes=15):
        tracert_test(destinations=DEST)
        start_tracert = datetime.datetime.now()

    elif now - start_ping > datetime.timedelta(seconds=10):
        ping_test(destinations=DEST)
        start_ping = datetime.datetime.now()


