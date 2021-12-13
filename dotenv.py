from dotenv import load_dotenv
from pathlib import Path
from dotenv import dotenv_values

def read_env(path):
    return load_dotenv(dotenv_path=Path(path))

def read_env_values(path):
    return dotenv_values(Path(dotenv_path=path))