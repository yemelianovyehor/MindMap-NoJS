import os
import sys
import json

'''
Generates the index.html and a json files from [argument 1] file. defaults to list.txt

the list.txt is a hierarchical list.
example:
```txt
A:
    B:
        C
    D
    E:
        F
    Q:
    P
    G:
        W
        R
        T:
            Y
```
tabs and ":" are important here.
'''
#Input File
IF = "list.txt"
if(len(sys.argv)>1):
    IF = sys.argv[1]

class node:
    def __init__(self, name, children):
        self.label = name
        self.children = children

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=False,
            indent=4)

# Read data from Input File
with open(IF, 'r') as file:
    lines = file.readlines()

# Function to parse the list.txt data into a nested structure
def parse_lines(lines):
    depth = []
    root = node('',[])
    for line in lines:
        tabs = line.count('\t')+line.count("    ")
        line = line.strip()
        if not line:
            continue
        
        name = line.replace(":","").strip()
        new_node = node(name,[]) 
        if len(depth) == 0:
            depth.append(new_node)
            root = new_node
            continue
        if tabs >= len(depth):
            parent = depth[-1]
            parent.children.append(new_node)
        else:
            diff = len(depth) - tabs
            depth = depth[:tabs]
            parent = depth[-1]
            parent.children.append(new_node)
        if line.endswith(":"):
            depth.append(new_node)
    return root

# Generate HTML content from the nested structure
def generate_html(node):
    html = ""
    html += f'    <li>\n'
    html += f'        <input type="checkbox" id="{node.label.replace(" ", "-").lower()}-toggle">\n'
    html += f'        <label for="{node.label.replace(" ", "-").lower()}-toggle">{node.label}</label>\n'
    
    if node.children:
        html += '<ul>\n'
        for child in node.children:
            html += generate_html(child)
        html += '</ul>\n'

    html += '    </li>\n'
        
    return html

# Parse the lines from list.txt
parsed_data = parse_lines(lines)
print("Parsed Data:", parsed_data.toJSON())

# Generate the HTML content
html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mindmap</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="mindmap">
        <ul>
            {generate_html(parsed_data)}
        </ul>
    </div>
</body>
</html>
'''

# Write the generated HTML content to a new file
with open('index.html', 'w') as file:
    file.write(html_content)
with open('mindmap.json', 'w') as file:
    file.write(parsed_data.toJSON())

print("HTML file generated successfully.")