import unittest
from core.interpreter import CommandInterpreter
from core.vfs import VirtualFileSystem


class TestUnixEmulator(unittest.TestCase):
    """Тестирование VFS и базовых команд для Этапа 3."""

    def setUp(self):
        """Инициализация изолированной ФС перед каждым тестом."""
        self.vfs = VirtualFileSystem()
        self.vfs._add_path("/home/user", "dir", "")
        self.vfs._add_path("/home/user/readme.txt", "file", "SGVsbG8=", 15)
        self.interpreter = CommandInterpreter(self.vfs)

    def test_cd_command(self):
        """Тест перемещения по папкам cd."""
        self.interpreter.execute("cd home/user")
        self.assertEqual(self.vfs.current_node.name, "user")

    def test_ls_command(self):
        """Тест вывода содержимого каталога ls."""
        self.interpreter.execute("cd home")
        res, _, _ = self.interpreter.execute("ls")
        self.assertEqual(res, "user")

    def test_vfs_recursive_size(self):
        """Тест рекурсивного подсчета веса каталогов."""
        user_node = self.vfs.resolve_path("home/user")
        calculated_size = self.vfs.calculate_node_size(user_node)
        self.assertEqual(calculated_size, 15)


if __name__ == "__main__":
    unittest.main()
