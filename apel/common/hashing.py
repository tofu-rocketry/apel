'''
   Copyright 2012 Konrad Jopek

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
# hashlib only available in python2.5+
try:
    from hashlib import md5
except ImportError:
    from md5 import md5
import gzip
import bz2


def calculate_hash(fname):
    '''
    Calculates MD5 hash from content of file with name='fname'.  Also opens gzip
    files.

    Used in parsers to avoid double parsing of files.
    For sample usage please go to: apel2/bin/client.py
    '''

    data = b'initial'

    md = md5()

    # try to open as a bzip2 file, then as a gzip file,
    # and if it fails try as a regular file
    #
    # bz2/gzip doesn't raise an exception when trying
    # to open a non-gzip file.  Only a read (such as
    # during parsing) does that.  For files of a wrong
    # format we will get IOError, empty files can
    # give EOFError as well.
    for method in (bz2.BZ2File, gzip.open, open):
        try:
            fp = method(fname, 'rb')
            while data != b'':
                # 128kiB buffer
                data = fp.read(131072)
                md.update(data)
            break
        except (IOError, EOFError):
            if method == open:
                # Something has gone wrong if we fail to open as a normal file.
                raise

    fp.close()
    return md.hexdigest()
