#!/usr/bin/python3
"""
test_console.py

This module contains the TestConsole class, a subclass of the standard
library's unittest.TestCase class. The module defines methods that test
the functionality of the command interpreter defined in HBNBCommand class
"""

HBNBCommand = __import__('console').HBNBCommand
from io import StringIO
import json
import os
import unittest
from unittest.mock import patch


class TestConsole(unittest.TestCase):
    """
    Defines methods that carry out tests on the command interpreter
    defined in the HBNBCommand class
    """

    def tearDown(self):
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass
    def test_create_basemodel(self):
        """Tests create command with BaseModel as argument"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
        uuid = f.getvalue()[:-1]
        self.assertEqual(len(uuid), 36)

    def test_show_basemodel(self):
        """Tests show command with BaseModel object id"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
        uuid = f.getvalue()[:-1]

        with patch('sys.stdout', new=StringIO()) as f1:
            HBNBCommand().onecmd(f"show BaseModel {uuid}")
        self.assertIn(uuid, f1.getvalue())

    def test_destroy_basemodel(self):
        """Tests destroy command with BaseModle object id"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
        uuid = f.getvalue()[:-1]
        self.assertEqual(len(uuid), 36)

        with patch('sys.stdout', new=StringIO()) as f1:
            HBNBCommand().onecmd(f"destroy BaseModel {uuid}")
        self.assertNotIn(uuid, f1.getvalue())

    def test_all_basemodel(self):
        """Tests all command with BaseModel objects"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
        basemodel_id = f.getvalue()[:-1]

        with patch('sys.stdout', new=StringIO()) as f1:
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create Place")

        with patch('sys.stdout', new=StringIO()) as f2:
            HBNBCommand().onecmd("create User")
        user_id = f2.getvalue()[:-1]

        with patch('sys.stdout', new=StringIO()) as f3:
            HBNBCommand().onecmd("all BaseModel")
        temp = json.loads(f3.getvalue()[:-1])
        self.assertIn(basemodel_id, f3.getvalue())
        self.assertNotIn(user_id, f3.getvalue())
        self.assertEqual(len(temp), 3)

    def test_update_basemodel(self):
        """Tests update command with BaseModel object"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
        model_id = f.getvalue()[:-1]
        with patch('sys.stdout', new=StringIO()) as f1:
            HBNBCommand().onecmd(f'update BaseModel {model_id} name "Joe"')
            HBNBCommand().onecmd(f"show BaseModel {model_id}")
        self.assertIn("'name': 'Joe'", f1.getvalue())


if __name__ == '__main__':
    unittest.main()
