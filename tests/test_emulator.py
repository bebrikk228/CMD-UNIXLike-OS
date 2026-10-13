import unittest
from core.interpreter import CommandInterpreter
from core.vfs import VirtualFileSystem


class TestUnixEmulator(unittest.TestCase):
    """Тестирование логики команд UNIX эмулятора."""

    def setUp(self):
        """Инициализация изолированной ФС перед каждым тестом."""
        self.vfs = VirtualFileSystem()
        self.vfs._add_path("/home/user", "dir", "")
        self.vfs._add_path("/home/user/readme.txt", "file", "SGVsbG8=", 15)
        self.interpreter = CommandInterpreter(self.vfs)

    def test_pwd_root(self):
        """Тест вывода корневого пути pwd."""
        res, _, _ = self.interpreter.execute("pwd")
        self.assertEqual(res, "/")

    def test_cd_and_pwd(self):
        """Тест перемещения по папкам cd и pwd."""
        self.interpreter.execute("cd home/user")
        res, _, _ = self.interpreter.execute("pwd")
        self.assertEqual(res, "/home/user")

    def test_ls_command(self):
        """Тест вывода содержимого каталога ls."""
        self.interpreter.execute("cd home")
        res, _, _ = self.interpreter.execute("ls")
        self.assertEqual(res, "user")

    def test_echo_command(self):
        """Тест команды вывода текста echo."""
        res, _, _ = self.interpreter.execute("echo Hello World")
        self.assertEqual(res, "Hello World")

    def test_mv_command(self):
        """Тест перемещения/переименования mv."""
        res_mv, _, _ = self.interpreter.execute("mv home new_home")
        self.assertIn("Moved/Renamed", res_mv)

        res_ls, _, _ = self.interpreter.execute("ls")
        ls_items = res_ls.split()

        self.assertIn("new_home", ls_items)
        self.assertNotIn("home", ls_items)

    def test_chown_command(self):
        """Тест смены владельца chown."""
        res, _, _ = self.interpreter.execute("chown admin home")
        self.assertIn("Changed owner", res)
        node = self.vfs.resolve_path("home")
        self.assertEqual(node.owner, "admin")

    def test_vfs_recursive_size(self):
        """Тест рекурсивного подсчета веса каталогов."""
        user_node = self.vfs.resolve_path("home/user")
        calculated_size = self.vfs.calculate_node_size(user_node)
        self.assertEqual(calculated_size, 15)
    
    def test_ls_invalid_option(self):
        """Тест вызова ls с некорректным флагом."""
        res, _, _ = self.interpreter.execute("ls -lx")
        self.assertIn("ls: invalid option -- 'x'", res)

if __name__ == "__main__":
    unittest.main()
