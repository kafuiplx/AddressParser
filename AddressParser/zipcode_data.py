__author__ = 'kafuinutakor'
import os


class ZipcodeData(object):

    def __init__(self):

        directory = os.getcwd()

        with open(directory + '/meta_data/zip_lite_all.txt', 'r+') as infile:

            data = [i.split('\t') for i in infile.read().splitlines()]

        self.zipcode_data = {}

        for item in data:

            self.zipcode_data[item[0]] = item





