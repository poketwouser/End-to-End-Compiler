import sys

class Parser:
    def __init__(self, filepath):
        self.commands = []
        with open(filepath, 'r') as f:
            for line in f:
                # remove comments and whitespace
                line = line.split('//')[0].strip()
                if line:
                    self.commands.append(line)
        self.current_index = -1
        self.current_command = ""

    def has_more_commands(self):
        return self.current_index + 1 < len(self.commands)

    def advance(self):
        if self.has_more_commands():
            self.current_index += 1
            self.current_command = self.commands[self.current_index]

    def command_type(self):
        if self.current_command.startswith('@'):
            return 'A_COMMAND'
        elif self.current_command.startswith('(') and self.current_command.endswith(')'):
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'

    def symbol(self):
        if self.command_type() == 'A_COMMAND':
            return self.current_command[1:]
        elif self.command_type() == 'L_COMMAND':
            return self.current_command[1:-1]
        return ""

    def dest(self):
        if '=' in self.current_command:
            return self.current_command.split('=')[0]
        return "null"

    def comp(self):
        comp_str = self.current_command
        if '=' in comp_str:
            comp_str = comp_str.split('=')[1]
        if ';' in comp_str:
            comp_str = comp_str.split(';')[0]
        return comp_str

    def jump(self):
        if ';' in self.current_command:
            return self.current_command.split(';')[1]
        return "null"
