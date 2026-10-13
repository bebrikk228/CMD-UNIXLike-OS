import base64
import csv
import os


class VFSNode:
    """Узел виртуальной файловой системы с поддержкой размера."""

    def __init__(
        self, name: str, is_dir: bool = True, content: str = "", size: int = 0
    ):
        """Инициализация элемента ФС."""
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.base_size = size
        self.owner = "root"
        self.children = {}
        self.parent = None


class VirtualFileSystem:
    """Управление виртуальной файловой системой в памяти."""

    def __init__(self):
        """Создание корневого каталога UNIX ФС."""
        self.root = VFSNode("/", is_dir=True)
        self.current_node = self.root

    def load_from_csv(self, csv_path: str) -> str:
        """Загрузка структуры файловой системы из CSV файла."""
        if not csv_path or not os.path.exists(csv_path):
            return "VFS Error: Файл VFS не найден."

        try:
            with open(csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sz = int(row["size"]) if row.get("size") else 0
                    self._add_path(row["path"], row["type"], row["content"], sz)
            return "VFS успешно загружена в память."
        except Exception as e:
            return f"VFS Load Error: ({str(e)})"

    def _add_path(
        self, vfs_path: str, node_type: str, b64_content: str, size: int = 0
    ):
        """Парсинг путей и построение дерева объектов в памяти."""
        if vfs_path == "/":
            return

        parts = [p for p in vfs_path.split("/") if p]
        current = self.root

        for i, part in enumerate(parts):
            is_last = i == len(parts) - 1
            if part not in current.children:
                if is_last and node_type == "file":
                    decoded = base64.b64decode(b64_content).decode("utf-8")
                    new_node = VFSNode(
                        part, is_dir=False, content=decoded, size=size
                    )
                else:
                    new_node = VFSNode(part, is_dir=True)

                new_node.parent = current
                current.children[part] = new_node
            current = current.children[part]

    def resolve_path(self, path_str: str) -> VFSNode | None:
        """Находит узел VFS по абсолютному или относительному пути."""
        if not path_str:
            return self.current_node

        current = self.root if path_str.startswith("/") else self.current_node
        parts = [p for p in path_str.split("/") if p]

        for part in parts:
            if part == ".":
                continue
            if part == "..":
                if current.parent:
                    current = current.parent
            elif part in current.children:
                current = current.children[part]
            else:
                return None

        return current

    def calculate_node_size(self, node: VFSNode) -> int:
        """Рекурсивный подсчет суммарного веса папки и ее содержимого."""
        if not node.is_dir:
            return node.base_size

        total = 0
        for child in node.children.values():
            total += self.calculate_node_size(child)
        return total

    def get_pwd(self) -> str:
        """Построение текущего абсолютного пути."""
        if self.current_node == self.root:
            return "/"

        path_parts = []
        current = self.current_node
        while current and current != self.root:
            path_parts.append(current.name)
            current = current.parent

        return "/" + "/".join(reversed(path_parts))
