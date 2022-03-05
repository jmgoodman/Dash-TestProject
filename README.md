# Dash-TestProject
 Avocado prices over time. From: https://realpython.com/python-dash/

## What is your dev environment?
I used:
* VS Code
* Windows 10
* Anaconda

## How to set up dev environment?
* install and boot up vs code with ADMIN PRIVELEGES
* Install the top 3 Python extensions for VS Code 
    * ctrl+shift+x -> type "python" in search bar
    * install: 
        * "Python" from Microsoft
        * "Python for VSCode" from Thomas Haakon Townsend
        * "Python Extension Pack" from Don Jayamanne)
* Install Anaconda & boot up Anaconda Navigator
* Create a new environment and install packages
    * Left panel: "Environments"
    * Bottom of panel with "search environments" at top: "Create"
    * Name it whatever you please
    * You may need to open an Anaconda prompt (Windows search bar "Anaconda Prompt") and enter `conda init` and `conda activate [env-name]`
    * Top of panel just to the right: change dropdown to "Not Installed", then search for packages:
        * Dash
        * Pandas
    * Select them and download any dependencies to your environment
* Back in VS Code, set your python interpreter
    * Ctrl+Shift+P, "Python: Select Interpreter"
    * choose your conda environment you just created, it should simply show it to you in a dropdown list, if not I apologize for the frustration :(
* Before running any Python, test VS Code's Powershell terminal
    * Ctrl+Shift+\`
    * `conda --version` in the terminal that should pop up on the bottom of the window
    * if not showing up, you'll need to add conda to your system path. I think `conda init` should do this, but manually adding it via the following should also work:
        * Windows 10 searchbar: "Edit the system environment variables"
        * "Environment Variables"
        * Select "Path", then click "Edit"
        * Open an Anaconda prompt and request `where conda`
        * take the path with `conda.exe` in it, copy everything up to `conda.exe`, and put that in as your new entry to the system path
        * click on as many OKs as you need
    * you may also need to run `Set-ExecutionPolicy -ExecutionPolicy Unrestricted`
        * BEFORE DOING SO: check permissions with `Get-ExecutionPolicy`. This should return `Unrestricted` if all is good to go.
* Run `app.py` by navigating to the script in VS code, clicking the ol' play button, and pray the terminal doesn't throw any errors. All the steps listed above should get you around any errors I ran into when setting up the environment.
* If anything goes screwy at any stage, never forget the golden rule of debugging: turn it off and on again. Restart VS Code, reinstall packages / software, reboot machines when all else fails.

## Actually...
* ditch anaconda
* follow the steps in the tutorial when it comes to setting up your preferred environment (& hence, interpreter)
* you will need the venv folder in the end to deploy to heroku
* and it's actually way easier than clunky ol' anaconda & lets you use good ol' pip install

## TODO
* Finish tutorial, especially the stuff about pretty styling
* Figure out deployment solution (Google Cloud + Kubernetes? Might be overkill... tutorial suggests Heroku, something the [plotly website](https://dash.plotly.com/deployment) corroborates)
* Add data of my choosing (maybe yet another covid dashboard? figure out how to query the [github jhu CSSE repository](https://github.com/CSSEGISandData/COVID-19) or some API with the data you want)
* Maybe even convert those data to a filesystem for SQL queries via php or smth
* go through [this](https://deeplearning.neuromatch.io/tutorials/W2D5_GenerativeModels/student/W2D5_Tutorial4.html?highlight=deploy) other tutorial to *really* grok what's going on (a lot of similar things going on, except it uses Flask directly, covers some complications if one uses notebooks & colab for development & testing, mentions [ngrok](https://ngrok.com/) as a solution to those problems, and it at least mentions django)
* speaking of django, try this tutorial: https://docs.djangoproject.com/en/4.0/intro/tutorial01/

## NOTE
heroku only accepts very specific versions of python: https://devcenter.heroku.com/articles/python-support
if you don't use one of these, heroku will not deploy your app.