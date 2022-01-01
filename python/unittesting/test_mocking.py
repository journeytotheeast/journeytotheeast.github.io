# import
import unittest
from unittest.mock import patch, Mock, MagicMock, call, DEFAULT
from base import Application
from base import get_json

# --- testing 
class testUtil(unittest.TestCase):

    @patch("builtins.open")
    def test_get_valid_json(self, mock_open):
        # arrange
        filename = "does_not_exist.json"
        mock_file = Mock()
        mock_file.read.return_value = '{"foo": "bar"}'
        mock_open.return_value = mock_file

        # action
        actual_result = get_json(filename)

        # assert
        self.assertEqual({u'foo': u'bar'}, actual_result)

    @patch("builtins.open")
    def test_get_json_ioerror(self, mock_open):
        # arrange
        filename = "does_not_exist.json"
        mock_open.side_effect = IOError

        # action
        actual_result = get_json(filename)

        # assert
        self.assertEqual('', actual_result)

    @patch("json.loads")
    @patch("builtins.open")
    def test_get_json_valueerror(self, mock_open, mock_loads):
        # arrange
        filename = "does_not_exist.json"
        mock_file = Mock()
        mock_file.read.return_value = '{"foo": "bar"}'
        mock_open.return_value = mock_file
        mock_open.side_effect = ValueError

        # action
        actual_result = get_json(filename)

        # assert
        self.assertEqual('', actual_result)


# --- testing Application ---

class testApp(unittest.TestCase):

    def setUp(self):
        self.obj = Application()

    def tearDown(self):
        pass

    @patch("base.Application.get_random_person")
    def test_new_person_v1(self, mock_get_random_person):
        # arrange
        user = {'people_seen': []}
        expected_person = 'Katie'
        mock_get_random_person.return_value = 'Katie'

        # action
        actual_person = self.obj.get_next_person(user)

        # assert
        self.assertEqual(actual_person, expected_person)


    def test_new_person_v2(self):
        # arrange
        user = {'people_seen': []}
        expected_person = 'Katie'
        self.obj.get_random_person = Mock() # or MagicMock()
        self.obj.get_random_person.return_value = 'Katie'

        # action
        actual_person = self.obj.get_next_person(user)

        # assert
        self.assertEqual(actual_person, expected_person)

    def test_new_person_v3(self):
        with patch.object(Application, "get_random_person") as mock_get_random_person:
            # arrange
            user = {'people_seen': []}  
            expected_person = 'Katie'
            mock_get_random_person.return_value = 'Katie'

            # action
            actual_person = self.obj.get_next_person(user)

            # assert
            self.assertEqual(actual_person, expected_person)

    @patch("base.Application.get_random_person")
    def test_experienced_user_v1(self, mock_get_random_person):
        # arrange
        user = {'people_seen': ['Sarah', 'Mary']}
        expected_person = 'Katie'
        mock_get_random_person.side_effect = ['Mary', 'Sarah', 'Katie']

        # action
        actual_person = self.obj.get_next_person(user)

        # assert
        self.assertEqual(actual_person, expected_person)

    
    @patch("base.let_down_gently")
    def test_person2_dislikes_person1_v1(self, mock_let_down):
        # arrange
        person1 = 'Bill'
        person2 = {
            'likes': ['Sam', 'Sung'],
            'dislikes': ['Bill']
        }

        # action
        self.obj.evaluate(person1, person2)

        # assert
        self.assertEqual(mock_let_down.call_count, 1)

    @patch("base.let_down_gently")
    def test_person2_dislikes_person1_v2(self, mock_let_down):
        # arrange
        person1 = 'Bill'
        person2 = {
            'likes': ['Sam', 'Sung'],
            'dislikes': ['Bill']
        }

        # action
        self.obj.evaluate(person1, person2)

        # assert
        mock_let_down.assert_called_once_with(person1)

    @patch("base.send_email")
    @patch("base.let_down_gently")
    @patch("base.give_it_time")
    def test_person2_dislikes_person1_v3(self, mock_give_it_time, mock_let_down, mock_send_email):
        # arrange
        person1 = 'Bill'
        person2 = {
            'likes': ['Sam', 'Sung'],
            'dislikes': ['Bill']
        }

        # action
        self.obj.evaluate(person1, person2)

        # assert
        mock_let_down.assert_called_once_with(person1)
        self.assertEqual(mock_give_it_time.call_count, 0)
        self.assertEqual(mock_send_email.call_count, 0)

    @patch("base.send_email")
    @patch("base.let_down_gently")
    @patch("base.give_it_time")
    def test_person2_likes_person1_v1(self, mock_give_it_time, mock_let_down, mock_send_email):
        # arrange
        person1 = 'Bill'
        person2 = {
            'likes': ['Bill', 'Sung'],
            'dislikes': ['Sam']
        }

        # action
        self.obj.evaluate(person1, person2)

        # assert
        first_call = mock_send_email.call_args_list[0]
        second_call = mock_send_email.call_args_list[1]
        self.assertEqual(first_call, call(person1))
        self.assertEqual(second_call, call(person2))   
