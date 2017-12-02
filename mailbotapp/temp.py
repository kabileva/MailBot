string = '\\xD1\\x80\\xD1\\x80'
try:
    string.decode('utf-8')
    print "string is UTF-8, length %d bytes" % len(string)
except UnicodeError:
    print "string is not UTF-8"
