import unittest
from src.core.vfs import VirtualFileSystem
from src.core.interpreter import CommandInterpreter


class TestUnixEmulator(unittest.TestCase):
    """Тестирование логики команд UNIX эмулятора."""

    def setUp(self):
        """Инициализация изолированной ФС перед каждым тестом."""
        self.vfs = VirtualFileSystem()
        # Имитируем ручную загрузку структуры
        self.vfs._add_path("/home/user", "dir", "")
        self.vfs._add_path("/etc/config.cfg", "file", "Y29uZmln")
        self.interpreter = CommandInterpreter(self.vfs)

    def test_pwd_root(self):
        """Тест вывода корневого пути pwd."""
        res, _ = self.interpreter.execute("pwd")
        self.assertEqual(res, "/")

    def test_cd_and_pwd(self):
        """Тест перемещения по папкам cd и pwd."""
        self.interpreter.execute("cd home")
        res, _ = self.interpreter.execute("pwd")
        self.assertEqual(res, "/home")

    def test_ls_command(self):
        """Тест вывода содержимого каталога ls."""
        self.interpreter.execute("cd home")
        res, _ = self.interpreter.execute("ls")
        self.assertEqual(res, "user")

    def test_echo_command(self):
        """Тест команды вывода текста echo."""
        res, _ = self.interpreter.execute("echo Hello World")
        self.assertEqual(res, "Hello World")

    def test_mv_command(self):
        """Тест перемещения/переименования mv."""
        self.interpreter.execute("mv home new_home")
        res, _ = self.interpreter.execute("ls")
        self.assertIn("new_home", res)


if __name__ == "__main__":
    unittest.main()
