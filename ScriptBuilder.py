from enum import Enum
from typing import List
from Command import Command


class ScriptBuilder:
    def __init__(self):
        self.commands: List[Command] = []
    
    def __getattr__(self, name):
        # Обрабатываем команды как атрибуты, а не как методы
        if name.upper() in Command.__members__:
            self.commands.append(Command[name.upper()])
            return self
        raise AttributeError(f"Команда {name} не найдена")
    
    def repeat(self, times: int = 1):
        # Добавляем команды REPEAT для повторения предыдущего действия
        for _ in range(times):
            self.commands.append(Command.REPEAT)
        return self
    
    def build(self) -> bytes:
        """Возвращает байтовое представление всех команд"""
        return b''.join([cmd.value for cmd in self.commands])

script = ScriptBuilder()

script.move_top.move_left.dig.repeat(3).move_right.stop
commands = script.build()


print(commands)