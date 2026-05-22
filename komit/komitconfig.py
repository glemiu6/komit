#komit/komitconfig.py
from dataclasses import dataclass
from komit.config_utils import load_config_file
@dataclass
class KomitConfig:
    model:str ='qwen2.5:7b'
    style:str ='conventional'
    max_diff_length:int = 4000
    ollama_url:str ='http://localhost:11434'
    timeout:int = 60
    include_branch_name:bool = True

    @classmethod
    def from_sources(cls,args):
        file_config=load_config_file(args.config)

        return cls(
            model=args.model or file_config.get('model',cls.model),
            style=args.style or file_config.get('style',cls.style),
            max_diff_length=args.max_diff or file_config.get('max_diff_length',cls.max_diff_length),
            ollama_url=args.ollama_url or file_config.get('ollama_url',cls.ollama_url),
            timeout=args.timeout or file_config.get('timeout',cls.timeout),
            include_branch_name=args.include_branch_name or file_config.get('include_branch_name',cls.include_branch_name)
        )