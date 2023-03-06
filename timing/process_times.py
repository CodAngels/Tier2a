import json

data = json.loads(open("timing/cs178-tier-2a-default-rtdb-export.json").read())
with open("timing/times.csv", "w") as f:
    for _, user in data["submissions"].items():
        f.write(str(user["name"]) + "," + str(user["time_taken"]) + "\n")