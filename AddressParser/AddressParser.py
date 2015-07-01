__author__ = 'kafuinutakor'
from zipcode_data import ZipcodeData
import string
from text_processors.TextSmush import TextSmush
import re


class AddressParser(object):

    def __init__(self):

        # zip code meta data for U.S. records
        self.ZipcodeData = ZipcodeData().zipcode_data


    def Parse(self, address_in):

        # add character processing to un-smush stuff
        address = TextSmush(address_in)

        #filer out punctuation here
        #also replace puncs with sapce before filtering
        address_num = address

        for i in string.punctuation:

            address_num = address_num.replace(i, " " + i + " ")


        #address token scheme will be computed twice to address different needs
        address_working_num = [str(filter(lambda x: x not in string.punctuation, i)) for i in " ".join(address_num.split()).split(" ")]

        numbers = filter(lambda x: x.isdigit(), address_working_num)

        try:

            #grab longest sequence for non zero begins

            """
            non zero begins also create logic for hyphenated zips
            cannot be first number in address string
            """

            if len(numbers) > 1:

                if address_working_num.index(max(numbers[1:], key=len)) != 0:

                    zipcode = max(numbers[1:], key=len)

                else:

                    zipcode = ""

            elif address_working_num.index(max(numbers, key=len)) != 0:

                zipcode = max(numbers, key=len)

            data = [i for i in self.ZipcodeData[zipcode]]

            #add street number parsing; iteratively
            # recompute address token stream

            address_name = address

            for i in string.punctuation:

            #special handling for hyphens

                if i != "-":

                    address_name = address_name.replace(i, " " + i + " ")

                else:

                    pass

            address_working_name = [str(filter(lambda x: x not in string.punctuation or x == "-", i)) for i in " ".join(address_name.split()).split(" ")]

            if str(numbers[0]) != zipcode:

                #overwrite array with string
                street_num = str(numbers[0])

            #check for street numbers with characters in them
            ### CHECK FOR THIS

            elif type(re.match("([0-9]+[A-Za-z]+)|([A-Za-z]+[0-9]+)", address_working_name[0])) is not type(None):

                street_num = address_working_name[0]

            #check for hyphens here

            elif "-" in address_working_name[0]:

                street_num = address_working_name[0]

            else:

                street_num = ""

            # add street name
            if street_num != "":
                try:
                    # from street name until city
                    if data[1].lower() in address_name.lower():

                        #add in regex position tracker to
                        #search for multiple occurences of city in the string
                        city_matches = [i.span() for i in re.finditer(data[1].lower(), address_name.lower())]

                        if len(city_matches) == 1:

                            #if the city appears only once in the address string then use the index position of city
                            street_name = "".join(

                                address_name[address_name.index(street_num) + len(street_num):address_name.lower().index(data[1].lower())]

                            ).replace(",", "").strip()

                        elif len(city_matches) > 1:

                            # if the city occurs more than once in the address string then..
                            street_name = "".join(

                                address_name[address_name.lower().index(street_num) + len(street_num):city_matches[len(city_matches) - 1][0]]

                            ).replace(",", "").strip()

                    # until state code; state code can occur multiple times in the address string
                    elif data[2] in address_working_name:

                        if address_working_name.count(data[2]) == 1:

                            street_name = " ".join(

                                address_working_name[address_working_name.index(street_num) + 1:address_working_name.index(data[2])]
                            )

                        else:

                            #remove first occurrence
                            address_working_name.remove(data[2])

                            street_name = " ".join(

                                address_working_name[address_working_name.index(street_num) + 1:address_working_name.index(data[2])]
                            )


                    else:

                        # until zipcode; note you need to use the numerically optimized parsed address
                        street_name = " ".join(

                            address_working_num[address_working_num.index(street_num) + 1:address_working_num.index(zipcode)]

                        )

                    #street name post process

                    street_name = street_name.replace(zipcode, "").strip()

                except:

                    street_name = ""

            else:

                street_name = ""

        except Exception, e:

            #print str(e)

            data = ["", "", "", "", ""]
            street_num = ""
            street_name = ""

        #post process street name; also check to see if the first item in its token stream is a number

        street_name = street_name.split(",")[0].strip()
        street_name = " ".join(street_name.split())

        street_name_working = street_name.split(" ")

        if street_name_working[0].isdigit():

            street_num = street_name_working[0]
            street_name = street_name.replace(street_num, "")

        else:

            pass

        data.extend([street_num, street_name])

        return data

