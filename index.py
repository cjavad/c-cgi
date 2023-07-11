#!/usr/bin/env python3

import cgi
import hashlib

form = cgi.FieldStorage()

root = "/var/www/html"
# cd to root directory
import os
os.chdir(root)

# Get GET variable "text" and compile jinja2 template c-template.c.jinja2 with the variable template_var
# then compile C code into output in folder endpoints/md5-hash of template and make redirect to the output
if "text" in form:
    template_var = form["text"].value
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(root))
    template = env.get_template('c-template.c.jinja2')
    output = template.render(template_var=template_var)

    hash_of_text = hashlib.md5(template_var.encode('utf-8')).hexdigest()

    with open(f"{hash_of_text}.c", "w") as f:
        f.write(output)

    # compile C code into executable
    import subprocess
    subprocess.run(["gcc", f"{hash_of_text}.c", "-o", f"endpoints/{hash_of_text}"])

    # Fial if compilation failed
    if not os.path.isfile(f"endpoints/{hash_of_text}"):
        print("Status: 500 Internal Server Error\n")
        print("Content-type: text/html\n")
        print("Compilation failed")
        exit()

    # Make executable chmod +x
    subprocess.run(["chmod", "+x", f"endpoints/{hash_of_text}"])

    # cleanup temp files
    import os
    os.remove(f"{hash_of_text}.c")

    print("Status: 302 Found")
    print(f"Location: /endpoints/{hash_of_text}\n")
    print("Content-type: text/html\n")

print("Status: 400 Bad Request\n")