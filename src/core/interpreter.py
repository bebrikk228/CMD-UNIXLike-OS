import os


class CommandInterpreter:
    """Интерпретатор команд VFS для Этапа 3."""

    def __init__(self, vfs):
        """Инициализация с подключенной VFS."""
        self.vfs = vfs

    def expand_env_vars(self, text: str) -> str:
        """Раскрытие переменных окружения ОС."""
        return os.path.expandvars(text)

    def execute(self, command_line: str) -> tuple[str, bool, bool]:
        """Выполнение базовых команд VFS без флагов."""
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
        if cmd_name == "ls":
            return self._cmd_ls(args), False, False
        if cmd_name == "cd":
            return self._cmd_cd(args), False, False

        return f"bash: {cmd_name}: command not found", False, False

    def _cmd_ls(self, args: list[str]) -> str:
        """Базовая команда ls без поддержки флагов."""
        target_path = args[0] if args else ""
        target_node = self.vfs.resolve_path(target_path)

        if not target_node:
            return (
                f"ls: cannot access '{target_path}': No such file or directory"
            )
        if not target_node.is_dir:
            return target_node.name

        if not target_node.children:
            return ""

        return "  ".join(target_node.children.keys())

    def _cmd_cd(self, args: list[str]) -> str:
        """Перемещение cd по VFS."""
        if not args:
            self.vfs.current_node = self.vfs.root
            return ""

        target_path = args[0]
        target_node = self.vfs.resolve_path(target_path)

        if not target_node:
            return f"bash: cd: {target_path}: No such file or directory"
        if not target_node.is_dir:
            return f"bash: cd: {target_path}: Not a directory"

        self.vfs.current_node = target_node
        return ""
