# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches v3 Scrapers
# Addon id: script.module.fuzzybritchesv3scrapers
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''

from functools import reduce
import re


class UnpackingError(Exception):
    """Badly packed source or general error. Argument is a
    meaningful description."""
    pass


def detect(source):
    """Detects whether `source` is H.U.N.T.E.R. coded."""
    source = source.replace(' ', '')
    if re.search(r'eval\(function\(h,u,n,t,e,r', source):
        return True
    else:
        return False


def _dehunt(d, e, f):
    g = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"
    h = g[0:e]
    i = g[0:f]
    d = d[::-1]
    j = reduce(lambda a, b: a + int(h[int(b[1])]) * (e ** int(b[0])) if int(h[int(b[1])]) != -1 else None, enumerate(d), 0)
    k = ""
    while j > 0:
        k = i[int(j % f)] + k
        j = (j - (j % f)) / f

    return k or "0"


def _jsunhunter(h, n, t, e):
    r = ""
    i = 0
    while i < len(h):
        s = ""
        while h[i] != n[e]:
            s += h[i]
            i += 1

        for j in enumerate(n):
            s = s.replace(j[1], str(j[0]))

        r += chr(int(_dehunt(s, e, 10)) - t)
        i += 1

    return r


def _filterargs(source):
    """Juice from a source file the four args needed by decoder."""
    argsregex = r'\(h,\s*u,\s*n,\s*t,\s*e,\s*r\).+}\("([^"]+)",[^,]+,\s*"([^"]+)",\s*(\d+),\s*(\d+)'
    try:
        payload, n, t, e = re.search(argsregex, source, re.DOTALL).groups()
        return payload, n, int(t), int(e)
    except AttributeError:
        raise UnpackingError('Corrupted h.u.n.t.e.r. data.')


def unhunt(source):
    payload, n, t, e = _filterargs(source)
    return _jsunhunter(payload, n, t, e)


if __name__ == "__main__":
    test = '''eval(function(h, u, n, t, e, r) {r = "";for (var i = 0, len = h.length; i < len; i++) {var s = "";while (h[i] !== n[e]) {s += h[i];i++}for (var j = 0; j < n.length; j++) s = s.replace(new RegExp(n[j], "g"), j);console.log(_0xe41c(s, e, 10) - t);r += String.fromCharCode(_0xe41c(s, e, 10) - t)}}("jjMErrQEryyEriQErrrEryiErimEriOEriQEjjMErrQEriOEryjEriyErrmEryyEryiErrMEryyEryjEriiEjrMErriErrmEryiErrmEjimEjjMErQrEjjMEryjErryEryiEryyEryjEriQEjjMEryOErimEriQErriEriOEryOEjiQErrmEryiEriOErrjEjrMErirErryErQmErmyEryjEriiEjimEjjMEjirEjjMEjrOEjQOEryrEryiEryjErryErrmEriyEjQyEjrOEjjMEjirEjjMEryrEryiEryjEjMQErrmEriyErryEjjMEjirEjjMEjrOEjrQEryrErrrEriOErriErryEjQyEjrOEjjMEjirEjjMErriErrmEryiErrmEjiQEryrErrrEriOErriErryEjjMEjirEjjMEjrOEjrQErryEryMEriMErimEryjErryEryrEjQyEjrOEjjMEjirEjjMErriErrmEryiErrmEjiQEryiEryrEjQrEjjMErQyEjjMErrQEryyEriQErrrEryiErimEriOEriQEjjMErrmEryyEryiErrMErrrErrMErryErrrErirEjrMEjimEjjMErQrEjjMErimErrQEjjMEjrMEryOErimEriQErriEriOEryOEjiQEriMErryErryEryjEjyyEjimEjjMErQrEjjMEjriEjiQErrmErijErrmEryMEjrMErQrEjjMEryyEryjEriiEjQjEjjMErrmEryyEryiErrMErmyEryjEriiEjiiEjjMEryMErrMEryjEjOQErimErryEriiErriEryrEjQjEjjMErQrEjjMEryOErimEryiErrMEjOrEryjErryErriErryEriQEryiErimErrmEriiEryrEjQjEjjMEryiEryjEryyErryEjjMErQyEjiiEjjMEryrEryyErrrErrrErryEryrEryrEjQjEjjMErrQEryyEriQErrrEryiErimEriOEriQEjjMEjrMEryjErryEryrEriMEriOEriQEryrErryEjimEjjMErQrEjjMErrmEryyEryiErrMErmyEryjEriiEjjMEjQyEjjMErrQEriOEryjEriyErrmEryyEryiErrMEryyEryjEriiEjrMEryjErryEryrEriMEriOEriQEryrErryEjimEjQrEjjMEryrErryEryiErmiErimEriyErryEriOEryyEryiEjrMErrmEryyEryiErrMErrrErrMErryErrrErirEjiiEjjMEjyyEjjMEjijEjjMEjyQEjiMEjjMEjijEjjMEjymEjiMEjiMEjiMEjimEjQrEjjMErQyEjiiEjjMErryEryjEryjEriOEryjEjQjEjjMErrQEryyEriQErrrEryiErimEriOEriQEjjMEjrMEjimEjjMErQrEjjMErimErrQEjjMEjrMErrQErrmErimEriiEjOrEriOEryyEriQEryiEjjMEjQiEjjMEjyrEjimEjjMErQrEjjMEryrErryEryiErmiErimEriyErryEriOEryyEryiEjrMErrmEryyEryiErrMErrrErrMErryErrrErirEjiiEjjMEjyyEjiMEjiMEjiMEjimEjQrEjjMErrQErrmErimEriiEjOrEriOEryyEriQEryiEjirEjirEjQrEjjMErQyEjjMErryEriiEryrErryEjjMErQrEjjMEryrEryiEriOEriMEriMEriiErrmErQmErryEryjEjrMEjimEjQrEjjMErQyEjjMErQyEjjMErQyEjimEjQrEjjMErQyEjjMErQyEjjMErrQEryyEriQErrrEryiErimEriOEriQEjjMEriMErryErryEryjErrrErrMErryErrrErirEjrMEjimEjjMErQrEjjMEryQErrmEryjEjjMEriMErmrEryiEryrEjjMEjQyEjjMEriMErryErryEryjEjyyEjiQErrOErryEryiErmrEryiErrmEryiEryrEjrMEjimEjQrEjjMErimErrQEjjMEjrMEriMErmrEryiEryrEjiQEryiEriOEryiErrmEriiEjOMEryiEryiEriMEjOiEriOEryOEriQEriiEriOErrmErriErryErriEjjMEjQyEjQyEjQyEjjMEjiMEjjMEjrQEjrQEjjMEriMErmrEryiEryrEjiQEryiEriOEryiErrmEriiEjMMEjyjEjMMEjOiEriOEryOEriQEriiEriOErrmErriErryErriEjjMEjQyEjQyEjQyEjjMEjiMEjimEjjMErQrEjjMEryrEryiEriOEriMEriMEriiErrmErQmErryEryjEjrMEjimEjQrEjjMErQyEjjMErQyEjjMErrQEryyEriQErrrEryiErimEriOEriQEjjMEryrEryiEriOEriMEriMEriiErrmErQmErryEryjEjrMEjimEjjMErQrEjjMEriMEriiErrmErQmErryEryjEjMOErrjErijEjiQEryrEryiEriOEriMEjrMEjimEjQrEjjMEriMEriiErrmErQmErryEryjEjMOErrjErijEjiQEryjErryEriyEriOEryQErryEjrMEjimEjQrEjjMErrmEryyEryiErrMErmyEryjEriiEjjMEjQyEjjMEjrOEjrOEjQrEjjMErQyEjjMErrrEriOEriQEryrEryiEjjMErirErryErQmErmyEryjEriiEjjMEjQyEjjMEjrOErrmEjOMErmjEjiMErrrEjOMEjMyEjyQEjMiErQmEjQmErrMErriErmMErmjEriOErrjErmOErmyEryyErrrEjyjErmQErijErrmEjyjErmQEjyyErrrEjyjErmQErQmErriErimEjyyEryiErjjErmmEjQyEjQyEjrOEjQrEjjMErrrEriOEriQEryrEryiEjjMEriMEriiErrmErQmErryEryjEjMmErriEjjMEjQyEjjMEjrOEriQEryjErmOEjOQErrMEryyEjMrErrQEjMOErmyErmQErymEjMyErjmEryrEriOEriyEjOjEjrOEjQrEjjMErrrEriOEriQEryrEryiEjjMEryrEryiEryjEjMQErrmEriyErryEjjMEjQyEjjMEjrOErirEriiEjMmErimErQjEriyEjyQEryyEjMyEjyjErrOEjymErmyEjyyEjyOErrQEjOMEjOiEjMjEjOrEjrOEjQrEjjMEriiErryEryiEjjMErrmEryyEryiErrMErmyEryjEriiEjjMEjQyEjjMEjrOEjOrEryrErirErmrErmOEjOOErmmEjMiEjOjEjOyEjOiErrOEjOMErrmErrMEjOQErmyEjMjEriiEjMOErimEjrOEjQrEjjMErrrEriOEriQEryrEryiEjjMEryrEriOEryyEryjErryErmyEryjEriiEjjMEjQyEjjMEjrOErrmEjOMErmjEjiMErrrEjOMEjMyEjyQEjMiErQmEjQmEriiEjMyErmrEjyyErirErrjEjyrErmjEriMErjmEjyjErmyEryyErrjErmOErmyEryQErryEriyEjymEriiErrjEjOOEriiEjyjErjjErmrEjQmEryjErrjEjOyEriiEriMErryEriyEjiMEjyjErriErmyEjiMErQmErjjErQjEjOQErmQEjMQErmiErriEriyErmrEjOyErmjEjMrErmmErQmEjQmEryOErrjEjOOEjOQEjyyErrjEjOOEriiErQjErriEjOrEjyyEryiEjMyEjyrErmyEjyiEjrOEjQrEjjMErrrEriOEriQEryrEryiEjjMErirErryEriiErmQErrmEriiEjjMEjQyEjjMEjrOErrmErrMErmiEjMrErrOErmyEriOErimEriiErriEjOMEjrOEjQrEjjMErrrEriOEriQEryrEryiEjjMErijEryOErrjErrmEryrErryEriMErrmEryiErrMEjjMEjQyEjjMEjrOErrMEryiEryiEriMEryrEjQjEjiOEjiOEryrEryiEryrEjiQErirEryyEriQEryiEryQEjiQEriMEryOEjiOEriMEriiErrmErQmErryEryjEjiOEjyMEjiQEjymEjymEjiQEjyMEjiOEjrOEjQrEjjMEriiErryEryiEjjMEriMEriiErrmErQmErryEryjEjMOErrjErijEjQrEjjMErrmEryyEryiErrMErmyEryjEriiEjjMEjQyEjjMErrQEriOEryjEriyErrmEryyEryiErrMEryyEryjEriiEjrMErQrEjrjEryrErrrEriOErriErryEjrjEjQjEjjMEjrjErmQErrrErirErjjErryEjMmErymErjOErrrEriyErriEriQEjMMEjMmEriOEryyErmjErrrEriyEjMrEjiyEjOmEjrjEjiiEjjMEjrjEryiEryrEjrjEjQjEjjMEjymEjyyEjyOEjyyEjyrEjyyEjQmEjyQEjyOEjyOErQyEjimEjQrEjjMEriiErryEryiEjjMErrQErrmErimEriiEjOrEriOEryyEriQEryiEjjMEjQyEjjMEjiMEjQrEjjMErrmEryyEryiErrMErrrErrMErryErrrErirEjrMEjimEjQrEjjMErrrEriOEriQEryrEryiEjjMEryjErrmEryiErimEriOEjjMEjQyEjjMEjriEjrMEryOErimEriQErriEriOEryOEjimEjiQEryOErimErriEryiErrMEjrMEjimEjjMEjiOEjjMEjriEjrMEryOErimEriQErriEriOEryOEjimEjiQErrMErryErimErrOErrMEryiEjrMEjimEjQrEjjMEriiErryEryiEjjMErrmEryrEriMErryErrrEryiErmjErrmEryiErimEriOEjjMEjQyEjjMEjrOEjymEjyQEjQjEjQmEjrOEjQrEjjMErimErrQEjjMEjrMEryjErrmEryiErimEriOEjjMEjQiEjjMEjymEjiQEjyyEjimEjjMErQrEjjMErrmEryrEriMErryErrrEryiErmjErrmEryiErimEriOEjjMEjQyEjjMEjrOEjyiEjQjEjyrEjrOEjQrEjjMErQyEjjMEriMEriiErrmErQmErryEryjEjMOErrjErijEjjMEjQyEjjMErijEryOEriMEriiErrmErQmErryEryjEjrMEriMEriiErrmErQmErryEryjEjMmErriEjimEjQrEjjMEriMEriiErrmErQmErryEryjEjMOErrjErijEjiQEryrErryEryiEryyEriMEjrMErQrEjjMErrQErimEriiErryEjQjEjjMEryOErimEriQErriEriOEryOEjiQErrmEryiEriOErrjEjrMEryrEriOEryyEryjErryErmyEryjEriiEjimEjiiEjjMErrrEriOEriQEryiEryjEriOEriiEryrEjQjEjjMEryiEryjEryyErryEjiiEjjMErrmEryyEryiEriOEryrEryiErrmEryjEryiEjQjEjjMErrQErrmEriiEryrErryEjiiEjjMEriyEryyEryiErryEjQjEjjMErrQErrmEriiEryrErryEjiiEjjMErrMEriiEryrErrMEryiEriyEriiEjQjEjjMEryiEryjEryyErryEjiiEjjMErimEriyErrmErrOErryEjQjEjjMEjrOErrMEryiEryiEriMEryrEjQjEjiOEjiOEryjErrrEriiEjiQErirEryyEriQEryiEryQEjiQEriMEryOEjiOEryiErrMEryyEriyErrjEjiOErirEriiEjMmErimErQjEriyEjyQEryyEjMyEjyjErrOEjymErmyEjyyEjyOErrQEjOMEjOiEjMjEjOrEjiQErijEriMErryErrOEjrOEjiiEjjMErrmEryrEriMErryErrrEryiEryjErrmEryiErimEriOEjQjEjjMErrmEryrEriMErryErrrEryiErmjErrmEryiErimEriOEjiiEjjMEryOErimErriEryiErrMEjQjEjjMEjrOEjymEjiMEjiMEjryEjrOEjiiEjjMEryiErQmEriMErryEjQjEjjMEjrOErrMEriiEryrEjrOEjiiEjjMErrmEriQErriEryjEriOErimErriErrMEriiEryrEjQjEjjMEryiEryjEryyErryEjiiEjjMErirErryErQmEjQjEjjMErirErryEriiErmQErrmEriiEjiiEjjMEriMEryjErimEriyErrmEryjErQmEjQjEjjMEjrOErrMEryiEriyEriiEjyyEjrOEjiiEjjMEriMEryjErryEriiEriOErrmErriEjQjEjjMEjrOErrmEryyEryiEriOEjrOEjiiEjjMErrMEriiEryrErijEryrErriErryErrQErrmEryyEriiEryiEjQjEjjMEryiEryjEryyErryEjiiEjjMEryOErimEryiErrMEjOrEryjErryErriErryEriQEryiErimErrmEriiEryrEjQjEjjMEryiEryjEryyErryEjiiEjjMEriiErimEryQErryErmiErimEriyErryEriOEryyEryiEjQjEjjMEjymEjymEjiiEjjMErrrErrmEryrEryiEjQjEjjMErQrErQyEjiiEjjMErrjErrmEryrErryEjQjEjjMErijEryOErrjErrmEryrErryEriMErrmEryiErrMEjjMErQyEjimEjQrEjjMEriMEriiErrmErQmErryEryjEjMOErrjErijEjiQEriOEriQEjrMEjrOEriMEriiErrmErQmEjrOEjiiEjjMErrQEryyEriQErrrEryiErimEriOEriQEjjMEjrMErryEjimEjjMErQrEjjMEriMEriiErrmErQmErryEryjEjMOErrjErijEjiQEryrErryEryiEjMyEryyEryiErryEjrMErrQErrmEriiEryrErryEjimEjQrEjjMEjriEjrMEjrjEjiQErijEryOEjiyErriErimEryrEriMEriiErrmErQmEjiyErrrEriOEriQEryiEryjEriOEriiEryrEjjMEjiQErijEryOEjiyEryjErryEryrErryEryiEjrjEjimEjiQErrrEryrEryrEjrMEjrjErrjErrmErrrErirErrOEryjEriOEryyEriQErriEjiyErrrEriOEriiEriOEryjEjrjEjiiEjjMEjrjEryiEryjErrmEriQEryrEriMErrmEryjErryEriQEryiEjrjEjimEjQrEjjMEryrErryEryiEjMmEriQEryiErryEryjEryQErrmEriiEjrMEriMErryErryEryjErrrErrMErryErrrErirEjiiEjjMEjymEjyyEjjMEjijEjjMEjymEjiMEjiMEjiMEjimEjQrEjjMErQyEjimEjQrEjjMEriMEriiErrmErQmErryEryjEjMOErrjErijEjiQEriOEriQEjrMEjrOErryEryjEryjEriOEryjEjrOEjiiEjjMErrQEryyEriQErrrEryiErimEriOEriQEjjMEjrMEjimEjjMErQrEjjMErrmEriiErryEryjEryiEjrMEjrjErryEryjEryjEriOEryjEjjMEriMEriiErrmErQmEjrjEjimEjQrEjjMEryrEryiEriOEriMEriMEriiErrmErQmErryEryjEjrMEjimEjQrEjjMErQyEjimEjQrEjjMEryrErryEryiErmiErimEriyErryEriOEryyEryiEjrMErrQEryyEriQErrrEryiErimEriOEriQEjjMEjrMEjimEjjMErQrEjjMEryrEryiEriOEriMEriMEriiErrmErQmErryEryjEjrMEjimEjQrEjjMErQyEjiiEjjMEjyrEjjMEjijEjjMEjyQEjiMEjjMEjijEjjMEjyQEjiMEjjMEjijEjjMEjymEjiMEjiMEjiMEjimEjQrEMjE", 62, "mjriyQOME", 47, 8, 56))'''
    if detect(test):
        print(unhunt(test))
