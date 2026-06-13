import sys
import os
from parser import Parser
from code_module import Code
from symbol_table import SymbolTable

def assemble(filepath):
    # First pass: labels
    parser = Parser(filepath)
    sym_table = SymbolTable()
    rom_address = 0
    
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == 'L_COMMAND':
            sym_table.add_entry(parser.symbol(), rom_address)
        else:
            rom_address += 1

    # Second pass: variables and code generation
    parser = Parser(filepath)
    ram_address = 16
    output_lines = []
    
    while parser.has_more_commands():
        parser.advance()
        cmd_type = parser.command_type()
        
        if cmd_type == 'A_COMMAND':
            sym = parser.symbol()
            if sym.isdigit():
                address = int(sym)
            else:
                if not sym_table.contains(sym):
                    sym_table.add_entry(sym, ram_address)
                    ram_address += 1
                address = sym_table.get_address(sym)
            binary_str = format(address, '016b')
            output_lines.append(binary_str)
            
        elif cmd_type == 'C_COMMAND':
            dest_bits = Code.dest(parser.dest())
            comp_bits = Code.comp(parser.comp())
            jump_bits = Code.jump(parser.jump())
            binary_str = '111' + comp_bits + dest_bits + jump_bits
            output_lines.append(binary_str)

    output_path = os.path.splitext(filepath)[0] + '.hack'
    with open(output_path, 'w') as f:
        f.write('\n'.join(output_lines) + '\n')
    print(f"Assembly complete. Output saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <file.asm>")
        sys.exit(1)
    assemble(sys.argv[1])
