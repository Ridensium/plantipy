"""
Start up of the wrangler dev server in the direcory of that script

[wrangler configuration](https://developers.cloudflare.com/workers/wrangler/configuration/)
[wrangler commands](https://developers.cloudflare.com/workers/wrangler/commands/#dev)
"""

import os
import subprocess

# Get the directory of the current script
tests_directory = os.path.dirname(os.path.abspath(__file__))

print('executing wrangler in:', tests_directory)

#running with secure context with local ip (not just localhost)
#that way can be accesed from test devices in the network
#and all js stuff which need secure context will work
command = "npx wrangler dev --ip 0.0.0.0 --port 443 --local-protocol https"

# Execute the command in the terminal
subprocess.run(command, shell=True, check=True, cwd=tests_directory)
