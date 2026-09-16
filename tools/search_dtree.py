import json

with open(r"D:\vphonewin\work\dtree.json", "rb") as f:
    raw_content = f.read()
if raw_content.startswith(b'\xff\xfe') or raw_content.startswith(b'\xfe\xff'):
    data = json.loads(raw_content.decode('utf-16'))
else:
    data = json.loads(raw_content.decode('utf-8'))

def search_nodes(node, path=""):
    name = node.get("name", "")
    cur_path = f"{path}/{name}" if path else name
    props = {k: v for k, v in node.items() if k != "children"}
    if "reg" in props:
        print(f"Path: {cur_path}")
        print(f"  reg: {props['reg']}")
    for k, v in props.items():
        if "mem" in k or "range" in k or "sram" in k or "config" in k:
            print(f"Path: {cur_path} | {k}: {v}")
    for child in node.get("children", []):
        search_nodes(child, cur_path)

search_nodes(data)
