import os
import glob

for install in glob.glob('freetype*_install'):
    
    # Get version
    p1 = install.index('-')
    p2 = install.index('_')
    version = install[p1+1:p2]
    
    print version
    
    # Compile test script
    os.system('gcc `%s/bin/freetype-config --cflags` freetype_test/freetype_test.c `%s/bin/freetype-config --libs` -o bin/freetype_test_%s' % (install, install, version))

    os.system('DYLD_LIBRARY_PATH=%s/lib bin/freetype_test_%s freetype_test/Vera.ttf 97 20 500 8 output/%s' % (install, version, version))