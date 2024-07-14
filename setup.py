# coding=utf-8
"""
Installe les packages nécessaires pour l'application dans le répertoire libs.
"""
import os

def mychdir(path):
    pass

def main():
    local_dir = os.path.dirname(__file__)
    venv_dir = os.path.join(local_dir, '.venv')
    python_path = '"' + os.path.join(venv_dir, 'Scripts', 'python.exe') + '"' if os.path.exists(venv_dir) else "python" # py -3
    if local_dir:
        chdir = os.chdir
    else:
        chdir = mychdir
    original_wd = os.getcwd()
    try:
        chdir(local_dir)    # pushd
        command = (
            f'{python_path} -m pip ' +
            'install -r requirements.txt ' +
            '--upgrade --force-reinstall --no-cache-dir'
        )
        # Werkzeug==2.3.6 MAIS Version actuelle = 2.0.3
        print(f"Executing {command}")
        os.system(command)
        print("----- Successfully installed the required packages.")
    finally:
        print("----- Exiting the script.")
        chdir(original_wd)  # popd

if (__name__ == "__main__"):
    main()