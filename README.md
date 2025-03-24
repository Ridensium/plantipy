# plantipy

Template repository for [pyscript](https://pyscript.net) small projects.

The purpose of it is to ease the set up, typing autosugesttion and testing of projects, developed locally.

## Better typing and autosuggestion

- `/external_pyscript.py` will add pyscript repo as submodule here in the `/external/pyscript` directory, and will add symlink of python package there as `/src/pyscript`. Symlincs are not seen from git but to be on save side that is in `.gitignore`

- Pyscript has module `js` for the javascript global namespace, imported with `import js`. If you plan to use it plantipy comes with package inside `/external/js` which covers most of js objects as dummy python classes with lots of classes and attributes there. With `/external_js.py` you can add an symlink from that package as `/src/js` to your project.

## Building documentation

With `/make_docs.py` you can make documentation from the project from the source code. It works without requirements to install thirdparty libraries.
The script will export the documentation as `markdown` files to `/docs/dev_docs`. You can keep `../dev_docs` in `.gitignore` and copy in the parent `/docs` the official ones.

## Minify and zip the source code

The `/make_distro.py` will add minified `.py` files, together with others types except `.pyc`, to directory `/dist/dev/py` as well with zip file `/dist/dev/distro.zip` of all of them.

## Testing

Pyscript projects need web server to be tested and some apis need also a secure context. As some may chose later *cloudflare* as cheap and scalable alternative for publishing the project there is little setup for that in plantipy. Cloudflare supports from a while python (based on pyodide) so this make it even more interesting.

[README TESTING](tests/README.md)