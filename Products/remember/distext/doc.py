from distutils.cmd import Command
from utils import useBuildPath, getBuildPath
import os, sys

class DocCommand(Command):
    """Command to build the documentation associated with a project"""

    description =     """Command to build the documentation associated with a project"""

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # make sure the tests pass and we can use the build dir to
        # generate docs
        #self.run_command('test')
        useBuildPath()

        base_pkg = self.distribution.packages[0]
        self.announce('building docs %s' % base_pkg)

        base_dir = os.path.join(getBuildPath(), base_pkg)

        doc_dir = os.path.join(os.getcwd(), "docs")
        os.system("epydoc -qq --pdf --inheritance listed -n %s -o %s %s &> /dev/null" % (base_pkg,
                                                                                         doc_dir,
                                                                                         base_dir))

        self.announce("documentation built")
