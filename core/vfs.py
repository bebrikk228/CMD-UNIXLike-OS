import base64
import csv
import os


class VFSNode:
    """Узел виртуальной файловой системы."""

    def __init__(self, name: str, is_dir: bool = True, content: str = ""):
        """Инициализация элемента ФС."""
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.owner = "root"  # Добавляем владельца по умолчанию для chown
        self.children = {}
        self.parent = None


class VirtualFileSystem:
    """Класс управления виртуальной файловой системой в памяти."""

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
                    self._add_path(row["path"], row["type"], row["content"])
            return "VFS успешно загружена в память."
        except Exception as e:
            return f"VFS Load Error: ({str(e)})"

    def _add_path(self, vfs_path: str, node_type: str, b64_content: str):
        """Парсинг путей и построение дерева объектов в памяти."""
        if vfs_path == "/":
            return

        parts = [p for p in vfs_path.split("/") if p]
        current = self.root

        for i, part in enumerate(parts):
            is_last = (i == len(parts) - 1)
            if part not in current.children:
                if is_last and node_type == "file":
                    decoded = base64.b64decode(b64_content).decode("utf-8")
                    new_node = VFSNode(part, is_dir=False, content=decoded)
                else:
                    new_node = VFSNode(part, is_dir=True)
                
                new_node.parent = current
                current.children[part] = new_node
            current = current.children[part]

    def get_pwd(self) -> str:
        """Рекурсивное построение текущего пути UNIX ФС."""
        if self.current_node == self.root:
            return "/"
        
        path_parts = []
        current = self.current_node
        while current and current != self.root:
            path_parts.append(current.name)
            current = current.parent
            
        return "/" + "/".join(reversed(path_parts))
