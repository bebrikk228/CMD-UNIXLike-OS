import unittest
from core.interpreter import CommandInterpreter


class TestUnixEmulator(unittest.TestCase):
    """Тестирование команд-заглушек и парсера для Этапа 2."""

    def setUp(self):
        """Инициализация интерпретатора."""
        self.interpreter = CommandInterpreter()

    def test_ls_stub(self):
        """Тест заглушки ls."""
        res, _, _ = self.interpreter.execute("ls -la /home")
        self.assertEqual(res, "ls -la /home")

    def test_cd_stub(self):
        """Тест заглушки cd."""
        res, _, _ = self.interpreter.execute("cd /var/log")
        self.assertEqual(res, "cd /var/log")

    def test_exit(self):
        """Тест команды exit."""
        res, should_exit, _ = self.interpreter.execute("exit")
        self.assertTrue(should_exit)


if __name__ == "__main__":
    unittest.main()
