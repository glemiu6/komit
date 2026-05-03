#komit/komitconfig.py
from dataclasses import dataclass

@dataclass
class KomitConfig:
    model:str ='qwen2.5:7b'
    style:str ='conventional'
    max_diff_length:int = 4000
    ollama_url:str ='http://localhost:11434'