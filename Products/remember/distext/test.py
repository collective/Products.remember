from distutils.cmd import Command
from utils import useBuildPath, getBuildPath
import os, sys

class TestCommand(Command):
    """Command to run unit tests after installation"""

    description = "run unit tests after installation"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # build and use the just built lib
        self.run_command('build')
        useBuildPath()

        base_pkg = self.distribution.packages[0]

        self.announce('running unittest for %s' % base_pkg)

        # Change into the build tests directory
        old_path = os.getcwd()
        os.chdir(os.path.join(getBuildPath(),
                              base_pkg,
                              "tests"))
        # make sure we can import these tests which currently
        # do a scan of cwd
        sys.path.insert(0, '.')

        # import the module and invoke its main()
        m = __import__("tests.runalltests",
                   globals(), globals(), ['runalltests'])
        m.main()
        os.chdir(old_path)


