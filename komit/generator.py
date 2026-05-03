from komit.config import Config
from ollama import Client
STYLES ={
    "conventional":(),
    "simple":(),
    "detailed":()
}

def generate_message(diff:str,config:Config|None=None):
    config = config or Config()