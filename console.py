#!/usr/bin/python3
"""
console.py

This module houses class HBNBCommand, a subclass of the standard library's Cmd
class. The module launches an interactive command interpreter when executed,
that can handle various commands, that are handled by methods defined in the
HBNBCommand class. The class is primarily intended to manipulate objects in a
file storage.
"""

import cmd
from datetime import datetime
import models
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import shlex


class HBNBCommand(cmd.Cmd):
    """
    This class defines a command interpreter and defines methods that guide
    actions in response to user interactions
    """

    prompt = '(hbtn) '

    def do_create(self, class_name=None):
        """
        Creates a new instance of class BaseModel, saves it (to a JSON file)
        and prints the id.
        """
        if not class_name:
            print("** class name missing **")
        elif class_name in globals() and type(globals()[class_name]) is type:
            instance = globals()[class_name]()
            instance.save()
            print(instance.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, class_info):
        """
        Prints the string representation of an instance based on the class name
        and id
        """
        if not class_info:
            print("** class name missing **")
        elif len(class_info.split()) < 2:
            print("** instance id missing **")
        else:
            class_name = class_info.split()[0]
            class_uuid = class_info.split()[1]
            obj_key = '.'.join([class_name, class_uuid])
            if (class_name not in globals() or
                    type(globals()[class_name]) is not type):
                print("** class doesn't exist **")
            elif models.storage.all.get(obj_key):
                print(models.storage.all.get(obj_key))
            else:
                print("** no instance found **")

    def do_destroy(self, class_info):
        """
        Deletes an instance based on the class name and id and saves the
        changes to the JSON file
        """
        if not class_info:
            print("** class name missing **")
        elif len(class_info.split()) < 2:
            print("** instance id missing **")
        else:
            class_name = class_info.split()[0]
            class_uuid = class_info.split()[1]
            obj_key = '.'.join([class_name, class_uuid])
            if (class_name in globals() or
                    type(globals()[class_name]) is not type):
                print("** class doesn't exist **")
            elif models.storage.all().get(obj_key):
                del models.storage.all()[obj_key]
            else:
                print("** no instance found **")

    def do_all(self, class_name):
        """
        Prints all string representation of all instances based or not on the
        class name
        """
        if not class_name:
            print(models.storage.all())
        elif class_name in globals() and type(globals()[class_name]) is type:
            objs = models.storage.all()
            print({key: val for key, val in objs.items()
                  if '__class__' in objs[key]
                  and objs[key]['__class__'] == class_name})
        else:
            print("** class doesn't exist **")

    def do_update(self, class_info):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute
        """
        if not class_info:
            print("** class name missing **")
        elif len(class_info.split()) < 2:
            print("** instance id missing **")
        elif len(class_info.split()) < 3:
            print("** attribute name missing **")
        elif len(class_info.split()) < 4:
            print("** value missing **")
        else:
            arg_list = class_info.split()
            class_nm, obj_id, attr_nm = arg_list[0], arg_list[1], arg_list[2]
            attr_val = shlex.split(arg_list[3])[0]
            obj_key = '.'.join([class_nm, obj_id])
            if (class_nm not in globals() or
                    type(globals()[class_nm]) is not type):
                print("** class doesn't exist**")
            elif not models.storage.all().get(obj_key):
                print("** no instance found **")
            else:
                attr_val = type(attr_val)(attr_val)
                instance = models.storage.all().get(obj_key)
                instance[attr_nm] = attr_val
                instance['updated_at'] = str(datetime.now())
                models.storage.save()

    def do_EOF(self, line):
        """Handles the end-of-file marker"""
        return True

    def do_quit(self, q):
        """Exits the command interpreter"""
        return True

    def emptyline(self):
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()