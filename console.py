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
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from models.engine.file_storage import FileStorage
import shlex


class HBNBCommand(cmd.Cmd):
    """
    This class defines a command interpreter and defines methods that guide
    actions in response to user interactions
    """

    prompt = '(hbtn) '

    def do_EOF(self, line):
        """Handles the end-of-file marker"""
        return True

    def do_quit(self, q):
        """Exits the command interpreter"""
        return True

    def emptyline(self):
        """
        Do nothing!
        """
        pass

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
            elif models.storage.all().get(obj_key):
                print(models.storage.all().get(obj_key))
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
            if (class_name not in globals() or
                    type(globals()[class_name]) is not type):
                print("** class doesn't exist **")
            elif obj_key not in models.storage.all():
                print("** no instance found **")
            else:
                del models.storage.all()[obj_key]
                models.storage.save()

    def do_all(self, class_name):
        """
        Prints all string representation of all instances based or not on the
        class name
        """
        objs_list = []
        all_objs = models.storage.all()
        if not class_name:
            for key in all_objs.keys():
                obj = all_objs[key]
                objs_list.append(str(obj))
            print(objs_list)
        elif class_name in globals() and type(globals()[class_name]) is type:
            for key in all_objs.keys():
                obj_class, obj_id = key.split('.')
                if obj_class == class_name:
                    obj = all_objs[key]
                    objs_list.append(str(obj))
            print(objs_list)

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
            all_objs = models.storage.all()

            if (class_nm not in globals() or
                    type(globals()[class_nm]) is not type):
                print("** class doesn't exist **")
            elif not models.storage.all().get(obj_key):
                print("** no instance found **")
            else:
                if '{' in class_info:
                    i = class_info.index('{')
                    update = class_info[i:]
                    update = eval(update)
                    for key, obj in all_objs.items():
                        if key == obj_key:
                            for key, val in update.items():
                                setattr(obj, key, val)
                        obj.save()
                else:
                    for key, obj in all_objs.items():
                        if key == obj_key:
                            setattr(obj, attr_nm, attr_val)
                        obj.save()

    def precmd(self, argument):
        """ executed just before the command line line is interpreted """
        args = argument.split('.', 1)
        if len(args) == 2:
            _class = args[0]
            args = args[1].split('(', 1)
            command = args[0]
            if ',' in args[1] and args[1].strip() and '{' not in args[1]:
                args = args[1].split(')', 1)
                if len(args) == 2:
                    _id = args[0].split(',', 1)
                    if (len(_id) == 2):
                        other_args = _id[1]
                        other_args = other_args.replace(',', '')
                        line = f"{command} {_class} {_id[0]} {other_args}"
                        line = line.replace('"', '')
                        return line
            else:
                args[1] = args[1].split(')')
                if ',' in args[1][0]:
                    args = args[1][0].split(',', 1)
                    _id = args[0].replace('"', '')
                    other_args = eval(args[1])
                    return f"{command} {_class} {_id} {other_args}"
                else:
                    _id = args[1][0].replace('"', '')
                    return f"{command} {_class} {_id}"
        else:
            return argument

    def do_count(self, class_name):
        """
        counts number of objects for a given class
        """
        obj_list = models.storage.all()
        count = 0
        for key, value in obj_list.items():
            cls_name = key.split('.')[0]
            if cls_name == class_name:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
