# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/common/Lib/plat-mac/lib-scriptpackages/Netscape/Standard_URL_suite.py
"""Suite Standard URL suite: Mac URL standard, supported by many apps


Level 1, version 1

Generated from /Volumes/Sap/Applications (Mac OS 9)/Netscape Communicator\xe2\x84\xa2 Folder/Netscape Communicator\xe2\x84\xa2
AETE/AEUT resource version 1/0, language 0, script 0
"""
import aetools
import MacOS
_code = 'GURL'

class Standard_URL_suite_Events:
    _argmap_GetURL = {'to': 'dest',
     'inside': 'HWIN',
     'from_': 'refe'}

    def GetURL(self, _object, _attributes={}, **_arguments):
        """GetURL: Loads the URL (optionally to disk)
        Required argument: The url
        Keyword argument to: file the URL should be loaded into
        Keyword argument inside: Window the URL should be loaded to
        Keyword argument from_: Referrer, to be sent with the HTTP request
        Keyword argument _attributes: AppleEvent attribute dictionary
        """
        _code = 'GURL'
        _subcode = 'GURL'
        aetools.keysubst(_arguments, self._argmap_GetURL)
        _arguments['----'] = _object
        _reply, _arguments, _attributes = self.send(_code, _subcode, _arguments, _attributes)
        if _arguments.get('errn', 0):
            raise aetools.Error, aetools.decodeerror(_arguments)
        return _arguments['----'] if _arguments.has_key('----') else None


_classdeclarations = {}
_propdeclarations = {}
_compdeclarations = {}
_enumdeclarations = {}