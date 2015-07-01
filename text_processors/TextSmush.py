__author__ = 'kafuinutakor'
import string

def TextSmush(text):

    text_working = list(text)

    for character in xrange(0, len(text_working)):

        if character != 0:

            if text_working[character].isdigit():

                if text_working[character - 1].isalpha():

                    text_working[character] = " " + text_working[character]

                else:

                    pass

            else:

                pass

    return "".join(text_working)
