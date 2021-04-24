from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            # test that you're getting a template
            self.assertEqual(response.status_code, 200)
            self.assertIn('<table class="board">', html)
            self.assertIn('<form id="newWordForm">', html)
           

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.get("/api/new-game")
            # breakpoint()
            # get_json() method does not return json-- it converts the JSON back to whatever type it should be
            key_and_game_board = response.get_json()
            self.assertEqual(response.status_code, 200)
            # tests to make sure the games dictionary contains a key of the game_id itself
            self.assertIn(key_and_game_board['gameId'], games.keys())
            # test to make sure the gameId value in the response is a string
            self.assertIsInstance(key_and_game_board['gameId'], str)
            # test to make sure the board value in the response is a list
            self.assertIsInstance(key_and_game_board['board'], list)
            # loop of tests to make sure that each element in the board value list is also a list
            for list_in_list in key_and_game_board['board']:
                self.assertIsInstance(list_in_list, list)
            # write a test for this route
            # the route returns JSON with a string game id, and a list-of-lists for the board
            # the route stores the new game in the games dictionary


    def test_api_score_word(self):
        """Test validity of player's words"""

        with self.client as client:
            response = client.get("/api/new-game")
            key_and_game_board = response.get_json()

            test_game_id = key_and_game_board["gameId"]

            games[test_game_id].board = [
                ["O", "N", "N", "E", "O"],
                ["X", "K", "E", "S", "A"],
                ["E", "C", "M", "Z", "N"],
                ["L", "F", "X", "F", "S"],
                ["B", "T", "O", "N", "C"]
            ]

            #test if valid word is on board
            post_response = client.post('/api/score-word',
                           json={'gameId': test_game_id,
                           'word' : 'TON'
                           })
            json_response = post_response.get_json()

            self.assertEqual(post_response.status_code, 200)
            self.assertEqual("ok",json_response["result"])

            #test if word is not a valid word
            post_response = client.post('/api/score-word',
                           json={'gameId': test_game_id,
                           'word' : 'TTT'
                           })
            json_response = post_response.get_json()

            self.assertEqual(post_response.status_code, 200)
            self.assertEqual("not-word",json_response["result"])

            #test if word is not the board
            post_response = client.post('/api/score-word',
                           json={'gameId': test_game_id,
                           'word' : 'CAT'
                           })
            json_response = post_response.get_json()

            self.assertEqual(post_response.status_code, 200)
            self.assertEqual("not-on-board",json_response["result"])
