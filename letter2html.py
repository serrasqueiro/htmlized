# letter2html.py -- (c)2019, 2021 Henrique Moreira
"""
  letter2html.py - simple Python functions to convert text to HTML
"""

import sys

# pylint: disable=missing-function-docstring, line-too-long


TRANSLATE = {
    0xc0:'&Agrave;', 0xc1:'&Aacute;', 0xc2:'&Acirc;', 0xc3:'&Atilde;', 0xc4:'&Auml;', 0xc5:'&Aring;',
    0xc6:'Ae', 0xc7:'&Ccedil;',
    0xc8:'&Egrave;', 0xc9:'&Eacute;', 0xca:'E', 0xcb:'E',
    0xcc:'&Igrave;', 0xcd:'&Iacute;', 0xce:'I', 0xcf:'I',
    0xd0:'Th', 0xd1:'N',
    0xd2:'&Ograve;', 0xd3:'&Oacute;', 0xd4:'O', 0xd5:'O', 0xd6:'O', 0xd8:'O',
    0xd9:'&Ugrave;', 0xda:'&Ugrave;', 0xdb:'U', 0xdc:'U',
    0xdd:'Y', 0xde:'th', 0xdf:'ss',
    0xe0:'&agrave;', 0xe1:'&aacute;', 0xe2:'&acirc;', 0xe3:'&atilde;', 0xe4:'&auml;', 0xe5:'&aring;',
    0xe6:'ae', 0xe7:'c',
    0xe8:'&egrave;', 0xe9:'&eacute;', 0xea:'e', 0xeb:'e',
    0xec:'&igrave;', 0xed:'&iacute;', 0xee:'i', 0xef:'i',
    0xf0:'th', 0xf1:'n',
    0xf2:'&ograve;', 0xf3:'&oacute;', 0xf4:'o', 0xf5:'o', 0xf6:'o', 0xf8:'o',
    0xf9:'&ugrave;', 0xfa:'&uacute;', 0xfb:'u', 0xfc:'u',
    0xfd:'y', 0xfe:'th', 0xff:'y',
    0xa1:'!', 0xa2:'{cent}', 0xa3:'{pound}', 0xa4:'{currency}',
    0xa5:'&yen;',
    0xa6:'|', # broken bar
    0xa7:'{section}', 0xa8:'{umlaut}',
    0xa9:'&copy;', 0xaa:'{^a}', 0xab:'<<', 0xac:'&not;',
    0xad:'-', 0xae:'{R}', 0xaf:'_', 0xb0:'{degrees}',
    0xb1:'{+/-}', 0xb2:'{^2}', 0xb3:'{^3}', 0xb4:"'",
    0xb5:'{micro}', 0xb6:'{paragraph}', 0xb7:'*',
    0xb8:'&ccedil;',
    0xb9:'{^1}', 0xba:'{^o}', 0xbb:'>>',
    0xbc:'{1/4}', 0xbd:'{1/2}', 0xbe:'{3/4}',
    0xbf:'?', # inverted question mark
    0xd7:'*', # multiplication sign
    0xf7:'/', # division sign
}


def main():
    """ Main tests """
    out = sys.stdout
    code = test_letter2html(out, sys.argv[1:])
    sys.exit(code)


def test_letter2html(out, args) -> int:
    """ Main testing function """
    enc_decode = "ISO-8859-1"
    assert translate_table.n_converts > 0
    tbl = TranslateTable(debug=1)
    assert tbl
    if not args:
        return 0
    print("###\n")
    for fname in args:
        data = open(fname, "r", encoding=enc_decode).read()
        astr = latin1_to_html(data)
        print(f"{fname}:", fname)
        print(astr)
    return 0


class TranslateTable():
    """ Translate to HTML class """
    def __init__ (self, debug=0):
        xlate = TRANSLATE
        self.xlate = xlate
        self.n_converts = len(xlate)
        self.hash_conversions(debug, relate=xlate)


    def hash_conversions(self, debug, **kvars) -> bool:
        if debug <= 0:
            return True
        if debug >= 2:
            for a_key, val in kvars.items():
                print( "key: <b>{}</b>".format(a_key), "is: <pre>", val ,"</pre>\n")
                print("<hr>")
        self._dump_convs(kvars["relate"])
        return True

    def _dump_convs(self, dig_conv):
        # pylint: disable=no-self-use, invalid-name
        used = [0] * 256
        url = "https://www.fileformat.info/info/unicode/char/"

        def hint_str (info, k):
            hint = "<a {} href='{}{:04x}/index.htm'>{}</a>".format("target='_blank'", url, k, info)
            return hint

        for kind in ["&", ""]:
            for k, html in dig_conv.items():
                assert html
                first = html[ 0 ].lower()
                if used[ k ] > 0:
                    continue
                bas = "k: 0x{:02x}".format(k) + " " + hint_str("{:d}d".format(k), k)
                if kind=="":
                    show = html.replace("<", "&lt;").replace(">", "&gt;")
                    print(bas, "; html is:", show, "<BR/>")
                    used[ k ] += 1
                else:
                    if html.find(kind) == 0:
                        print(bas, "; html string is:", html, "<BR/>")
                        used[ k ] += 1
                        if first=="&":
                            isOk = html.endswith(";")
                            assert isOk, f"Uops: {html}"
        k = 0x7f
        while True:
            k += 1
            if k >= 256:
                break
            if k == 0xa0:
                print("<hr>Now ASCII after 0xA0 (160d)<br>")
            if used[ k ] <= 0:
                hint = hint_str("info", k)
                print("<p>unused k:", "0x{:02x} #{:03};".format(k, k), hint, "</p>")
        return True


def latin1_to_html(astr:str) -> str:
    """This takes a UNICODE string and replaces Latin-1 characters with
      something equivalent in html. It returns a plain ASCII string.
      This function makes a best effort to convert Latin-1 characters into
      ASCII equivalents. It does not just strip out the Latin-1 characters.
      All characters in the standard 7-bit ASCII range are preserved.
      In the 8th bit range all the Latin-1 accented letters are converted
      to unaccented equivalents. Most symbol characters are converted to
      something meaningful. Anything not converted is deleted.
    """
    result = ""
    for achr in astr:
        idx = ord(achr)
        this = translate_table.xlate.get(idx)
        if this:
            result += this
        elif idx >= 0x80:
            pass
        else:
            result += achr
    return result


#
# Global / singletons
#
translate_table = TranslateTable()


#
# Test suite
#
if __name__ == "__main__":
    main()
