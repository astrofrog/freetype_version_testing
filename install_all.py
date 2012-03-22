import os
import shutil
import glob
import tarfile

for freetype in glob.glob('freetype-*.tar.gz'):

    free_dir = freetype.replace('.tar.gz', '')

    # Remove previously existing library
    if os.path.exists(free_dir):
        shutil.rmtree(free_dir)

    # Expand
    t = tarfile.open(freetype)
    t.extractall()

    # Configure and make
    os.chdir(free_dir)
    os.system('./configure --prefix=%s' % os.path.abspath('../%s_install' % free_dir))
    os.system('make')
    os.system('make install')
    os.chdir('..')
