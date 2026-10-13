import unittest
from core.interpreter import CommandInterpreter


class TestUnixEmulator(unittest.TestCase):
    """Тестирование REPL и команд-заглушек для Этапа 1."""

    def setUp(self):
        """Инициализация интерпретатора."""
        self.interpreter = CommandInterpreter()

    def test_ls_stub(self):
        """Тест работы заглушки ls."""
        res, _, _ = self.interpreter.execute("ls -la /home")
        self.assertEqual(res, "ls -la /home")

    def test_cd_stub(self):
        """Тест работы заглушки cd."""
        res, _, _ = self.interpreter.execute("cd /var/log")
        self.assertEqual(res, "cd /var/log")

    def test_exit_command(self):
        """Тест завершения работы по команде exit."""
        res, should_exit, _ = self.interpreter.execute("exit")
        self.assertEqual(res, "Goodbye!")
        self.assertTrue(should_exit)


if __name__ == "__main__":
    unittest.main()
