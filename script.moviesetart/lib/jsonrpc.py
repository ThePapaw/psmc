# -*- coding: utf-8 -*-

import os
import sys
import urllib

try:
    import json as simplejson
    # test json has not loads, call error
    if not hasattr( simplejson, "loads" ):
        raise Exception( "Hmmm! Error with json %r" % dir( simplejson ) )
except Exception, e:
    print "[MovieSetArt] %s" % str( e )
    import simplejson
# for fun! :) json use speedup
if simplejson.decoder.c_scanstring is not None:
    print "[MovieSets] Yes, json use speedup :)"

try:
    import xbmc
except:
    #we're not in XBMC so we only get http
    xbmc = None


class UserPassError( Exception ):
    pass


class ConnectionError( Exception ):
    def __init__( self, code, message ):
        Exception.__init__( self, message )
        self.code = code
        self.message = message


class baseNamespace:
    def createParams( self, method, args, kwargs ):
        postdata = '{"jsonrpc": "2.0", "id":"1", "method":"%s.%s"' % ( self.name, method )
        if kwargs:
            postdata += ', "params": {'
            append = ''
            for k in kwargs:
                if append: append += ', '
                val = kwargs[ k ]
                append += '"%s":%s' % ( str( k ), simplejson.dumps( val ) )
            postdata += append + '}'
        elif args:
            postdata += ', "params":'
            if len( args ) == 1: args = args[ 0 ]
            postdata += simplejson.dumps( args )
        postdata += '}'
        return postdata


class httpNamespace( baseNamespace ):
    def __init__( self, name, api ):
        self.__handler_cache = {}
        self.api = api
        self.name = name

    def __getattr__( self, method ):
        if method in self.__handler_cache:
            return self.__handler_cache[ method ]

        def handler( *args, **kwargs ):
            postdata = self.createParams( method, args, kwargs )

            try:
                fobj = urllib.urlopen( self.api.url, postdata )
            except IOError, e:
                if e.args[ 0 ] == 'http error':
                     if e.args[ 1 ] == 401: raise UserPassError()
                raise ConnectionError( e.errno, 'Connection error: ' + str( e.errno ) )

            jsonstring = fobj.read()
            try: jsonstring = unicode( jsonstring, 'utf-8', errors='ignore' )
            except: pass
            try:
                json = simplejson.loads( jsonstring )
            finally:
                fobj.close()

            if 'error' in json:
                print postdata
                print json.get( "error" )

            return json.get( "result", {} )

        handler.method = method
        self.__handler_cache[ method ] = handler
        return handler


class execNamespace( baseNamespace ):
    def __init__( self, name, api ):
        self.__handler_cache = {}
        self.api = api
        self.name = name

    def __getattr__( self, method ):
        if method in self.__handler_cache:
            return self.__handler_cache[ method ]

        def handler( *args, **kwargs ):
            postdata = self.createParams( method, args, kwargs )

            jsonstring = xbmc.executeJSONRPC( postdata )
            try: jsonstring = unicode( jsonstring, 'utf-8', errors='ignore' )
            except: pass
            json = simplejson.loads( jsonstring )

            if 'error' in json:
                print postdata
                print json.get( "error" )

            return json.get( "result", {} )

        handler.method = method
        self.__handler_cache[ method ] = handler
        return handler


class jsonrpcAPI:
    def __init__( self, mode='exec', url='http://127.0.0.1:80/jsonrpc', user=None, password=None ):
        mode = ( mode, 'http' )[ ( xbmc is None ) ]
        self.__namespace = None
        if mode == 'http':
            if password: url = url.replace( 'http://', 'http://%s:%s@' % ( user, password ) )
            self.url = url
            self.__namespace = httpNamespace
        else:
            self.__namespace = execNamespace
        self.__namespace_cache = {}

    def __getattr__( self, namespace ):
        if namespace in self.__namespace_cache:
            return self.__namespace_cache[ namespace ]

        self__namespace = self.__namespace #to prevent recursion
        nsobj = self__namespace( namespace, self )

        self.__namespace_cache[ namespace ] = nsobj
        return nsobj
