import os
import shutil
from random import randint


def read_file(file_path) -> str:
    with open(file_path, 'r') as file:
        return str(file.read())


def generate_random_email() -> str:
    return f"tester{randint(10, 99)}test{randint(1000, 9999)}"

def remove_file(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass


def remove_files(files):
    for file in files:
        read_file(file)

def remove_directory(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass

def remove_directories(path):
    for directory in path:
        remove_directory(directory)

def remove_report_files():
    remove_directories(['reports','results_chrome','results_firefox','results_edge','results_safari'])

remove_report_files()