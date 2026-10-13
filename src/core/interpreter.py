import os


class CommandInterpreter:
    """Интерпретатор-заглушка для Этапа 2."""

    def __init__(self):
        """Инициализация без VFS."""
        pass

    def expand_env_vars(self, text: str) -> str:
        """Раскрытие переменных окружения ОС."""
        return os.path.expandvars(text)

    def execute(self, command_line: str) -> tuple[str, bool, bool]:
        """Обработка команд-заглушек."""
        clean_line = self.expand_env_vars(command_line.strip())
        if not clean_line or clean_line.startswith("#"):
            return "", False, False

        parts = clean_line.split()
        if not parts:
            return "", False, False

        cmd_name = parts[0]
        args = parts[1:]

        if cmd_name == "exit":
            return "Goodbye!", True, False
        if cmd_name in {"ls", "cd"}:
            return f"{cmd_name} {' '.join(args)}".strip(), False, False

        return f"bash: {cmd_name}: command not found", False, False
