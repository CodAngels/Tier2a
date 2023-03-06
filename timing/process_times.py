import json, datetime

data = json.loads(open("timing/cs178-tier-2a-default-rtdb-export.json").read())
with open("timing/times.csv", "w") as f:
    f.write("Name,Start Time,End Time,Duration\n")
    for _, user in data["submissions"].items():
        time_elapsed_ms = user["end_time"] - user["start_time"]
        f.write(str(user["name"]) + "," + 
                datetime.datetime.fromtimestamp(user["start_time"] / 1000).strftime("%H:%M:%S") + "." + str(user["start_time"] % 1000) + "," +
                datetime.datetime.fromtimestamp(user["end_time"] / 1000).strftime("%H:%M:%S") + "." + str(user["end_time"] % 1000) + "," + 
                str((time_elapsed_ms // (1000*60)) % 60) + ":" + str((time_elapsed_ms // 1000) % 60) + "." + str(time_elapsed_ms % 1000) + "\n")