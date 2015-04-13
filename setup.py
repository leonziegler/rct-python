from setuptools import setup, find_packages
import os

# Determine version
version_file = os.path.realpath(__file__)
version_file = os.path.join(version_file[:version_file.rfind("/")], "VERSION")
version = open(version_file).read().strip()

cfg_folder = "configuration"

print "installing packages:", find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

setup(name="rct-python",
      version=version,
      description="Robotics Coordinate Transform (Python).",
      long_description="This library wraps the functionality of the tf2 library from ROS and supports communication over the RSB middleware.",
      author = "Norman Koester",
      author_email = "nkoester[at]techfak.uni-bielefeld.de",
      url="TODO",
      download_url="TODO",
      # scripts = ["bin/ltm-core-py",],
      # installs config files
      # data_files=[('configuration', [ cfg_folder+"/"+f for f in listdir(cfg_folder) if isfile(join(cfg_folder,f)) ]),],
      packages = find_packages(exclude = ["*.tests", "*.tests.*", "tests.*", "tests"]),
      include_package_data = True,
      keywords=['transformation', 'coordinates', 'tf', 'tf2'],
      license = "LGPLv3",
      classifiers = [
          'Development Status :: Beta',
          'Environment :: Console',
          'Environment :: Robotics/Cognitive Systems',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: Linux',
          'Programming Language :: Python',
          'Topic :: Text Processing :: Markup :: XML'
      ],
      # 'Louie', 'suds', 'restlib',
      install_requires = ['nose', 'coverage',
                        'nosexcover', 'pylint', 'setuptools-lint',
                        "rsb-python>=0.11", "rstconverters==0.11"])

# Make the scripts executable for Unit Testing
# subprocess.call(["chmod -R ugo+x bin"], shell = True)

