<%
import re
pattern_docstrings = r'("|\'){3}(?:.|\n)*?("|\'){3}'
pattern_begin_line = r'^\s*'

CLASSES = module.classes(sort=sort_identifiers)
FUNCTIONS = module.functions(sort=sort_identifiers)
VARIABLES = module.variables(sort=sort_identifiers)
NAME = module.name
SUPER = module.supermodule



# PARSE DOCS ---------------------------------------------------------------
def parse_docstrings(item):
    lines = item.docstring.splitlines()
    for l in range(len(lines)):
        line = lines[l]
        if len(line) > 0:
            line = re.sub(pattern_begin_line, '', line, flags=re.DOTALL)
            lines[l] = f'> {line}' if line not in ['[!NOTE]', '[!TIP]','[!IMPORTANT]','[!WARNING]','[!CAUTION]'] else f'\n> {line}'
    return '\n'.join(lines)
# -----------------------------------------------------------------------------

# PARSE METHOD ---------------------------------------------------------------
def parse_method(class_name, item):
    params = item.params(annotate=show_type_annotations)
    params = ", ".join(params)
    returns = parse_returns(item)
    docstrings = parse_docstrings(item)
    source = parse_source(item)
    detail = f"""
<details><summary><i>{class_name}</i>.<b>{item.name}</b></summary>

  ```python
{source}
  ```
  
</details>
"""

    text = f"""
{detail}
`{item.name}({params})`{returns}
{docstrings}
"""
    return text
# -----------------------------------------------------------------------------



# PARSE CLASS ---------------------------------------------------------------
def parse_class(item):
    name = item.name
    params = item.params()
    params = f"({', '.join(p for p in params)})" if params else ''
    docstrings = parse_docstrings(item)

    methods = item.methods(show_inherited_members, sort=sort_identifiers)
    stat_methods = item.functions(show_inherited_members, sort=sort_identifiers)

    methods = f"#### methods:\n{parse_methods(name, methods)}" if methods else ''
    stat_methods = f"#### static and class methods:\n{parse_methods(name, stat_methods)}" if stat_methods else ''

    text = f"""---
### _class_ {name}
`{NAME}.{name}{params}`
{docstrings}
{methods}
{stat_methods}
"""
    return text
# -----------------------------------------------------------------------------

# PARSE METHODS ---------------------------------------------------------------
def parse_methods(class_name, methods):

    return '\n'.join([parse_method(class_name, item) for item in methods])
# -----------------------------------------------------------------------------


# PARSE CLASSES ---------------------------------------------------------------
def parse_classes():
    classes = '\n'.join([parse_class(item) for item in CLASSES]) if CLASSES else ''
    return f'### Classes:\n{classes}\n---' if classes else ''
# -----------------------------------------------------------------------------

# PARSE RETURNS ------------------------------------------------
def parse_returns(item):
    returns = show_type_annotations and item.return_annotation() or ''
    if returns:
        return f" -> `{returns}`"
    else:
        return ''
# -------------------------------------------------------------



# PARSE FUNC ---------------------------------------------------------------
def parse_func(item):
    params = item.params(annotate=show_type_annotations)
    params = ", ".join(params)
    returns = parse_returns(item)
    docstrings = parse_docstrings(item)
    source = parse_source(item)

    detail = f"""
<details><summary><i>{NAME}<i>.<b>{item.name}</b></summary>

```python
{source}
```
    
</details>
"""


    text = f"""---
{detail}
`{item.name}({params})`{returns}
{docstrings}

"""
    return text
# ---------------------------------------------------------------------



# PARSE FUNCTIONS ---------------------------------------------------------------
def parse_functions():
    functions = '\n'.join([parse_func(item) for item in FUNCTIONS]) if FUNCTIONS else ''
    return f'### Functions:\n{functions}\n---' if functions else ''
# -----------------------------------------------------------------------------






# PARSE GLOBAL -------------------------------------------------------------
def parse_gvar(item):
    text = f"""
{item.name}
parse_docstrings(item)
    return text
"""
#-------------------------------------------------------------------------

# PARSE GLOBALS -------------------------------------------------------------
def parse_gvars():
    gvars = '\n'.join([parse_gvar(item) for item in VARIABLES]) if VARIABLES else ''
    return f'## Global VARIABLES:\n{gvars}\n---' if gvars else ''
#-------------------------------------------------------------------------


# PARSE SOURCE ------------------------------------
def parse_source(item):
    source = item.source
    source = re.sub(pattern_docstrings, '', source, flags=re.DOTALL)
    source = re.sub(r'#.*$', '', source, flags=re.MULTILINE)
    return source
# -----------------------------------------

#END
%>

${'# ' + module.name + '.py'}
${parse_docstrings(module)}

${parse_classes()}

${parse_functions()}

${parse_gvars()}