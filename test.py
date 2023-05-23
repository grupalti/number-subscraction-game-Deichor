import unittest
from unittest.mock import patch
from io import StringIO
from game import Game, HumanPlayer, ComputerPlayer, GameStatus


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.status.current_number = 10

    def test_human_player_move(self):
        with patch('builtins.input', return_value='1'):
            move = self.game.players[0].make_move(self.game.status.get_current_number())
            self.assertEqual(move, 1)

    def test_computer_player_move(self):
        move = self.game.players[1].make_move(self.game.status.get_current_number())
        self.assertIn(move, [1, 2])

    def test_game_status_update(self):
        self.game.status.update_current_number(3)
        self.assertEqual(self.game.status.current_number, 7)

    def test_game_status_game_over(self):
        self.assertFalse(self.game.status.is_game_over())
        self.game.status.update_current_number(10)
        self.assertTrue(self.game.status.is_game_over())

    def test_game_status_toggle_player_turn(self):
        self.assertTrue(self.game.status.is_player_turn)
        self.game.status.toggle_player_turn()
        self.assertFalse(self.game.status.is_player_turn)

    @patch('sys.stdout', new_callable=StringIO)
    def test_game_play(self, mock_stdout):
        with patch('builtins.input', side_effect=['1', '1', '2', '1', '1']):
            self.game.play()
            expected_output = "Current number: 10\nCurrent number: 9\nCurrent number: 8\nCurrent number: 6\nCurrent number: 5\nCurrent number: 3\nCurrent number: 2\nCurrent number: 0\nCongratulations, Player! You won!\n"
            self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()