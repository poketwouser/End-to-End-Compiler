import sys
import os

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


def compile_file(jack_path, out_dir):
    basename = os.path.splitext(os.path.basename(jack_path))[0]
    tokenizer = JackTokenizer(jack_path)
    tokens = tokenizer.tokenize(out_dir=out_dir)

    engine = CompilationEngine(tokens, basename, out_dir=out_dir)
    engine.compile_class()


def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    input_path = sys.argv[1].rstrip('/\\')
    
    if os.path.isdir(input_path):
        out_dir = os.path.join(os.path.dirname(input_path), 'out')
        os.makedirs(out_dir, exist_ok=True)
        
        jack_files = [f for f in os.listdir(input_path) if f.endswith('.jack')]
        if not jack_files:
            sys.exit(1)
        
        for jack_file in sorted(jack_files):
            jack_path = os.path.join(input_path, jack_file)
            compile_file(jack_path, out_dir)
            
    elif os.path.isfile(input_path):
        src_dir = os.path.dirname(os.path.abspath(input_path))
        out_dir = os.path.join(os.path.dirname(src_dir), 'out')
        os.makedirs(out_dir, exist_ok=True)
        
        basename = os.path.basename(input_path)
        compile_file(input_path, out_dir)
    
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
