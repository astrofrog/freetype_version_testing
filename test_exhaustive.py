import os
import string
from hashlib import md5

import matplotlib.pyplot as plt

fig = {}
ax = {}

for rend in ['grey', 'mono']:
    fig[rend] = plt.figure(figsize=(10,10))
    ax[rend] = fig[rend].add_subplot(1,1,1)

if not os.path.exists('bin'):
    os.mkdir('bin')

if not os.path.exists('output'):
    os.mkdir('output')

VERSIONS = ['2.1.10', '2.3.0', '2.3.1', '2.3.2', '2.3.3', '2.3.4', '2.3.5', '2.3.6', '2.3.7', '2.3.9', '2.3.10', '2.3.11', '2.3.12', '2.4.0', '2.4.1', '2.4.2', '2.4.3', '2.4.4', '2.4.5', '2.4.6', '2.4.7', '2.4.8', '2.4.9']
CHARACTERS = string.letters + string.digits

for ic, char in enumerate(CHARACTERS):

    print "CHARACTER: %s" % char
    
    hash_prev = {'mono':None, 'grey':None}

    for iv, version in enumerate(VERSIONS):

        install = 'freetype-%s_install' % version

        # Compile test script
        os.system('gcc `%s/bin/freetype-config --cflags` freetype_test/freetype_test.c `%s/bin/freetype-config --libs` -o bin/freetype_test_%s >& log_compile' % (install, install, version))

        os.system('DYLD_LIBRARY_PATH=%s/lib LD_LIBRARY_PATH=%s/lib bin/freetype_test_%s freetype_test/Vera.ttf %i 20 500 8 output/%s >& log_run' % (install, install, version, ord(char), version))

        for rend in ['grey', 'mono']:

            hash_curr = md5(open('output/%s_%s.pgm' % (version, rend)).read())

            if hash_prev[rend] is None:
                hash_prev[rend] = hash_curr
                color='green'
            else:
                if hash_prev[rend].hexdigest() != hash_curr.hexdigest():
                    print " -> %s changed at %s" % (rend, version)
                    hash_prev[rend] = hash_curr
                    color='red'
                else:
                    color='green'

            ax[rend].scatter([ic], [iv], edgecolor='none', facecolor=color)

for rend in ['grey', 'mono']:

    ax[rend].set_xlim(-0.5, len(CHARACTERS) - 0.5)
    ax[rend].xaxis.set_ticks(range(len(CHARACTERS)))
    ax[rend].xaxis.set_ticklabels([x for x in CHARACTERS])
    ax[rend].set_ylim(-0.5, len(VERSIONS) - 0.5)
    ax[rend].yaxis.set_ticks(range(len(VERSIONS)))
    ax[rend].yaxis.set_ticklabels(VERSIONS)

    fig[rend].savefig('breaking_points_%s.png' % rend)
