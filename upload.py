import os
import shutil

try:
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
finally:
    shutil.rmtree(os.path.join(os.path.dirname(__file__), 'build'))
    shutil.rmtree(os.path.join(os.path.dirname(__file__), 'dist'))
    shutil.rmtree(os.path.join(os.path.dirname(__file__), 'ebbinghaus.egg-info'))
