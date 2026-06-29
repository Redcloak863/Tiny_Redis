import re

def findcommand(string: str) -> tuple[str, str]:
    """
    Finds the command, which should be all caps at the beginning of the string.
    :param string: The input string.
    :return a tuple of two strings: The extracted command and data.
    """
    commmandPattern = re.compile(r"([A-Z]+\b)")
    dataPattern = re.compile(r"\"(.+?)\"")
    command = re.match(commmandPattern, string)  # Using match to limit our attention to the beginning of the string.
    data = re.findall(dataPattern, string)  # Using findall to now broaden our search.
    return bulkstring(command.group(0)), bulkstring()

def bulkstring(string: str) -> str:
    """
    Formats a string as $<string length>\r\n<string>\r\n
    :param string:
    :return: string
    """
    return str('$' + str(len(string)) + '\\r\\n' + string + '\\r\\n')

def bulkarray(command: str, *args: str) -> str:
    """
    Creates the bulk array that's to be returned by the ECHO command.
    :param command: The REDIS command.
    :param args: Its argument(s).
    :return: The formatted string.
    """
    array_size = 1  # This is the minimum assuming a command that takes no argument, like EXIT.
    bulk_cmd = bulkstring(command)
    bulk_args = ''
    for arg in args:
        array_size += 1
        bulk_args = bulk_args + f'{bulkstring(arg)}'
    return f'*{array_size}\\r\\n{bulk_cmd}\\{bulk_args}'

def parsebulkarray(array: str) -> list:
    """
    Parses a bulk array and returns its elements as a list.
    :param array:
    :return: The array elements in a list.
    """
    arraycontents = []
    pattern = re.compile(r"(?<=\*)\d")  # Find the # of elements in the array.
    arraylength = int(re.findall(pattern, array)[0])
    # print(arraylength)
    arrayelements = re.findall(r'\n(.*?)\r', array, re.DOTALL)
    # print(arrayelements)
    for n in range(1, len(arrayelements), 2):
        arraycontents.append(arrayelements[n])
    return arraycontents



if __name__ == '__main__':
    # print(bulkString('ECHO').encode())
    # print(bulkString('EXIT'))
    print(bulkarray('EXIT'))
    print(bulkarray('ECHO', 'Hello!'))
    print(bulkarray('ECHO', "You've probably heard me before!", "Or not.", "Who knows?"))
    print(bulkarray('ECHO', "You've probably heard me before!"))
    print(parsebulkarray('*2\r\n$4\r\nECHO\r\n$6\r\nHello!\r\n'))
    print(parsebulkarray("*2\r\n$4\r\nECHO\r\n\$32\r\nYou've probably heard me before!\r\n"))
