<h1 align="center">Process Chain</h1>

Multiple process are connected together to form a process chain that implements a function. The process chain is called pchain, which is a new type of programming concept and method.

Python Interface
------

The python interface provides basic manipulation of the pchain, but does not limit the implementation of each process. Process implementation can be implemented in multiple languages such as c/c++, java, python, c#

For example, the following code executes a process chain

```python
from pchain import runner
runner.run('chain.py')
```
    
pchain
------

Define some basic environment variables

#### a. variables

>   **nativepath** : path of native library 'star_pchain.dll/so/dylib'
>   **webpath**    : path of web page
>   **platform**   : may be 'windows', 'linux', 'darwin', apps can change it's value for other platforms
>   **userpath**   : path of pchain to save log or package
>   **packagepath** : path of pchain packages installed
>   **SystemPackageInfo** : packages loaded by pchain, which must be set from object 'pcrealm'
>   **templatepath** : save template for package or project

#### b. functions

>    **cleinit()** : init cle core, load pchain share library. This function must be called first
>    **cleloop()** : dispatch cle message, press 'ESC' to exit
>    **cleterm()** : clear cle core.

for example,

```python
import pchain
pchain.cleinit()
realm = Service.PCRealmBase._New()
```

runner
------

Initialize CLE, create default 'test' service, load and execute process chain file

**run(filename,debugmode=False)**

debugmode : 
>    false, the process chain file will be run to finish.
>    true, start web server using 'flask' at port 4000. Using web browser to view running status of each process, and run step by step.

```python
from pchain import runner
runner.run('xxxxx')
```

debug
----

Start web server using 'flask' at port 4000. Using web browser to view running status of each process, and run step by step.

**start()**

```python
from pchain import debug
debug.start()
```

pack
----

Used to generate packages. This function parses the ‘packageinfo.json’ file in the current directory. If it is a python package, it uses ‘pipreqs’ to generate the 'requirements.txt' dependency. Then, package all the files in the current directory into a compressed package in '.zip' format.

**pack()**

in current directory, execute the following code

```python
from pchain import pack
pack.pack()
```

loader
----

Load a locally installed package; either, download the package remotely, install it locally, and load it at the same time; or load the local '.zip' package, or install the local '.zip' package, or load a directory in that directory Contains the 'packageinfo.json' file

Before calling this function, CLE must have been initialized, the default service has been created, and 'star_pchain.dll/so/dylib' has been loaded correctly.

**namespace = load(PackageName,PackageVersion='',PrintFlag=True)**

Returns a cle namespace object if the package is already installed locally, through which the process types and data types defined in the package can be accessed.

Otherwise returns None

> **PackageVersion** : may be empty, or else, is such as '1.0.0'
> **PrintFlag**
>>    - true ：print error message to console
>>    - false : do not print any message

**namespace = loadurl(url)**

If the package is already installed locally, it will load and return True; otherwise, download the package from url, install it, then load it, and return True

**namespace = loadzip(zipfilename,installIgnoreVersion = False)**

If the package is already installed locally, it will be loaded and return True; otherwise, the package will be installed, the load it, and return True

**namespace = loadfolder(Folder)**

load package from floder

> Floder : package folder

```python
from pchain import loader
package = loader.loadzip('xxxxx.1.0.0.zip')
package = loader.loadurl('http://xxx.xxx.xxx/xxxxx.1.0.0.zip')
package = loader.load('mypackage')
```

Python Tools
----

#### a. pcrunner.py

Load and execute process chain files

**usage : python pchain/tools/pcrunner.py [--DEBUG] xxx.py**

If '--DEBUG' is set, after loading, start the local Web Server with 'flask'. The execution status of the process chain can be viewed through the browser, or it can be performed in a single step.

or

```python
from pchain.tools import pcrunner
pcrunner.do('--debug','xxxx.py')  or
pcrunner.do('xxxx.py')
```

#### b. pcpack.py

The file in a directory is marked as a '.zip' archive containing the 'packageinfo.json' file, which is a parameter representation of the package.

The packageinfo.json contains the following parameters:

>   **"PackageName"**    : "xxx"
>   **"PackageVersion"** : "1.0.0"
>   **"PackageEntry"**   : "packagename.py"
>   **"PackageLang"**    : "python" for python2&python3,  "python2", or "python3"
>   **"PackageInfo**     : "xxxx"

**usage : python pchain/tools/pcpack.py packagefolder**

or

```python
from pchain.tools import pcpack
pcpack.do('packagefolder')
```

#### c. pcpackinstall.py

install local package

**usage : python pchain/tools/pcpackinstall.py xxx-python.1.0.0.zip**

or

```python
from pchain.tools import pcpackinstall
pcpackinstall.do('xxx-python.1.0.0.zip')
```

#### d. pcmanager.py

create new project or new package

**usage : python pchain/tools/pcmanager.py --project | --raw_project  projectname**
**or      python pchain/tools/pcmanager.py --package | --raw_package packagename**

or

```python
from pchain.tools import pcmanager
pcmanager.do('--project',projectname)  or
pcmanager.do('--package',packagename)
```

