#!/usr/bin/env python
# -*- coding: ascii -*-
# Program msys_build_deps.py
# Requires Python 2.7 or later and win32api.

"""Build Pygame dependencies using MinGW and MSYS

Configured for Pygame 1.9.2 and Python 2.7 or higher.

By default the libraries are installed in the MSYS directory /usr/local unless
a different directory is specified by the --prefix command line argument.

This program can be run from a Windows cmd.exe or MSYS terminal. The current
directory and its outer directory are searched for the library source
directories. Run the program from the pygame trunk directory. The Windows
file path cannot have spaces in it.

The recognized, and optional, environment variables are:
  PREFIX - Destination directory
  MSYS_ROOT_DIRECTORY - MSYS home directory (may omit 1.0 subdirectory)
  CPPFLAGS - preprocessor options, appended to options set by the program
  CFLAGS - compiler flags, appended to options set by the program
  LDFLAGS - linker options, prepended to flags set by the program

To get a list of command line options run

python build_deps.py --help

This program has been tested against the following libraries:

SDL 1.2.15
SDL_image 1.2.12
SDL_mixer 1.2.12
SDL_ttf 2.0.11
smpeg-0.4.5
freetype 2.4.10
libogg 1.3.0
libvorbis 1.3.3
FLAC 1.2.1
mikmod 3.1.12 patched (included with SDL_mixer 1.2.12)
tiff 4.0.3
libpng 1.6.2
jpeg 9
zlib 1.2.8
PortMidi revision 217

The build environment used: 

GCC 4.8.1
MSYS 1.0.17
dx7 headers
nasm 2.11.06

The libraries are linked to the msvcrt.dll, the VC 6.0 runtime library.

The build has been performed on Windows XP, SP3.

Build issues:
  An intermittent problem was noted with SDL's configure involving locking of
  conftest.exe resulting in various C library functions being reported unavailable
  when in fact they are present. This does not appear to be a problem with the
  configure script itself but rather Msys. If it happens then just rerun
  msys_build_deps.py.
"""

import msys

from optparse import OptionParser
import os
import sys
from glob import glob
import time

# For Python 2.x/3.x compatibility
def geterror():
    return sys.exc_info()[1]

#
#   Generic declarations
#
hunt_paths = ['.', '..']

default_prefix_mp = '/usr/local'

def prompt(p=None):
    """MSYS friendly raw_input
    
    This provides a hook that can be replaced for testing.
    """
    
    msys.msys_raw_input(p)

def print_(*args, **kwds):
    msys.msys_print(*args, **kwds)

def confirm(message):
    """Ask a yes/no question, return result"""
    
    reply = prompt("\n%s [Y/n]:" % message)
    if reply and reply[0].lower() == 'n':
        return 0
    return 1

def as_flag(b):
    """Return bool b as a shell script flag '1' or '0'"""
    
    if b:
        return '1'
    return '0'

def as_linker_lib_path(p):
    """Return as an ld library path argument"""
    
    if p:
        return '-L' + p
    return ''

def as_linker_option(p):
    """Return as an ld library path argument"""
    
    if p:
        return '-Wl,' + p
    return ''

def as_preprocessor_header_path(p):
    """Return as a C preprocessor header include path argument"""
    
    if p:
        return '-I' + p
    return ''

def as_macro_define(m, v):
    """Return as a C preprocessor command line macro definition"""
    
    if v:
        return '-D%s=%s' % (m, v)
    return '-D%s' % (m,)
        
def merge_strings(*args, **kwds):
    """Returns non empty string joined by sep

    The default separator is an empty string.
    """

    sep = kwds.get('sep', '')
    return sep.join([s for s in args if s])
   
class BuildError(Exception):
    """Raised for missing source paths and failed script runs"""
    pass

class Dependency(object):
    """Builds a library"""
    
    def __init__(self, name, wildcards, libs, shell_script):
        self.name = name
        self.wildcards = wildcards
        self.shell_script = shell_script
        self.libs = libs

    def configure(self, hunt_paths):
        self.path = None
        self.paths = []
        self.hunt(hunt_paths)
        self.choosepath()

    def hunt(self, hunt_paths):
        parent = os.path.abspath('..')
        for p in hunt_paths:
            for w in self.wildcards:
                found = glob(os.path.join(p, w))
                found.sort() or found.reverse()  #reverse sort
                for f in found:
                    if f[:5] == '..'+os.sep+'..' and \
                        os.path.abspath(f)[:len(parent)] == parent:
                        continue
                    if os.path.isdir(f):
                        self.paths.append(f)

    def choosepath(self):
        path = None
        if not self.paths:
            raise BuildError("Path for %s: not found" % self.name)
        if len(self.paths) == 1:
            path = self.paths[0]
        else:
            print_("Select path for %s:" % self.name)
            for i in range(len(self.paths)):
                print_("  %d = %s" % (i+1, self.paths[i]))
            print_("  0 = <Nothing>")
            choice = prompt("Select 0-%d (1=default):" % len(self.paths))
            if not choice:
                choice = 1
            else:
                choice = int(choice)
            if choice > 0:
                path = self.paths[choice-1]
        if path is not None:
            self.path = os.path.abspath(path)

    def build(self, msys):
        if self.path is not None:
            env_home = msys.environ.get('HOME', None)
            msys.environ['HOME'] = self.path
            try:
                return_code = msys.run_shell_script(self.shell_script)
            finally:
                if env_home is not None:
                    msys.environ['HOME'] = env_home
                else:
                    del msys.environ['HOME']
            if return_code != 0:
                raise BuildError("The build for %s failed with code %d" %
                                 (self.name, return_code))
        else:
            raise BuildError("No source directory for %s" % self.name)

class Preparation(object):
    """Perform necessary build environment preparations"""
    
    def __init__(self, name, shell_script):
        self.name = name
        self.path = ''
        self.paths = []
        self.libs = []
        self.shell_script = shell_script

    def configure(self, hunt_paths):
        pass

    def build(self, msys):
        return_code = msys.run_shell_script(self.shell_script)
        if return_code != 0:
            raise BuildError("Preparation '%s' failed with code %d" %
                             (self.name, return_code))

def configure(dependencies, hunt_paths):
    """Find source directories of all dependencies"""
    
    success = True
    print_("Hunting for source directories...")
    for dep in dependencies:
        try:
            dep.configure(hunt_paths)
        except BuildError:
            print_(geterror())
            success = False
        else:
            if dep.path:
                print_("Source directory for", dep.name, ":", dep.path)
    if not success:
        raise BuildError("Not all source directories were found")

def build(dependencies, msys):
    """Execute the shell scripts for all dependencies"""
    
    for dep in dependencies:
        print_("\n\n----", dep.name, "----")
        dep.build(msys)

def command_line():
    """Process the command line and return the options"""
    
    usage = ("usage: %prog [options] --all\n"
             "       %prog [options] [args]\n"
             "\n"
             "Build the Pygame dependencies. The args, if given, are\n"
             "libraries to include or exclude.\n"
             "\n"
             "At startup this program may prompt for missing information.\n"
             "Be aware of this before redirecting output or leaving the\n"
             "program unattended. Once the 'Starting build' message appears\n"
             "no more user input is required. The build process will\n"
             "abort on the first error, as library build order is important.\n"
             "\n"
             "See --help-args.\n"
             "\n"
             "For more details see the program's document string\n")
    
    parser = OptionParser(usage)
    parser.add_option('-a', '--all', action='store_true', dest='build_all',
                      help="Include all libraries in the build")
    parser.set_defaults(build_all=False)
    parser.add_option('--no-configure', action='store_false', dest='configure',
                      help="Do not prepare the makefiles")
    parser.set_defaults(configure=True)
    parser.add_option('--no-compile', action='store_false', dest='compile',
                      help="Do not compile or install the libraries")
    parser.set_defaults(compile=True)
    parser.add_option('--no-install', action='store_false', dest='install',
                      help="Do not install the libraries")
    parser.add_option('--no-strip', action='store_false', dest='strip',
                      help="Do not strip the library")
    parser.set_defaults(strip=True)
    parser.set_defaults(install=True)
    parser.add_option('--clean', action='store_true', dest='clean',
                      help="Remove generated files (make clean)"
                           " as a last step")
    parser.set_defaults(clean=False)
    parser.add_option('--clean-only', action='store_true', dest='clean_only',
                      help="Perform only a clean")
    parser.set_defaults(clean_only=False)
    parser.add_option('-e', '--exclude', action='store_true', dest='exclude',
                      help="Exclude the specified libraries")
    parser.set_defaults(exclude=False)
    parser.add_option('-m', '--msys-root', action='store',
                      dest='msys_directory',
                      help="MSYS directory path, which may include"
                           " the 1.x subdirectory")
    parser.set_defaults(msys_directory='')
    parser.add_option('-s', '--sources', action='store',
                      dest='sources',
                      help="Paths to search for library source directories"
                           " as a semicolon ';' separated list: defaults to %s"
                           % (';'.join(hunt_paths),))
    parser.add_option('-p', '--prefix', action='store',
                      dest='prefix',
                      help="Destination directory of the build: defaults to MSYS %s"
                           % (default_prefix_mp,))
    parser.set_defaults(prefix='')
    parser.add_option('--help-args', action='store_true', dest='arg_help',
                      help="Show a list of recognised libraries,"
                           " in build order, and exit")
    parser.set_defaults(arg_help=False)
    parser.add_option('--subsystem-noforce', action='store_true', dest='subsystem_noforce',
                      help="Do not force the dlls to build with the GUI subsystem type")
    parser.set_defaults(subsystem_noforce=False)
    parser.add_option('-b', '--beep', action='store_true', dest='finish_alert',
                      help="Beep the computer speaker when finished.")
    parser.set_defaults(finish_alert=False)
    parser.add_option('-n', '--beep-ntimes', type='int', action='store', dest='finish_alert_ntimes',
                      help="Beep the computer speaker n times when finished")
    parser.set_defaults(finish_alert_ntimes=0)
    return parser.parse_args()

def set_environment_variables(msys, options):
    """Set the environment variables used by the scripts"""
    
    environ = msys.environ

    msys_root_wp = msys.msys_root
    prefix_wp = options.prefix
    if not prefix_wp:
        prefix_wp = environ.get('PREFIX', '')
    if prefix_wp:
        prefix_mp = msys.windows_to_msys(prefix_wp)
    else:
        prefix_mp = default_prefix_mp
        prefix_wp = msys.msys_to_windows(prefix_mp)
    include_mp = prefix_mp + '/include'
    lib_mp = prefix_mp + '/lib'
    subsystem = ''
    if not options.subsystem_noforce:
        subsystem = '-mwindows'
    resources_mp = ''

    environ['PREFIX'] = prefix_mp
    environ.pop('INCLUDE', None)  # INCLUDE causes problems with MIXER.
    environ['CPPFLAGS'] = merge_strings(as_preprocessor_header_path(include_mp),
                                        environ.get('CPPFLAGS', ''),
                                        sep=' ')
    # Need to make the resources object file an explicit linker option to
    # bypass libtool (freetype).
    environ['LDFLAGS'] = merge_strings(environ.get('LDFLAGS', ''),
                                       as_linker_lib_path(lib_mp),
                                       as_linker_option(resources_mp),
                                       subsystem,
                                       sep=' ')

    environ['BDCONF'] = as_flag(options.configure and
                                not options.clean_only)
    environ['BDCOMP'] = as_flag(options.compile and
                                not options.clean_only)
    environ['BDINST'] = as_flag(options.install and
                                options.compile and
                                not options.clean_only)
    environ['BDSTRIP'] = as_flag(options.compile and
                                 options.install and
                                 options.strip and
                                 not options.clean_only)
    environ['BDCLEAN'] = as_flag(options.clean or options.clean_only)
    environ['BDMSVCRT_VERSION'] = '%i' % (options.msvcrt_version,)
    environ['BDRESOURCES'] = resources_mp

class ChooseError(Exception):
    """Failure to select dependencies"""
    pass

def choose_dependencies(dependencies, options, args):
    """Return the dependencies to actually build"""

    if options.build_all:
        if args:
            raise ChooseError("No library names are accepted"
                              " for the --all option.")
        if options.exclude:
            return []
        else:
            return dependencies

    if args:
        names = [d.name for d in dependencies]
        args = [a.upper() for a in args]
        for a in args:
            if a not in names:
                msg = ["%s is an unknown library; valid choices are:" % a]
                msg.extend(names)
                raise ChooseError('\n'.join(msg))
        if options.exclude:
            return [d for d in dependencies if d.name not in args]
        return [d for d in dependencies if d.name in args]

    return []
    
def summary(dependencies, msys, start_time, chosen_deps):
    """Display a summary report of new, existing and missing libraries"""

    import datetime

    print_("\n\n=== Summary ===")
    if start_time is not None:
        print_("  Elapse time:",
               datetime.timedelta(seconds=time.time()-start_time))
    print_()
    for dep in chosen_deps:
        if dep.path is None:
            print_("  ** No source directory found for", dep.name)
        elif dep.path:
            print_("  Source directory for", dep.name, ":", dep.path)
    print_()
    prefix = msys.msys_to_windows(msys.environ['PREFIX']).replace('/', os.sep)
    bin_dir = os.path.join(prefix, 'bin')
    lib_dir = os.path.join(prefix, 'lib')
    for d in dependencies:
        for lib in d.libs:
            if lib.endswith('.dll'):
                lib_path = os.path.join(bin_dir, lib)
                try:
                    mod_time = os.path.getmtime(lib_path)
                except:
                    msg = "No DLL"
                else:
                    if mod_time >= start_time:
                        msg = "Installed new DLL %s" % (lib_path,)
                    else:
                        msg = "-- (old DLL %s)" % (lib_path,)
            elif lib.endswith('.a'):
                lib_path = os.path.join(lib_dir, lib)
                try:
                    mod_time = os.path.getmtime(lib_path)
                except:
                    msg = "No static library"
                else:
                    if mod_time >= start_time:
                        msg = "Installed new static library %s" % (lib_path,)
                    else:
                        msg = "-- (old static library %s)" % (lib_path,)
            else:
                msg = "Internal error: unknown library type %s" % (lib,)
            print_("  %-10s: %s" % (d.name, msg))
    
def main(dependencies, msys_preparation):
    """Build the dependencies according to the command line options."""

    options, args = command_line()
    if options.arg_help:
        print_("These are the Pygame library dependencies:")
        for dep in dependencies:
            print_(" ", dep.name)
        return 0
        
    # Only building against msvcrt.dll for now.
    options.msvcrt_version = 60
    
    try:
        chosen_deps = choose_dependencies(dependencies, options, args)
    except ChooseError:
        print_(geterror())
        return 1
    if not chosen_deps:
        if not args:
            print_("No libraries specified.")
        elif options.build_all:
            print_("All libraries excluded")
    print_("Linking to C runtime library msvcrt.dll.")
    if chosen_deps and not options.clean_only:
        chosen_deps.insert(0, msys_preparation)
    try:
        m = msys.Msys(options.msys_directory)
    except msys.MsysException:
        print_(geterror())
        return 1
    print_("Using MSYS in directory:", m.msys_root)
    print_("MinGW directory:", m.mingw_root)
    start_time = None
    return_code = 1
    set_environment_variables(m, options)
    if not options.clean_only:
        print_("Destination directory:",
               m.msys_to_windows(m.environ['PREFIX']).replace('/', os.sep))
    print_("common CPPFLAGS:", m.environ.get('CPPFLAGS', ''))
    print_("common CFLAGS:", m.environ.get('CFLAGS', ''))
    print_("common LDFLAGS:", m.environ.get('LDFLAGS', ''))
    sources = hunt_paths
    if options.sources:
        sources = options.sources.split(';')
    print_("library source directories search paths: %s" % (';'.join(sources),))
    try:
        configure(chosen_deps, sources)
    except BuildError:
        print_("Build aborted:", geterror())
    else:
        if options.clean_only:
            print_("\n=== Performing clean ===")
        else:
            print_("\n=== Starting build ===")
        start_time = time.time()  # For file timestamp checks.
        try:
            build(chosen_deps, m)
        except BuildError:
            print_("Build aborted:", geterror())
        else:
            # A successful build!
            return_code = 0
    if not options.clean_only:
        summary(dependencies, m, start_time, chosen_deps)

    # MinGW configure file for setup.py (optional).
    try:
        import mingwcfg
    except ImportError:
        pass
    else:
        mingwcfg.write(m.mingw_root)

    if options.finish_alert or options.finish_alert_ntimes > 0:
        if options.finish_alert_ntimes > 0:
            m.environ['BDNTIMES'] = "%i" % (options.finish_alert_ntimes,)
        alert.build(m)
    return return_code

#
#   Build specific code
#

# This list includes the MSYS shell scripts to build each library. Each script
# runs in an environment where MINGW_ROOT_DIRECTORY is defined and the MinGW
# bin directory is in PATH. Four build control environment variables are
# defined: BDCONF, BDCOMP, BDINST and BDCLEAN. They are either '0' or '1'. They
# represent configure, compile, install and clean respectively. When '1' the
# corresponding action is performed. When '0' it is skipped. The installation
# directory is given by PREFIX. The script needs to prepend it to PATH. The
# script's HOME directory is the source code root directory. Various gcc flags
# are in CPPFLAGS, CFLAGS, and LDFLAGS. INCLUDE is undefined.
#
# None of these scripts end with an "exit". Exit, possibly, leads to Msys
# freezing on some versions of Windows (98).
# 
# The list order corresponds to build order. It is critical.
dependencies = [
    Dependency('SDL', ['SDL-[1-9].*'], ['SDL.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if [ x$BDCONF == x1 ]; then
  # Remove NONAMELESSUNION from directx.h headers.
  for d in video audio; do
    BDDXHDR=src/$d/windx5/directx.h
    cp -f $BDDXHDR $BDDXHDR'_'
    sed 's/^\\(#define NONAMELESSUNION\\)/\\/*\\1*\\//' $BDDXHDR'_' >$BDDXHDR
    if [ x$? != x0 ]; then exit $?; fi
    rm $BDDXHDR'_'
    BDDXHDR=
  done

  # If this comes from the repository it has no configure script
  if [ ! -f "./configure" ]; then
    ./autogen.sh
  fi

  mkdir -p ./pgbuild
  
  cd ./pgbuild
  ../configure --prefix="$PREFIX" --disable-static --disable-stdio-redirect \
               CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
  
  # check for MSYS permission errors
  if [ x"`grep 'Permission denied' config.log`" != x ]; then
      echo '**** MSYS problems; build aborted.'
      exit 1
  fi
  cd ..
fi

if [ x$BDCOMP == x1 ]; then
  cd ./pgbuild
  make
  cd ..
fi

if [ x$BDINST == x1 ]; then
  cd ./pgbuild
  make install-bin install-hdrs install-lib
  # Need SDL_config.h.default and SDL_config_win32.h for Windows.
  cp -f "$HOME/include/SDL_config_win32.h" "$PREFIX/include/SDL"
  cp -f "$HOME/include/SDL_config.h.default" "$PREFIX/include/SDL/SDL_config.h"
  cd ..
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/SDL.dll"
fi

if [ x$BDCLEAN == x1 ]; then
  cd ./pgbuild
  set +e
  make clean
  cd ..
fi
"""),
    Dependency('Z', ['zlib-[1-9].*'], ['zlib1.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if [ x$BDCONF == x1 ]; then
  cp -fp win32/Makefile.gcc .
  # Will use contributed asm code.
  cp -fp contrib/asm686/match.S .
fi

if [ x$BDCOMP == x1 ]; then
  # Build with the import library renamed, using asm code, our CPPFLAGS,
  # CFLAGS, and LDFLAGS (passed in as LOC).
  make IMPLIB=libz.dll.a OBJA=match.o -fMakefile.gcc
       CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LOC="-DASMV $LDFLAGS"
fi

if [ x$BDINST == x1 ]; then
  # Make sure everything is installed in the correct places
  make install LIBRARY_PATH="$PREFIX/lib" INCLUDE_PATH="$PREFIX/include" \
    BINARY_PATH="$PREFIX/bin" SHARED_MODE=1 IMPLIB=libz.dll.a -fMakefile.gcc
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/zlib1.dll"
fi

if [ x$BDCLEAN == x1 ]; then
  set +e
  make clean -fMakefile.gcc
fi
"""),
    Dependency('FREETYPE', ['freetype-[2-9].*'], ['libfreetype-6.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if [ x$BDCONF == x1 ]; then
  mkdir -p ./pgbuild
  
  cd ./pgbuild
  ../configure --prefix="$PREFIX" \
               CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
  
  # check for MSYS permission errors
  if [ x"`grep 'Permission denied' builds/unix/config.log`" != x ]; then
      echo '**** MSYS problems; build aborted.'
      exit 1
  fi
  cd ..
fi

if [ x$BDCOMP == x1 ]; then
  cd ./pgbuild
  make
  cd ..
fi

if [ x$BDINST == x1 ]; then
  cd ./pgbuild
  make install
  cd ..
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/libfreetype-6.dll"
fi

if [ x$BDCLEAN == x1 ]; then
  cd ./pgbuild
  set +e
  make clean
  cd ..
fi
"""),
    Dependency('FONT', ['SDL_ttf-[2-9].*'], ['SDL_ttf.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if [ x$BDCONF == x1 ]; then
  # If this comes from the repository it has no configure script
  if [ ! -f "./configure" ]; then
    ./autogen.sh
  fi

  mkdir -p ./pgbuild
  
  cd ./pgbuild
  ../configure --prefix="$PREFIX" \
               CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
  
  # check for MSYS permission errors
  if [ x"`grep 'Permission denied' config.log`" != x ]; then
      echo '**** MSYS problems; build aborted.'
      exit 1
  fi
  cd ..
fi

if [ x$BDCOMP == x1 ]; then
  cd ./pgbuild
  make
  cd ..
fi

if [ x$BDINST == x1 ]; then
  cd ./pgbuild
  make install
  cd ..
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/SDL_ttf.dll"
fi

if [ x$BDCLEAN == x1 ]; then
  cd ./pgbuild
  set +e
  make clean
  cd ..
fi
"""),
    Dependency('PNG', ['l*png*[1-9][1-9.]*'], ['libpng16-16.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if [ x$BDCONF == x1 ]; then
  mkdir -p ./pgbuild
  
  cd ./pgbuild
  ../configure --prefix="$PREFIX" \
               CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
  
  # check for MSYS permission errors
  if [ x"`grep 'Permission denied' config.log`" != x ]; then
      echo '**** MSYS problems; build aborted.'
      exit 1
  fi
  cd ..
fi

if [ x$BDCOMP == x1 ]; then
  cd ./pgbuild
  make
  cd ..
fi

if [ x$BDINST == x1 ]; then
  cd ./pgbuild
  make install
  cd ..
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/libpng16-16.dll"
fi

if [ x$BDCLEAN == x1 ]; then
  cd ./pgbuild
  set +e
  make clean -fMakefile.mingw prefix="$PREFIX"
  cd ..
fi
"""),
    Dependency('JPEG', ['jpeg-[6-9]*'], ['libjpeg-9.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if [ x$BDCONF == x1 ]; then
  mkdir -p ./pgbuild
  
  cd ./pgbuild
  ../configure --prefix="$PREFIX" \
               CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
  
  # check for MSYS permission errors
  if [ x"`grep 'Permission denied' config.log`" != x ]; then
      echo '**** MSYS problems; build aborted.'
      exit 1
  fi

  cp ../jconfig.vc jconfig.h
  cd ..
fi

if [ x$BDCOMP == x1 ]; then
  cd ./pgbuild
  make
  cd ..
fi

if [ x$BDINST == x1 ]; then
  cd ./pgbuild
  make install
  cd ..
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/libjpeg-9.dll"
fi

if [ x$BDCLEAN == x1 ]; then
  cd ./pgbuild
  set +e
  make clean
  cd ..
fi
"""),
    Dependency('TIFF', ['tiff-[3-9].*'], ['libtiff-5.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

# Only building the library.
bd_subdirs="port libtiff"


if [ x$BDCONF == x1 ]; then
  mkdir -p ./pgbuild
  
  cd ./pgbuild
  ../configure --disable-cxx --prefix="$PREFIX" \
               CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
  
  # check for MSYS permission errors
  if [ x"`grep 'Permission denied' config.log`" != x ]; then
      echo '**** MSYS problems; build aborted.'
      exit 1
  fi
  cd ..
fi

if [ x$BDCOMP == x1 ]; then
  cd ./pgbuild
  make SUBDIRS="$bd_subdirs"
  cd ..
fi

if [ x$BDINST == x1 ]; then
  cd ./pgbuild
  make install SUBDIRS="$bd_subdirs"
  cd ..
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/libtiff-5.dll"
fi

if [ x$BDCLEAN == x1 ]; then
  cd ./pgbuild
  set +e
  make clean SUBDIRS="$bd_subdirs"
  rm -f libtiff.dll.a
  rm -f libtiff.dll
  cd ..
fi
"""),
    Dependency('WEBP', ['libwebp-[0].*'], ['libwebp-4.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if [ x$BDCONF == x1 ]; then
  mkdir -p ./pgbuild

  cd ./pgbuild
  ../configure --prefix="$PREFIX" \
               CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS" \
               --disable-static
  
  # check for MSYS permission errors
  if [ x"`grep 'Permission denied' config.log`" != x ]; then
      echo '**** MSYS problems; build aborted.'
      exit 1
  fi
  cd ..
fi

if [ x$BDCOMP == x1 ]; then
  cd ./pgbuild
  make
  cd ..
fi

if [ x$BDINST == x1 ]; then
  cd ./pgbuild
  make install
  cd ..
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/libwebp-4.dll"
fi

if [ x$BDCLEAN == x1 ]; then
  cd ./pgbuild
  set +e
  make clean
  cd ..
fi
"""),
    Dependency('IMAGE', ['SDL_image-[1-9].*'], ['SDL_image.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if [ x$BDCONF == x1 ]; then
  # If this comes from the repository it has no configure script
  if [ ! -f "./configure" ]; then
    ./autogen.sh
  fi

  # configure searches for the JPEG dll. Unfortunately it uses the wrong file
  # name. Correct this.
  mv configure configure~
  sed -e 's|jpeg\.dll|libjpeg-*.dll|' configure~ >configure
  
  # Add the destination bin directory to the library search path so
  # configure can find its precious DLL files.
  export LDFLAGS="$LDFLAGS -L$PREFIX/bin"
  
  # Add path to PNG headers
  CPPFLAGS="$CPPFLAGS `$PREFIX/bin/libpng-config --I_opts`"
  
  mkdir -p ./pgbuild
  
  cd ./pgbuild
  # Disable dynamic loading of image libraries as it uses the wrong DLL
  # search path: does not check in the same directory.
  #  --disable-libtool-lock: Prevent libtool deadlocks (maybe).
  ../configure --disable-jpg-shared --disable-png-shared --disable-tif-shared \
               --disable-webp-shared --disable-libtool-lock --prefix="$PREFIX" \
               CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
  
  # check for MSYS permission errors
  if [ x"`grep 'Permission denied' config.log`" != x ]; then
      echo '**** MSYS problems; build aborted.'
      exit 1
  fi
  cd ..
fi

if [ x$BDCOMP == x1 ]; then
  cd ./pgbuild
  make
  cd ..
fi

if [ x$BDINST == x1 ]; then
  cd ./pgbuild
  make install
  cd ..
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/SDL_image.dll"
fi

if [[ x$BDCLEAN == x1 && -f Makefile ]]; then
  cd ./pgbuild
  set +e
  make clean
  cd ..
fi
"""),
    Dependency('SMPEG', ['smpeg-[0-9].*', 'smpeg'], ['smpeg.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if (( $BDMSVCRT_VERSION != 60 )); then
  echo The smpeg build has been disabled\\.
  exit 0
fi

if [ x$BDCONF == x1 ]; then
  # This comes straight from SVN so has no configure script
  if [ ! -f "./configure" ]; then
    ./autogen.sh
  fi

  mkdir -p ./pgbuild
  
  cd ./pgbuild
  # Don't need the toys. Disable dynamic linking of libgcc and libstdc++
  ../configure --disable-gtk-player --disable-opengl-player --prefix="$PREFIX" \
               CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
              
  # check for MSYS permission errors
  if [ x"`grep 'Permission denied' config.log`" != x ]; then
      echo '**** MSYS problems; build aborted.'
      exit 1
  fi
  cd ..
fi

if [ x$BDCOMP == x1 ]; then
  cd ./pgbuild
  # Only build the DLL. Leave out undefined symbols so the DLL will build.
  make libsmpeg.la CXXLD='$(CXX) -no-undefined'
  cd ..
fi

if [ x$BDINST == x1 ]; then
  cd ./pgbuild
  make install-libLTLIBRARIES \
       install-libsmpegincludeHEADERS \
       install-binSCRIPTS
  cd ..
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/smpeg.dll"
fi

if [[ x$BDCLEAN == x1 && -f Makefile ]]; then
  cd ./pgbuild
  set +e
  make clean
  cd ..
fi
"""),
    Dependency('OGG', ['libogg-[1-9].*'], ['libogg-0.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if [ x$BDCONF == x1 ]; then
  mkdir -p ./pgbuild
  
  cd ./pgbuild
  # configure looks for a previous build. Remove if found.
  if [ -f "Makefile" ]; then
    make distclean
  fi
  ../configure --prefix="$PREFIX" --disable-static \
               CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
  
  # check for MSYS permission errors
  if [ x"`grep 'Permission denied' config.log`" != x ]; then
      echo '**** MSYS problems; build aborted.'
      exit 1
  fi
  cd ..
fi

if [ x$BDCOMP == x1 ]; then
  cd ./pgbuild
  make
  cd ..
fi

if [ x$BDINST == x1 ]; then
  cd ./pgbuild
  make install
  cd ..
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/libogg-0.dll"
fi

if [[ x$BDCLEAN == x1 && -f Makefile ]]; then
  cd ./pgbuild
  set +e
  make clean
  cd ..
fi
"""),
    Dependency('VORBIS',
               ['libvorbis-[1-9].*'],
               ['libvorbis-0.dll', 'libvorbisfile-3.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if [ x$BDCONF == x1 ]; then
  mkdir -p ./pgbuild
  
  cd ./pgbuild
  # configure looks for a previous build. Remove if found.
  if [ -f "Makefile" ]; then
    make distclean
  fi
  ../configure --prefix="$PREFIX" --disable-static \
               CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS" LIBS='-logg'
  # check for MSYS permission errors
  if [ x"`grep 'Permission denied' config.log`" != x ]; then
      echo '**** MSYS problems; build aborted.'
      exit 1
  fi
  cd ..
fi

if [ x$BDCOMP == x1 ]; then
  cd ./pgbuild
  make
  cd ..
fi

if [ x$BDINST == x1 ]; then
  cd ./pgbuild
  make install
  cd ..
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/libvorbis-0.dll"
  strip --strip-all "$PREFIX/bin/libvorbisfile-3.dll"
fi

if [[ x$BDCLEAN == x1 && -f Makefile ]]; then
  cd ./pgbuild
  set +e
  make clean
  cd ..
fi
"""),
    Dependency('FLAC', ['flac-[1-9].*'], ['libFLAC.a'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if [ x$BDCONF == x1 ]; then
  # Add __MINGW32__ to SIZE_T_MAX declaration test in alloc.h header.
  BDHDR='include/share/alloc.h'
  BDTMP='alloc.h_'
  cp -f "$BDHDR" "$BDTMP"
  sed 's/^#  ifdef _MSC_VER$/#  if defined _MSC_VER || defined __MINGW32__/' \
    "$BDTMP" >"$BDHDR"
  rm "$BDTMP"

  # Will only install a static library, but that is all that is needed.
  ./configure --disable-shared --disable-ogg --disable-cpplibs \
    --disable-doxygen-docs --prefix="$PREFIX" \
              CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
  
  # check for MSYS permission errors
  if [ x"`grep 'Permission denied' config.log`" != x ]; then
      echo '**** MSYS problems; build aborted.'
      exit 1
  fi
fi

if [ x$BDCOMP == x1 ]; then
  make
fi

if [ x$BDINST == x1 ]; then
  cp src/libFLAC/.libs/libFLAC.a "$PREFIX/lib"
  mkdir -p "$PREFIX/include/FLAC"
  cp -f include/FLAC/*.h "$PREFIX/include/FLAC"
fi

if [[ x$BDCLEAN == x1 && -f Makefile ]]; then
  set +e
  make clean
fi
"""),
    Dependency('MIKMOD', ['libmikmod-3.*'], ['libmikmod.a'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if [ x$BDCONF == x1 ]; then

  function mikmod_getver
  {
    gawk '\
      function getnum(s)
      {
        match(s, /[0-9]+/)
        return substr(s, RSTART, RLENGTH)
      }
      /^LIBMIKMOD_MAJOR_VERSION *= *[0-9]+/ { major = getnum($0); next}
      /^LIBMIKMOD_MINOR_VERSION *= *[0-9]+/ { minor = getnum($0); next}
      /^LIBMIKMOD_MICRO_VERSION *= *[0-9]+/ { micro = getnum($0); next}
      END { printf "%s %s %s", major, minor, micro }' \
      $1
    }

  export mikmod_version=(`mikmod_getver configure.in`)
  sed -e "s~@prefix@~$PREFIX~g" \
      -e "s~@exec_prefix@~$PREFIX~g" \
      -e "s~@LIBMIKMOD_VERSION@~${mikmod_version[0]}.${mikmod_version[1]}.${mikmod_version[2]}~g" \
      -e "s~@REENTRANT@~-D_REENTRANT~g" \
      -e "s~@LIB_LDADD@~~g" \
      -e "s~@LIBRARY_LIB@~-lpthread~g" \
      libmikmod-config.in >libmikmod-config

  # Enviroment variable expansion is used in writing the makefile...
  cat > win32/Makefile.static.mingw << THE_END
# MinGW Makefile adapted from template for use under win32
#
# libmikmod subdirectory

# Your compiler here
CC=gcc
# Compiler flags
CPPFLAGS_MIKMOD=-c -DWIN32 -DDRV_DS -DDRV_WIN -DHAVE_FCNTL_H -DHAVE_MALLOC_H -DHAVE_LIMITS_H \\$(CPPFLAGS)
COMPILE=\\$(CC) \\$(CPPFLAGS_MIKMOD) -I../include -I.. -I../win32 \\$(CFLAGS)

.SUFFIXES:
.SUFFIXES: .o .c

LIBNAME=libmikmod.a

LIBS=\\$(LIBNAME)

DRIVER_OBJ=drv_ds.o drv_win.o

OBJ=\\$(DRIVER_OBJ) \\
    drv_nos.o drv_raw.o drv_stdout.o drv_wav.o \\
    load_669.o load_amf.o load_dsm.o load_far.o load_gdm.o load_it.o  \\
    load_imf.o load_m15.o load_med.o load_mod.o load_mtm.o load_okt.o \\
    load_s3m.o load_stm.o load_stx.o load_ult.o load_uni.o load_xm.o \\
    mmalloc.o mmerror.o mmio.o \\
    mdriver.o mdreg.o mloader.o mlreg.o mlutil.o mplayer.o munitrk.o mwav.o \\
    npertab.o sloader.o virtch.o virtch2.o virtch_common.o

all:            \\$(LIBS)

clean:
\tfor f in \\$(LIBS) ; do rm -f $f; done
\trm -f *.o
\trm -f mikmod_build.h

distclean:
\trm -f ../include/mikmod.h

install:
\tcp -fp libmikmod.a "\\$(PREFIX)/lib"
\tcp -fp ../include/mikmod.h "\\$(PREFIX)/include"
\tcp -fp ../libmikmod-config "\\$(PREFIX)/bin"

\\$(LIBNAME):     \\$(OBJ)
\tar -r \\$(LIBNAME) *.o
\tranlib \\$(LIBNAME)

../include/mikmod.h ../win32/mikmod_build.h:\t../include/mikmod.h.in
\tsed -e "s~@LIBMIKMOD_MAJOR_VERSION@~${mikmod_version[0]}~" \\
\t    -e "s~@LIBMIKMOD_MINOR_VERSION@~${mikmod_version[1]}~" \\
\t    -e "s~@LIBMIKMOD_MICRO_VERSION@~${mikmod_version[2]}~" \\
\t    -e "s~@DOES_NOT_HAVE_SIGNED@~~" \\
\t    ../include/mikmod.h.in >../win32/mikmod_build.h
\tcp -f ../win32/mikmod_build.h ../include/mikmod.h

drv_ds.o:       ../drivers/drv_ds.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../drivers/drv_ds.c
drv_nos.o:      ../drivers/drv_nos.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../drivers/drv_nos.c
drv_raw.o:      ../drivers/drv_raw.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../drivers/drv_raw.c
drv_stdout.o:   ../drivers/drv_stdout.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../drivers/drv_stdout.c
drv_wav.o:      ../drivers/drv_wav.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../drivers/drv_wav.c
drv_win.o:       ../drivers/drv_win.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../drivers/drv_win.c
load_669.o:     ../loaders/load_669.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_669.c
load_amf.o:     ../loaders/load_amf.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_amf.c
load_dsm.o:     ../loaders/load_dsm.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_dsm.c
load_far.o:     ../loaders/load_far.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_far.c
load_gdm.o:     ../loaders/load_gdm.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_gdm.c
load_it.o:      ../loaders/load_it.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_it.c
load_imf.o:     ../loaders/load_imf.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_imf.c
load_m15.o:     ../loaders/load_m15.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_m15.c
load_med.o:     ../loaders/load_med.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_med.c
load_mod.o:     ../loaders/load_mod.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_mod.c
load_mtm.o:     ../loaders/load_mtm.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_mtm.c
load_okt.o:     ../loaders/load_okt.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_okt.c
load_s3m.o:     ../loaders/load_s3m.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_s3m.c
load_stm.o:     ../loaders/load_stm.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_stm.c
load_stx.o:     ../loaders/load_stx.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_stx.c
load_ult.o:     ../loaders/load_ult.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_ult.c
load_uni.o:     ../loaders/load_uni.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_uni.c
load_xm.o:      ../loaders/load_xm.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../loaders/load_xm.c
mmalloc.o:      ../mmio/mmalloc.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../mmio/mmalloc.c
mmerror.o:      ../mmio/mmerror.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../mmio/mmerror.c
mmio.o:         ../mmio/mmio.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../mmio/mmio.c
mdriver.o:      ../playercode/mdriver.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../playercode/mdriver.c
mdreg.o:        ../playercode/mdreg.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../playercode/mdreg.c
mloader.o:      ../playercode/mloader.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../playercode/mloader.c
mlreg.o:        ../playercode/mlreg.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../playercode/mlreg.c
mlutil.o:       ../playercode/mlutil.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../playercode/mlutil.c
mplayer.o:      ../playercode/mplayer.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../playercode/mplayer.c
munitrk.o:      ../playercode/munitrk.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../playercode/munitrk.c
mwav.o:         ../playercode/mwav.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../playercode/mwav.c
npertab.o:      ../playercode/npertab.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../playercode/npertab.c
sloader.o:      ../playercode/sloader.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../playercode/sloader.c
virtch.o:       ../playercode/virtch.c ../playercode/virtch_common.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../playercode/virtch.c
virtch2.o:      ../playercode/virtch2.c ../playercode/virtch_common.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../playercode/virtch2.c
virtch_common.o:        ../playercode/virtch_common.c \\
\t                ../win32/mikmod_build.h ../include/mikmod_internals.h
\t\\$(COMPILE) -o \\$@ ../playercode/virtch_common.c
THE_END

    unset -v mikmod_version
fi

if [ x$BDCOMP == x1 ]; then
  cd win32
  make -fMakefile.static.mingw \
       CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"

  cd ..
fi

if [ x$BDINST == x1 ]; then
  cd win32
  make install -fMakefile.static.mingw PREFIX="$PREFIX"
  cd ..
fi

if [[ x$BDCLEAN == x1 && -f Makefile ]]; then
  cd win32
  set +e
  make clean -fMakefile.static.mingw
  rm -f Makefile.static.mingw
  cd ..
  rm -f libmikmod-config
fi

"""),
    Dependency('MIXER', ['SDL_mixer-[1-9].*'], ['SDL_mixer.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

mikmod_dependencies='-ldsound'
flac_dependencies='-lWs2_32'

if [ x$BDCONF == x1 ]; then
  # If this came from SVN then need a configure script.
  if [ ! -f "./configure" ]; then
    ./autogen.sh
  fi

  mkdir -p ./pgbuild
  
  cd ./pgbuild
  # No dynamic loading of dependent libraries. Use LIBS so FLAC test
  # builds (unfortunately LIBS is not passed on to Makefile).
  export LIBS="$mikmod_dependencies $flac_dependencies"
  ../configure --disable-music-ogg-shared --disable-music-mp3-shared \
               --disable-music-mod-shared --disable-music-flac-shared \
               --disable-music-fluidsynth-midi --disable-static \
               --disable-libtool-lock --prefix="$PREFIX" \
               CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
  
  # check for MSYS permission errors
  if [ x"`grep 'Permission denied' config.log`" != x ]; then
      echo '**** MSYS problems; build aborted.'
      exit 1
  fi
  
  # ./configure messes up on its Makefile generation, putting some rules
  # on the same line as their targets, and placing multiple targets in one
  # line. Break them up. Also add the required FLAC and mikmod linkage flags.
  mv -f Makefile Makefile~
  sed -e 's~\\(-c $< -o $@\\) \\($(objects)\\)~\\1\\\n\\2~g' \
      -e 's~\\(\\.c\\)\\(\t$(LIBTOOL)\\)~\\1\\\n\\2~g' \
      -e 's~\\(: \\./version.rc\\)\\(\t$(WINDRES)\\)~\\1\\\n\\2~' \
      -e "s~\\(-lFLAC\\)~\\1 $flac_dependencies~" \
      -e "s~\\(-lmikmod\\)~\\1 $mikmod_dependencies~" \
      Makefile~ >Makefile
   
  cd ..
fi

if [ x$BDCOMP == x1 ]; then
  cd ./pgbuild
  # Only build the DLL. The executables link to WinMain, which is not found.
  make build/libSDL_mixer.la
  cd ..
fi

if [ x$BDINST == x1 ]; then
  cd ./pgbuild
  make install-hdrs install-lib
  cd ..
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/SDL_mixer.dll"
fi

if [[ x$BDCLEAN == x1 && -f Makefile ]]; then
  cd ./pgbuild
  set +e
  make clean
  cd ..
fi
"""),
    Dependency('PORTMIDI', ['portmidi', 'portmidi-[1-9].*'], ['portmidi.dll'], """

set -e
export PATH="$PREFIX/bin:$PATH"

if [ x$BDCONF == x1 ]; then
  # Fix up some g++ 4.5.0 issues in the source code.
  source_file=pm_common/portmidi.c
  if [ ! -f "$source_file~" ]; then
     mv "$source_file" "$source_file~"
     sed \
'420,+7s/return !Pm_QueueEmpty(midi->queue);/\
return Pm_QueueEmpty(midi->queue) ? pmNoData : pmGotData;/' \
         "$source_file~" >"$source_file"
  fi
  source_file=pm_win/pmwin.c
if [ ! -f "$source_file~" ]; then
     mv "$source_file" "$source_file~"
     sed \
-e '20,+6s/^\\(#include <windows.h>\\)/#include <ctype.h>\\\n\\1/' \
-e '91,+7s/if (RegQueryValueEx(hkey, key, NULL, &dwType, pattern, &pattern_max) !=/\
if (RegQueryValueEx(hkey, key, NULL, \\&dwType, (BYTE *) pattern, (DWORD *) \\&pattern_max) !=/' \
         "$source_file~" >"$source_file"
  fi
  source_file=pm_win/pmwinmm.c
  if [ ! -f "$source_file~" ]; then
     mv "$source_file" "$source_file~"
     sed \
-e '207,+7s/midi_out_caps = pm_alloc( sizeof(MIDIOUTCAPS) \\* midi_num_outputs );/\
midi_out_caps = (MIDIOUTCAPS *) pm_alloc( sizeof(MIDIOUTCAPS) * midi_num_outputs );/' \
-e '531,+10s/return pm_hosterror;/return pmInsufficientMemory;/' \
-e '531,+10s/return pm_hosterror;/return pm_hosterror ? pmInsufficientMemory : pmNoError;/' \
-e '626,+7s/return m->error;/return m->error == MMSYSERR_NOERROR ? pmNoError : pmHostError;/' \
-e '1206,+7s/midi->fill_offset_ptr = &(hdr->dwBytesRecorded);/\
midi->fill_offset_ptr = (uint32_t *) \\&(hdr->dwBytesRecorded);/' \
-e '1422,+7s/PmInternal \\* midi = descriptors\\[i\\]\\.internalDescriptor;/\
PmInternal * midi = (PmInternal *) descriptors[i].internalDescriptor;/' \
         "$source_file~" >"$source_file"
  fi

  cat > GNUmakefile << 'THE_END'
# Makefile for portmidi, generated for Pygame by msys_build_deps.py.

prefix = /usr/local

pmcom = pm_common
pmwin = pm_win
pt = porttime

pmdll = portmidi.dll
pmlib = libportmidi.a
pmimplib = libportmidi.dll.a
pmcomsrc = $(pmcom)/portmidi.c $(pmcom)/pmutil.c
pmwinsrc = $(pmwin)/pmwin.c $(pmwin)/pmwinmm.c
pmobj = portmidi.o pmutil.o pmwin.o pmwinmm.o
pmsrc = $(pmcomsrc) $(pmwinsrc)
pmreqhdr = $(pmcom)/portmidi.h $(pmcom)/pmutil.h
pmhdr = $(pmreqhdr) $(pmcom)/pminternal.h $(pmwin)/pmwinmm.h

ptsrc = $(pt)/porttime.c porttime/ptwinmm.c
ptobj = porttime.o ptwinmm.o
ptreqhdr = $(pt)/porttime.h
pthdr = $(ptreqhdr)

src = $(pmsrc) $(ptsrc)
reqhdr = $(pmreqhdr) $(ptreqhdr)
hdr = $(pmhdr) $(pthdr)
obj = $(pmobj) $(ptobj)
def = portmidi.def

IHDR := -I$(pmcom) -I$(pmwin) -I$(pt)
LIBS := $(LOADLIBES) $(LDLIBS) -lwinmm



all : $(pmdll)
.PHONY : all

$(pmlib) : $(src) $(hdr)
\tg++ $(CPPFLAGS) $(IHDR) -c $(CFLAGS) $(src)
\tar rc $(pmlib) $(obj)
\tranlib $(pmlib)

$(pmdll) : $(pmlib) $(def)
\tg++ -shared -static-libgcc $(LDFLAGS) -def $(def) $(pmlib) $(LIBS) -o $@
\tdlltool -D $(pmdll) -d $(def) -l $(pmimplib)
\tranlib $(pmimplib)

.PHONY : install

install : $(pmdll)
\tcp -f --target-directory=$(PREFIX)/bin $<
\tcp -f --target-directory=$(PREFIX)/lib $(pmlib)
\tcp -f --target-directory=$(PREFIX)/lib $(pmimplib)
\tcp -f --target-directory=$(PREFIX)/include $(reqhdr)

.PHONY : clean

clean :
\trm -f $(obj) $(pmdll) $(pmimplib) $(pmlib)
THE_END

  cat > portmidi.def << 'THE_END'
LIBRARY portmidi.dll
EXPORTS
Pm_Abort
Pm_Close
Pm_CountDevices
Pm_Dequeue
Pm_Enqueue
Pm_GetDefaultInputDeviceID
Pm_GetDefaultOutputDeviceID
Pm_GetDeviceInfo
Pm_GetErrorText
Pm_GetHostErrorText
Pm_HasHostError
Pm_Initialize
Pm_OpenInput
Pm_OpenOutput
Pm_Poll
Pm_QueueCreate
Pm_QueueDestroy
Pm_QueueEmpty
Pm_QueueFull
Pm_QueuePeek
Pm_Read
Pm_SetChannelMask
Pm_SetFilter
Pm_SetOverflow
Pm_Terminate
Pm_Write
Pm_WriteShort
Pm_WriteSysEx
Pt_Sleep
Pt_Start
Pt_Started
Pt_Stop
Pt_Time
THE_END

fi

if [ x$BDCOMP == x1 ]; then
  make CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
fi

if [ x$BDINST == x1 ]; then
  make install PREFIX="$PREFIX"
fi

if [ x$BDSTRIP == x1 ]; then
  strip --strip-all "$PREFIX/bin/portmidi.dll"
fi

if [[ x$BDCLEAN == x1 && -f Makefile ]]; then
  set +e
  make clean
  rm -f GNUmakefile portmidi.def
fi
"""),
    
    ]  # End dependencies = [.


msys_prep = Preparation('destintation directory', """

# Ensure the destination directory and its subdirectories exist.
mkdir -p "$PREFIX/lib"
mkdir -p "$PREFIX/include"
mkdir -p "$PREFIX/bin"
mkdir -p "$PREFIX/doc"
mkdir -p "$PREFIX/man"
mkdir -p "$PREFIX/share"
""")

alert = Preparation('computer beeper', r"""

#
# Alert the user by beeping the computer speaker
#
if [ x"$BDNTIMES" == x ]; then
  BDNTIMES=1
fi

for (( i = $BDNTIMES ; i ; i-- )); do
    printf $'\a\a\a\a\a'
    sleep 1s
done
""")

if __name__ == '__main__':
    sys.exit(main(dependencies, msys_prep))
