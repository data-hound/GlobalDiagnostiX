# -*- coding: utf-8 -*-

"""
Generate test-image for calculating the MTF
"""
from __future__ import division
import math
import numpy
import scipy.misc
import itertools
import matplotlib.pyplot as plt


def draw_fansegment(startradius, length, angle):
    plt.arrow(Size[1] / 2 + (startradius * numpy.cos(numpy.deg2rad(angle))),
              Size[0] / 2 + (startradius * numpy.sin(numpy.deg2rad(angle))),
              length * numpy.cos(numpy.deg2rad(angle)),
              length * numpy.sin(numpy.deg2rad(angle)))


def get_git_hash():
    """
    Get the current git hash from the repository.
    Good for saving this information into the log files of process.
    Based on http://stackoverflow.com/a/949391/323100 and
    http://stackoverflow.com/a/18283905/323100
    """
    from subprocess import Popen, PIPE
    import os
    gitprocess = Popen(['git', '--git-dir', os.path.join(os.getcwd(), '.git'),
                        'rev-parse', '--short', '--verify', 'HEAD'],
                       stdout=PIPE)
    (output, _) = gitprocess.communicate()
    return output.strip()

# Setup
Size = [800, 600]
numpy.random.seed(1796)
FilePrefix = 'Phantom_' + get_git_hash() + '_'

print 'Generating random image with a size of', Size[0], 'x', Size[1], 'px'
# Generate random image
ImageRandom = numpy.random.randint(2, size=Size) * 256
scipy.misc.imsave(FilePrefix + 'random.png', ImageRandom)
print 'Saved random image as', FilePrefix + 'random.png\n'

# Write grid onto image
GridSize = 100
for x, y in itertools.izip_longest(range(0, Size[0], GridSize),
                                   range(0, Size[1], GridSize)):
    if x:
        ImageRandom[x, :] = 1
    if y:
        ImageRandom[:, y] = 1
scipy.misc.imsave(FilePrefix + 'random_grid.png', ImageRandom)
print 'Saved random image with grid as', FilePrefix + 'random_grid.png\n'

# Checkerboard
print 'Generating checkerboard pattern with a size of', Size[0], 'x', Size[1], \
    'px'
StripeSize = 50
CheckerBoard = numpy.zeros(Size)
# Horizontal stripes
for x in range(Size[0]):
    if math.fmod(x, StripeSize * 2) < StripeSize:
        CheckerBoard[x, :] = 1
# vertical stripes stipes -> flip vertical 0/1
for y in range(Size[1]):
    if math.fmod(y, StripeSize * 2) < StripeSize:
        for x in range(Size[0]):
            if CheckerBoard[x, y]:
                CheckerBoard[x, y] = 0
            else:
                CheckerBoard[x, y] = 1
CheckerBoard[:StripeSize, :] = 1
CheckerBoard[-StripeSize:, :] = 1
CheckerBoard[:, :StripeSize] = 1
CheckerBoard[:, -StripeSize:] = 1
scipy.misc.imsave(FilePrefix + 'checkerboard.png', CheckerBoard)
print 'Saved checkerboard image as', FilePrefix + 'checkerboard.png\n'

print 'Generating star pattern with a size of', Size[0], 'x', Size[1], 'px'
# Draw star-pattern with defined length
saveDPI = 150
fig = plt.figure(figsize=(Size[1] / saveDPI, Size[0] / saveDPI))
Length = 100
angles = numpy.linspace(0, 360, 3600)
for radius in range(0, max(Size), 2 * Length):
    for angle in angles:
        if round(angle / 10) % 2 == 0:
            draw_fansegment(radius, Length, angle)
            draw_fansegment(radius + Length, Length, angle + 10)
    plt.plot(Size[1] / 2 + radius * numpy.cos(numpy.deg2rad(angles)),
             Size[0] / 2 + radius * numpy.sin(numpy.deg2rad(angles)),
             color='k', linewidth=2)
    plt.plot(Size[1] / 2 + radius / 2 * numpy.cos(numpy.deg2rad(angles)),
             Size[0] / 2 + radius / 2 * numpy.sin(numpy.deg2rad(angles)),
             color='k', linewidth=2)
plt.axis([0, Size[1], 0, Size[0]])
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)
fig.savefig(FilePrefix + 'star.png', dpi=saveDPI)
plt.close()
print 'Saved star pattern as', FilePrefix + 'star.png\n'

# Show what we've done
plt.figure('Result', figsize=(10, 10))
plt.suptitle('Images from script version ' + get_git_hash())
plt.subplot(221)
plt.imshow(plt.imread(FilePrefix + 'random.png'), cmap='gray',
           interpolation='nearest')
plt.title('Random image')
plt.axis('off')
plt.subplot(222)
plt.imshow(plt.imread(FilePrefix + 'random_grid.png'), cmap='gray',
           interpolation='nearest')
plt.title('with superimposed grid')
plt.axis('off')
plt.subplot(223)
plt.imshow(plt.imread(FilePrefix + 'star.png'), cmap='gray',
           interpolation='nearest')
plt.title('Poor mans Siemens star')
plt.subplot(224)
plt.axis('off')
plt.imshow(plt.imread(FilePrefix + 'checkerboard.png'), cmap='gray',
           interpolation='nearest')
plt.title('Checkerboard pattern')
plt.axis('off')
plt.show()
