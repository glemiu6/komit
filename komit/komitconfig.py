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

        def pick(arg_val, file_key, default):
            if arg_val is not None:
                return arg_val
            return file_config.get(file_key, default)

        return cls(
            model=pick(args.model,"model",cls.model),
            style=pick(args.style,"style",cls.style),
            max_diff_length=pick(args.max_diff,"max_diff_length",cls.max_diff_length),
            ollama_url=pick(args.ollama_url,"ollama_url",cls.ollama_url),
            timeout=pick(args.timeout,"timeout",cls.timeout),
            include_branch_name=pick(args.include_branch_name,"include_branch_name",cls.include_branch_name)
        )