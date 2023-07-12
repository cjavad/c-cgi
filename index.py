#!/usr/bin/env python3

import cgi
import hashlib
import subprocess
import random
from jinja2 import Environment, FileSystemLoader

root = "/app"
endpoint_dir = f"{root}/endpoints"

def random_hash_function():
    return random.choice([
        hashlib.sha1,
        hashlib.sha224,
        hashlib.sha256,
        hashlib.sha384,
        hashlib.sha512,
        hashlib.md5
    ])

def internal_server_error(message: str):
    print("Status: 500 Internal Server Error\n")
    print("Content-type: text/html\n")
    print(message)
    exit()

def bad_request():
    print("Status: 400 Bad Request\n")

def compile_endpoint(message: str) -> str:
    output = Environment(loader=FileSystemLoader(root)).get_template('c-template.jinja2').render(message=message)

    endpoint_hash = random_hash_function()(output.encode('utf-8')).hexdigest()

    # Compile from stdin
    echo = subprocess.Popen(["echo", output], stdout=subprocess.PIPE)
    proc = subprocess.run(["gcc", "-o", f"{endpoint_dir}/{endpoint_hash}", "-x", "c", "-"], stdin=echo.stdout, stderr=subprocess.PIPE)

    if proc.returncode != 0:
        internal_server_error(proc.stderr.decode("utf-8"))
    else:
        # Set executable bit
        subprocess.run(["chmod", "+x", f"{endpoint_dir}/{endpoint_hash}"])

    return endpoint_hash

def main(form: cgi.FieldStorage):
    if "message" in form:
        endpoint_hash = compile_endpoint(form["message"].value)
        print("Status: 302 Found")
        print(f"Location: /endpoints/{endpoint_hash}\n")
        print("Content-type: text/html\n")
    else:
        bad_request()

if __name__ == "__main__":
    main(cgi.FieldStorage())