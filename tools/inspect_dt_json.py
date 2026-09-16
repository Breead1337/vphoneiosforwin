import json

data = json.load(open(r"D:\vphonewin\work\dtree.json", "r", encoding="utf-16"))

def search(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "children":
                search(v, path)
            else:
                subpath = f"{path}/{k}" if path else k
                if isinstance(v, dict):
                    if "reg" in v:
                        print(f"Node: {subpath} -> reg: {v['reg']}")
                    for prop in v:
                        if any(x in prop.lower() for x in ["sram", "mem", "range", "config"]):
                            print(f"  {subpath} -> {prop}: {v[prop]}")
                    search(v, subpath)
    elif isinstance(obj, list):
        for item in obj:
            search(item, path)

search(data)
