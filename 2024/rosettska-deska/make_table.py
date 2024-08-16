import sys
import json

T = json.load(open("table.json"))

for key, value in T.items():
    print("<tr>")
    print(f"<td>{key}</td>")
    print(f"<td>{value}</td>")
    print("</tr>")

print("")

for key, value in T.items():
    print("<tr>")
    print(f"<td>{value}</td>")
    print(f"<td>{key}</td>")
    print("</tr>")
