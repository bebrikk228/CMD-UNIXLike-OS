import os
import shlex


class CommandInterpreter:
    """Парсер и исполнитель базовых команд UNIX для VFS."""

    def __init__(self, vfs):
        """Инициализация интерпретатора с подключенной VFS."""
        self.vfs = vfs

    def expand_env_vars(self, text: str) -> str:
        """Раскрытие переменных окружения ОС."""
        return os.path.expandvars(text)

    def execute(self, command_line: str) -> tuple[str, bool, bool]:
        """Парсинг командной строки, флагов и аргументов."""
        clean_line = self.expand_env_vars(command_line.strip())
        if not clean_line or clean_line.startswith("#"):
            return "", False, False

        try:
            parts = shlex.split(clean_line)
        except ValueError as e:
            return f"bash: parse error: {e}", False, False

        if not parts:
            return "", False, False

        cmd_name = parts[0]
        remaining = parts[1:]

        flags = [a for a in remaining if a.startswith("-") and len(a) > 1]
        args = [a for a in remaining if not a.startswith("-") or a == "-"]

        if flags and cmd_name in {"cd", "pwd", "clear", "exit", "echo"}:
            flag_name = flags[0][1:]
            return (
                f"bash: {cmd_name}: invalid option -- '{flag_name}'",
                False,
                False,
            )

        if cmd_name == "exit":
            return "Goodbye!", True, False
        if cmd_name == "clear":
            return "", False, True
        if cmd_name == "ls":
            return self._cmd_ls(flags, args), False, False
        if cmd_name == "cd":
            return self._cmd_cd(args), False, False
        if cmd_name == "pwd":
            return self.vfs.get_pwd(), False, False
        if cmd_name == "echo":
            return " ".join(remaining), False, False

        return f"bash: {cmd_name}: command not found", False, False

    def _parse_ls_flags(
        self, flags_list: list[str]
    ) -> tuple[bool, bool, bool, str | None]:
        """Парсит флаги ls. Возвращает (has_l, has_a, has_h, invalid_flag)."""
        has_l, has_a, has_h = False, False, False
        valid_flags = {"l", "a", "h"}

        for flag in flags_list:
            for char in flag[1:]:
                if char not in valid_flags:
                    return False, False, False, char
                if char == "l":
                    has_l = True
                elif char == "a":
                    has_a = True
                elif char == "h":
                    has_h = True
        return has_l, has_a, has_h, None

    def _cmd_ls(self, flags: list[str], args: list[str]) -> str:
        """Реализация команды ls с поддержкой флагов и путей VFS."""
        has_l, has_a, has_h, invalid_char = self._parse_ls_flags(flags)
        if invalid_char:
            return f"ls: invalid option -- '{invalid_char}'"

        target_path = args[0] if args else ""
        target_node = self.vfs.resolve_path(target_path)

        if not target_node:
            return (
                f"ls: cannot access '{target_path}': No such file or directory"
            )
        if not target_node.is_dir:
            return target_node.name

        items = []
        if has_a:
            dot_sz = self.vfs.calculate_node_size(target_node)
            p_node = (
                target_node.parent if target_node.parent else target_node
            )
            dotdot_sz = self.vfs.calculate_node_size(p_node)
            items.extend(
                [(".", True, "root", dot_sz), ("..", True, "root", dotdot_sz)]
            )

        for name, node in target_node.children.items():
            sz = self.vfs.calculate_node_size(node)
            items.append((name, node.is_dir, node.owner, sz))

        if not items:
            return ""
        if has_l:
            return self._format_ls_long(items, has_h)
        return "  ".join([item[0] for item in items])

    def _format_ls_long(self, items: list[tuple], has_h: bool) -> str:
        """Форматирует вывод ls -l."""
        lines = []
        for name, is_dir, owner, raw_size in items:
            pfx = "drwxr-xr-x" if is_dir else "-rw-r--r--"
            if has_h:
                if raw_size >= 1048576:
                    sz = f"{raw_size / 1048576:.1f}M"
                elif raw_size >= 1024:
                    sz = f"{raw_size / 1024:.1f}K"
                else:
                    sz = f"{raw_size}B"
            else:
                sz = str(raw_size)

            lines.append(f"{pfx}  {owner}  {sz}  {name}")
        return "\n".join(lines)

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
