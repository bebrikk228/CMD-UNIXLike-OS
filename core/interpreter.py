import os


class CommandInterpreter:
    """Парсер и исполнитель команд UNIX для VFS."""

    def __init__(self, vfs):
        """Инициализация интерпретатора с подключенной VFS."""
        self.vfs = vfs

    def expand_env_vars(self, text: str) -> str:
        """Раскрытие переменных окружения ОС."""
        return os.path.expandvars(text)

    def execute(self, command_line: str) -> tuple[str, bool]:
        """Парсинг, исправление типов и маршрутизация команд."""
        clean_line = self.expand_env_vars(command_line.strip())
        if not clean_line or clean_line.startswith("#"):
            return "", False

        parts = clean_line.split()
        cmd_name = parts[0]
        args = parts[1:]

        if cmd_name == "exit":
            return "Goodbye!", True
        elif cmd_name == "ls":
            return self._cmd_ls(), False
        elif cmd_name == "cd":
            return self._cmd_cd(args), False
        elif cmd_name == "pwd":
            return self.vfs.get_pwd(), False
        elif cmd_name == "echo":
            return " ".join(args), False
        elif cmd_name == "mv":
            return self._cmd_mv(args), False
        elif cmd_name == "chown":
            return self._cmd_chown(args), False

        return f"bash: {cmd_name}: command not found", False

    def _cmd_ls(self) -> str:
        """Реальная логика команды ls."""
        current = self.vfs.current_node
        if not current.children:
            return ""
        return "  ".join(current.children.keys())

    def _cmd_cd(self, args: list[str]) -> str:
        """Реальная логика команды cd."""
        if not args:
            self.vfs.current_node = self.vfs.root
            return ""

        target = args[0]
        current = self.vfs.current_node

        if target == "/":
            self.vfs.current_node = self.vfs.root
            return ""
        elif target == "..":
            if current.parent:
                self.vfs.current_node = current.parent
            return ""

        if target in current.children:
            node = current.children[target]
            if node.is_dir:
                self.vfs.current_node = node
                return ""
            return f"bash: cd: {target}: Not a directory"
        
        return f"bash: cd: {target}: No such file or directory"

    def _cmd_mv(self, args: list[str]) -> str:
        """Логика команды mv (перемещение или переименование в памяти)."""
        if len(args) < 2:
            return "mv: missing file operand"

        src, dest = args[0], args[1]
        current = self.vfs.current_node

        if src not in current.children:
            return f"mv: cannot stat '{src}': No such file or directory"

        # Переименование или перемещение внутри текущей папки
        node = current.children.pop(src)
        node.name = dest
        current.children[dest] = node
        return f"Moved/Renamed '{src}' to '{dest}'"

    def _cmd_chown(self, args: list[str]) -> str:
        """Логика команды chown (смена владельца файла/папки в памяти)."""
        if len(args) < 2:
            return "chown: missing operand"

        new_owner, target = args[0], args[1]
        current = self.vfs.current_node

        if target not in current.children:
            return f"chown: cannot access '{target}': No such file"

        node = current.children[target]
        old_owner = node.owner
        node.owner = new_owner
        return f"Changed owner of '{target}' from '{old_owner}' to '{new_owner}'"
