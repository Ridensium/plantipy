# plantipy
Template repository for pyscript small projects.
The purpose of it to ease the set up, typos and testing small projects developed locally.


## Better typing
Classes for the javasript object proxies in js module to help typing when using them.
To use them make symlinc of `/external/js` to `/src/js` if your code will be in the `/src` folder. Need to keep the name as it is _js_.

__/full_path__ is path part at your device pointing to the cyted directories.

```
ln -s /full_path/external/js /full_path/src/js
```

It will make help also if clone pyscript repo as submodule and then make symlink of python part of it to src folder of the projet.

```
git submodule add https://github.com/pyscript/pyscript.git external/pyscript

ln -s /full_path/external/pyscript/core/src/stdlib/pyscript /full_path/src/pyscript
```

## Building documentation
Building documentation in markdown to be served with the repository via `/build/make_docs.py`.
That script will built markdown files for the python files located in the `/src` and put them into `/docs`.


## Minify and zip the source code
Minifying the source in separate folder, together with zipped file of the latter via `/build/minify_and_compress.py`.
It will save minified python files into `/dist/py` directory, and will add `/dist/distro.zip` compresing them.


## Testing
As some projects later may be hosted and one of the chiepes alternative is cloudflare the web test server is with wrangler a CLI tool for managin Cloudflare Workers.
Cloudflare supports from a while python (based on pyodide) so this will prevent for playng with javascrip or other languages/platform on that server part.
Directory for all of this is `/tests`.
It contains:

- `wrangler.toml` preconfigured settings for running the server
- `wrangler.py` the very server worker as simple possible
- `index.html` index web page of the website running with script tag `<script type="mpy" src="index.py" config="config.toml" terminal></script>` 
- `index.py` the pyscript python file loaded in the script tag above
- `config.toml` the pyscript settings loaded from the script tag above
- `_RUN_SERVER.py` a python script for running the wrangler worker as web server on your local ip (not just localhost) in secure context so to be able to test on other devices on your network. The secure context is needed because some javascript apis of the browser needed it.

You can install the **wrangler** using **npm**, which requires **Node.js**. If you dont have the latter can download and install it from [nodejs.org](nodejs.org). 
After you have Node.js (npm comes with it) can install the **wrangler**:

```
npm install -g wrangler
```
[cloudflare docs](https://developers.cloudflare.com/workers/wrangler/install-and-update/)


## Online development
For developing in a browser the best and maybe only solution is the official one - [pyscript.com](pyscript.com)