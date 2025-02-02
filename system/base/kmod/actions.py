#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    options = "--sysconfdir=/etc \
               --with-zlib \
               --with-xz"
               
    if get.buildTYPE() == "emul32":
        options += " --bindir=/usr/emul32 \
                     --libdir=/usr/lib32"

    if get.buildTYPE() != "emul32":
        options += " --with-zstd"
                         
    autotools.configure(options)

def build():
    autotools.make()

# need git for check
#def check():     
#    autotools.make("check")

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    if get.buildTYPE() == "emul32":
        pisitools.removeDir("/usr/emul32")
        return

    pisitools.dosym("modprobe.d.5.gz","/usr/share/man/man5/modprobe.conf.5.gz")
    for sym in ["modinfo","insmod","rmmod","depmod","modprobe"]:
        pisitools.dosym("/usr/bin/kmod","/sbin/%s" % sym)

    pisitools.dosym("/usr/bin/kmod","/bin/lsmod")

    pisitools.makedirs("%s/etc/depmod.d" % get.installDIR())
    pisitools.makedirs("%s/etc/modprobe.d" % get.installDIR())
    pisitools.dodoc("NEWS", "README", "TODO", "COPYING")
