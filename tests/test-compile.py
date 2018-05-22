import unittest, sys, os, shutil
from setup import downloadSource
sys.path.append("..")

module = __import__('hv-compile')

srcPath = "src"
dstPath = "out"
name    = "metro"
libName = "libmetro." + ("so", "a")[sys.platform == "darwin"]

class CompileTestCase(unittest.TestCase):
  """Tests for `hv-compile`"""

  @classmethod
  def tearDownClass(cls):
    print("Cleaning Up")
    shutil.rmtree(dstPath)

  def testSourceExists(self):
    """Return True if Heavy source exists."""
    self.assertTrue(os.path.exists(srcPath))

  def testStaticLibraryIsGenerated(self):
    """Return True if static library is generated."""
    module.compileSource(srcPath, name, dstPath)
    self.assertTrue(os.path.exists(os.path.join(dstPath,libName)))

if __name__ == '__main__':
  if not os.path.exists(srcPath):
    print("Downloading test source files")
    downloadSource() # TODO: Error if fails

  unittest.main()