from app.db.number_map import number_map, number_units

class NumberToEnglishTransformer:
    """Transforms a number to its written english equivalent
    """

    @staticmethod
    def get_english_units(number:str) -> str:
        """Gets the top level units (e.g. hundreds, thousands, millions, billions, etc...

        Args:
            number (int): The number to be converted into english
        """
        units = ''
        split_num = number.split(',')
        for n in [x for x in split_num if x != split_num[0]]:
            units += n
        return number_units[len(units)]

    @staticmethod
    def preprocess_number(number:int) -> str:
        """Preprocesses the number into a standard comma formatted string (e.g. 1000 --> "1,000")

        Args:
            number (int): The number to be converted into english
        """
        return '{:,}'.format(number)

    @staticmethod
    def transform_largest_units(number:str) -> str:
        """Transforms the largest units of the number-split-on-commas (e.g. transforms the "100" in ex. "100,000,000" --> ["100","000","000"])

        Args:
            number (int): The number to be converted into english
        """
        return number_map[number.split(',')[0]] + ' ' + NumberToEnglishTransformer.get_english_units(number)

    @staticmethod
    def combine_remaining(number:str, iter_split:int) -> str:
        """Combines the remaining units in the number-split-on-commas (e.g. combines "000" and "000" in ex. "100,000,000" --> ["100","000","000"])

        Args:
            number (int): The number to be converted into english
        """
        combined_number = ''
        for n in number.split(',')[iter_split:]:
            combined_number += n
        return combined_number

    @staticmethod
    def preprocess_remaining(number:str, iter_split:int) -> str:
        """Preprocesses the remaining units in the number-split-on-commas into a standard comma formatted string (e.g. "1,234,567" --> "234,567")

        Args:
            number (int): The number to be converted into english
            iter_split (int): The current iteration while looping through the number-split-on-commas (e.g. ["100","000","000"] iterating from 0-2 because length==3)
        """
        return NumberToEnglishTransformer.preprocess_number(int(NumberToEnglishTransformer.combine_remaining(number, iter_split)))

    @staticmethod
    def transform(payload:int) -> str:
        """Preprocesses the remaining units in the number-split-on-commas into a standard comma formatted string (e.g. "1,234,567" --> "234,567")

        Args:
            payload (int): The number to be converted into english
            iter_split (int): The current iteration while looping through the number-split-on-commas (e.g. ["100","000","000"] iterating from 0-2 because length==3)
        """
        payload=int(payload.number)
        number_in_english = ''

        if payload is None or type(payload) is not int:
            raise ValueError(payload)

        formatted_number = NumberToEnglishTransformer.preprocess_number(payload)
        for iter_split in range(len(formatted_number.split(','))):
            number_in_english += NumberToEnglishTransformer.transform_largest_units(NumberToEnglishTransformer.preprocess_remaining(formatted_number, iter_split)) + ' '
        return number_in_english