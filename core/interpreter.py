

class CommandInterpreter:
    """Парсер команд, переменных окружения и выполнения скриптов."""

    def __init__(self):
        """Инициализация поддерживаемых команд."""
        self.supported_cmds = {"ls", "cd", "exit"}

    def expand_env_vars(self, text: str) -> str:
        """Раскрытие переменных окружения ОС."""
        return os.path.expandvars(text)

    def execute(self, command_line: str) -> tuple[str, bool]:
        """Парсинг и выполнение одной строки команды UNIX."""
        clean_line = self.expand_env_vars(command_line.strip())
        
        if not clean_line or clean_line.startswith("#"):
            return "", False

        parts = clean_line.split()
        # ИСПРАВЛЕНИЕ: берем только саму команду (первое слово)
        cmd_name = parts[0]
        args = parts[1:]

        if cmd_name == "exit":
            return "Goodbye!", True

        if cmd_name in self.supported_cmds:
            return f"Stub execution: {cmd_name} with args: {args}", False

        return f"bash: {cmd_name}: command not found", False
