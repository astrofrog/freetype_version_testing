import os
import glob
import string
from hashlib import md5

if not os.path.exists('bin'):
    os.mkdir('bin')

if not os.path.exists('output'):
    os.mkdir('output')

VERSIONS = ['2.1.10', '2.3.0', '2.3.1', '2.3.2', '2.3.3', '2.3.4', '2.3.5', '2.3.6', '2.3.7', '2.3.9', '2.3.10', '2.3.11', '2.3.12', '2.4.0', '2.4.1', '2.4.2', '2.4.3', '2.4.4', '2.4.5', '2.4.6', '2.4.7', '2.4.8', '2.4.9']

for char in string.letters + string.digits:

    print "CHARACTER: %s" % char

    hash_prev = None

    for version in VERSIONS:
        
        install = 'freetype-%s_install' % version

        # Compile test script
        os.system('gcc `%s/bin/freetype-config --cflags` freetype_test/freetype_test.c `%s/bin/freetype-config --libs` -o bin/freetype_test_%s >& log_compile' % (install, install, version))

        os.system('DYLD_LIBRARY_PATH=%s/lib LD_LIBRARY_PATH=%s/lib bin/freetype_test_%s freetype_test/Vera.ttf %i 20 500 8 output/%s >& log_run' % (install, install, version, ord(char), version))

        hash_curr = md5(open('output/%s_mono.pgm' % version).read())

        if hash_prev is None:
            hash_prev = hash_curr
        else:
            if hash_prev.hexdigest() != hash_curr.hexdigest():
                print " -> changed at %s" % version
                hash_prev = hash_curr
