"""
Making docs from the source in markdown
SHOUD BE RUN FROM PROJECT FOLDER
"""

import os, sys, pdoc, subprocess
from pdoc import tpl_lookup
from unittest.mock import MagicMock



SRC = './src' #source file directory
DOCS = './docs/dev_docs' #docs directory
DOC_TEMPL = './_tools/doc_templates' #mako doc templates

EXCLUDE = ['pyscript', 'js'] #

# Ensure the 'src' directory is in the Python module search path so no need tu run pdoc there
sys.path.insert(0, os.path.abspath(SRC))

# Mock external modules you want to exclude
# neede because pdoc tryes to parse pyscript from there polyscript an so on ...

for e in EXCLUDE:
    sys.modules[e] = MagicMock()

# Get a list of python files in the SRC
files = [f for f in os.listdir(SRC) if os.path.isfile(os.path.join(SRC, f))]
modules = [f[:-3] for f in files if f.endswith('.py')]
print('Modules', modules)


tpl_lookup.directories.insert(0, DOC_TEMPL)


context = pdoc.Context()

# Create pdoc.Module objects for each module, skipping the excluded ones
modules = [pdoc.Module(mod, context=context)
           for mod in modules if mod not in EXCLUDE]

# Link inheritance in the pdoc context
pdoc.link_inheritance(context)

# recursively gather module documentation as HTML or Markdown
def recursive_htmls(mod):
    yield mod.name, mod.text()  # Yield the module's name and text
    #for submod in mod.submodules():
    #    if submod.name not in EXCLUDE:
    #        yield from recursive_htmls(submod)  # Recursively handle submodules

# Create output directory if it doesn't exist
os.makedirs(DOCS, exist_ok=True)

# Iterate through the modules and write documentation to files
for mod in modules:
    print(f"Generating doc for {mod.name}...")
    for module_name, text in recursive_htmls(mod):
        # Generate Markdown file for each module
        file_path = os.path.join(DOCS, f'{module_name}.md')
        with open(file_path, 'w') as f:
            f.write(text)

print("Documentation generation complete.")
