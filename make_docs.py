"""
a simple module for making documentation of the package
---
plantipy - @Ridensium - 2005
"""

import os, sys, inspect, importlib, re
from unittest.mock import MagicMock

#source file directory
SRC = './src' 

#draft docs directory
DOCS = './docs/dev_docs'

# excluded packages
EXCLUDE = ['pyscript', 'js', 'window', 'navigator', 'document']

# template for all objects
OBJECT_TEMPLATE = """{heading} *{type}*:  {name}()

<details><summary>{signature}</summary>


  ```python
{source}
  ```


</details>


{info}


"""

# template for modules
MODULE_TEMPLATE = """## {name}

{info}

{classes}

{functions}

"""


# template for the package index
PACKAGE_TEMPLATE = """## {name}

{info}


Modules docs:


{modules}


"""


# mocking what need to exclide
for e in EXCLUDE:
    sys.modules[e] = MagicMock()

# converting src path to absolute
SRC = os.path.abspath(SRC)

# adding so to be found
if SRC not in sys.path:
    sys.path.insert(0, SRC)


# beautify the docstrings
def parse_docstrings(text):
    if not text:
        return ''
    pattern_docstrings = r'("|\'){3}(?:.|\n)*?("|\'){3}'
    pattern_begin_line = r'^\s*'
    lines = text.splitlines()
    for l in range(len(lines)):
        line = lines[l]
        if len(line) > 0:
            #clean empty at begining
            line = re.sub(pattern_begin_line, '', line, flags=re.DOTALL)
       
            # to make texts as quotes but
            #lines[l] = f'> {line}' if line in ['[!NOTE]', '[!TIP]','[!IMPORTANT]','[!WARNING]','[!CAUTION]'] else f'\n> {line}'
    
    
    return '\n'.join(lines)

# clean the source for the expand section
def parse_source(source):
    pattern_docstrings = r'("|\'){3}(?:.|\n)*?("|\'){3}'
    source = re.sub(pattern_docstrings, '', source, flags=re.DOTALL)
    source = re.sub(r'#.*$', '', source, flags=re.MULTILINE)
    return source



class Package:
    def __init__(self, name, obj):
        doc = inspect.getdoc(obj)
       
        modules = [Module(name, obj) for name, obj in inspect.getmembers(obj, inspect.ismodule) if name not in EXCLUDE]
        
        file_path = os.path.join(DOCS, f'_{name}_.md')
        
        parsed_doc = PACKAGE_TEMPLATE.format(
            name=name,
            info = parse_docstrings(doc),
            modules = '\n'.join([f'- [{m.name}]({m.name}.md)' for m in modules])
        )

        with open(file_path, 'w') as f:
            f.write(parsed_doc)

        print('package:', name, file_path)

class Object:
    """super class for all objects"""
    heading:int = 3
    template = OBJECT_TEMPLATE


    def __init__(self, name, obj, type='object'):
        doc = inspect.getdoc(obj)
        source = inspect.getsource(obj)
        signature = str(inspect.signature(obj))
        self.name = name
        self.source = source
        self.signature = signature
        parsed_doc = parse_docstrings(doc)

        if signature.endswith(')'):
            signature=f'[{signature[1:-1]}]'
        else:
            signature = '[' + re.sub(r'\)\s*->', '] -> ', signature[1:])


        self.doc = self.template.format(
            heading = '#'*self.heading,
            type=type,
            name=name.replace('_', '\_'), #bec md
            signature=signature,
            info=parsed_doc,
            source=parse_source(source))  

class Module:
    """class for parsing the modules"""
    def __init__(self, name, obj):
        self.name = name
        self.obj = obj
        doc = inspect.getdoc(obj)
        classes = [Class(name, _obj) for name, _obj in inspect.getmembers(obj, inspect.isclass) if _obj.__module__ == obj.__name__]
        functions = [Function(name, _obj) for name, _obj in inspect.getmembers(obj, inspect.isfunction)  if _obj.__module__ == obj.__name__]
   
        file_path = os.path.join(DOCS, f'{name}.md')
        
        parsed_doc = MODULE_TEMPLATE.format(
            name=name,
            info = parse_docstrings(doc),
            classes = '\n'.join([c.doc for c in classes]),
            functions = '\n'.join([f.doc for f in functions])

        )

        with open(file_path, 'w') as f:
            f.write(parsed_doc)

        print('module:', name, file_path)

class Function(Object):
    """class for parsing the funtions in the Module"""
    heading:int = 2
    def __init__(self, name, obj):
        super().__init__(name, obj, type='function')
     

class Method(Object):
    """class for parsing the methods in the Class"""
    def __init__(self, name, obj):
        super().__init__(name, obj, type='method')

class MethodS(Object):
    """class for parsing the static and class methods in the Class"""
    def __init__(self, name, obj):
        super().__init__(name, obj, type='static/class method')

class Class(Object):
    """class for the classes in module"""
    heading:int = 2
    def __init__(self, name, obj):
        super().__init__(name, obj, type='class')

        functions = [Method(name, _obj) for name, _obj in inspect.getmembers(obj, inspect.isfunction)]
        callables = [MethodS(name, _obj) for name, _obj in inspect.getmembers(obj, inspect.isroutine) if not name.startswith('__') and not inspect.isfunction(_obj)]
        
        for f in functions:
            self.doc += f.doc

        for c in callables:
            self.doc += c.doc


# run the module for making the docs
def make(package='src'):
    package = importlib.import_module(package)
    name = os.path.basename(os.path.dirname(SRC))
    os.makedirs(DOCS, exist_ok=True)
    Package(name, package)


if __name__=="__main__":
    make()