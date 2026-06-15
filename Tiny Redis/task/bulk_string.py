import re

def findCommand(string: str) -> str:
    """
    Finds the command, which should be all caps at the beginning of the string.
    :param string: The input string.
    :return two strings: The extracted command and data.
    """
    commmandPattern = re.compile(r"([A-Z]+\b)")
    dataPattern = re.compile(r"\"(.+?)\"")
    command = re.match(commmandPattern, string)  # Using match to limit our attention to the beginning of the string.
    data = re.findall(dataPattern, string)  # Using findall to now broaden our search.
    return bulkstring(command.group(0)), bulkstring()

def bulkstring(string: str) -> str:
    return str('$' + str(len(string)) + '\\r\\n' + string + '\\r\\n')

def bulkArray(command: str, *args: str) -> str:
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

if __name__ == '__main__':
    # print(bulkString('ECHO').encode())
    # print(bulkString('EXIT'))
    print(bulkArray('EXIT'))
    print(bulkArray('ECHO', 'Hello!'))
    print(bulkArray('ECHO', "You've probably heard me before!", "Or not.", "Who knows?"))
    print(bulkArray('ECHO', "You've probably heard me before!"))
