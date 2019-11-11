"""
    Database module
"""

# Modules XBMC
import os, sys, re, xml.dom.minidom
import xbmc, xbmcvfs

# Modules Custom
import jsonrpc
from url_util import UrlUtil
from log import log

# Import SQLite for local database
try:
    from sqlite3 import dbapi2 as sqlite
except:
    from pysqlite2 import dbapi2 as sqlite

# Import MySQL for shared database
import mysql.connector
    
SORTTITLE = { "method": "sorttitle", "order": "ascending" }
ARTWORK_TYPE_THUMB = "thumb"
ARTWORK_TYPE_POSTER = "poster"
ARTWORK_TYPE_FANART = "fanart"
ARTWORK_TYPE_LOGO = "clearlogo"
ARTWORK_TYPE_CLEARART = "clearart"
ARTWORK_TYPE_BANNER = "banner"
ARTWORK_TYPE_EXTRAFANART1 = "extrafanart1"
DATABASE_VERSION_FRODO = "75"

# Class to implement a custom cursor returning dictionary results
class MySQLCursorDict(mysql.connector.cursor.MySQLCursor):
    
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None

# Video database class performing fetching and updating operations
class Database():
    
    def initialise( self, useSQL ):
        self.useSQL = useSQL
        if (self.useSQL):
            self.useMySQL = False
            myVideoConfig = self.getVideoDBConfig()
            dbType = myVideoConfig["type"]
            dbName = myVideoConfig["name"]
            
            if (dbType == "mysql"):
                log( "Using MySQL connector: %s" % myVideoConfig )
                self.useMySQL = True
                self.db_conn = mysql.connector.connect(
                                  user=myVideoConfig["user"], password=myVideoConfig["pass"],
                                  host=myVideoConfig["host"], port=myVideoConfig["port"],
                                  database=dbName.encode("utf-8"))
            else:
                log( "Using SQlite connector: %s" % myVideoConfig )
                dbName = "%s.db" % dbName
                self.video_db = os.path.join(xbmc.translatePath("special://database"), dbName)
                self.db_conn = sqlite.connect(self.video_db)
            self.db_conn.row_factory = sqlite.Row
        else:
            self.json_api = jsonrpc.jsonrpcAPI()

    def getElementText(self, domItem, name, default=""):
        element = domItem.getElementsByTagName(name)
        if ( len(element) > 0 ):
            return element[0].firstChild.data
        return default
        
    def getVideoDBConfig(self):
        result = {}
        
        # Set default to sqlite
        result["type"] = "sqlite3"
        result["name"] = "MyVideos"
        
        # Assume Frodo DB file, as later versions use JSON
        result["name"] = "MyVideos%s" % DATABASE_VERSION_FRODO
        
        # Look for overrides in advanced settings
        advanced_xml = xbmc.translatePath( "special://profile/advancedsettings.xml" )
        if xbmcvfs.exists( advanced_xml ):
            log( "Parsing advancedsettings.xml" )
            if hasattr( xbmcvfs, "File" ):
                OPEN = xbmcvfs.File
            else:
                OPEN = open
            configFile = OPEN( advanced_xml )

            # Parse XML
            try:
                document = xml.dom.minidom.parse(configFile)
            except:
                print "Error parsing XML: ", sys.exc_info()
                return result
            for item in document.getElementsByTagName("videodatabase"):
                result["type"] = self.getElementText(item, "type", "sqlite3")
                result["name"] = self.getElementText(item, "name", result["name"])
                if (result["type"] == "mysql"):
                    result["host"] = self.getElementText(item, "host")
                    result["port"] = self.getElementText(item, "port", "3306")
                    result["user"] = self.getElementText(item, "user")
                    result["pass"] = self.getElementText(item, "pass")
            configFile.close()
        return result
            
    def getCursor(self):
        if (self.useMySQL):
            return self.db_conn.cursor(cursor_class=MySQLCursorDict)
        else:
            return self.db_conn.cursor()
            
    def executeQuery(self, cursor, query, params=None):
        if (self.useMySQL):
            query = query.replace("?", "%s")
            
        if (params != None):
            return cursor.execute(query, params)
        else:
            return cursor.execute(query)
            
    def getMovieSets(self):
        if (self.useSQL):
            cur = self.getCursor()
            self.executeQuery(cur, "SELECT * FROM sets")
            rows = cur.fetchall()
            movie_sets = []
            for row in rows:
                movie_set = {}
                movie_set[ "setid" ] = row[ "idSet" ]
                movie_set[ "label" ] = row[ "strSet" ]
                movie_sets.append(movie_set)
            return movie_sets
        else:
            json = self.json_api.VideoLibrary.GetMovieSets(properties=["art"])
            movie_sets = json.get( "sets", [] )
            log( "Sets: %s" % movie_sets )
            return movie_sets
    
    def getMoviesInSet( self, setId ):
        if (self.useSQL):
            cur = self.getCursor()
            self.executeQuery(cur, "SELECT * FROM movie where idSet = ?", (setId,))
            rows = cur.fetchall()
            movies = []
            for row in rows:
                movie = {}
                movie[ "title" ] = row[ "c00" ]
                movie[ "file" ] = row[ "c22" ]   # only folder, but enough
                movies.append(movie)
            return movies
        else:
            # Get the list of movies using GetMovieSetDetails
            json = self.json_api.VideoLibrary.GetMovieSetDetails( setid=setId, properties=["art"] )
            set_details = json.get( "setdetails", [] ) 
            log( "Set details: %s" % set_details )
            movies = set_details.get( "movies", [] )
            for movie in movies:
                # Get the file location of the movie using GetMovieDetails
                json = self.json_api.VideoLibrary.GetMovieDetails( movieid=movie["movieid"], properties=["file","art"] )
                details = json.get( "moviedetails", [] )
                # log( "Set Movie: %s" % details )
                movie[ "title" ] = movie[ "label" ]
                movie[ "file" ] = details[ "file" ]
            return movies
    
    # Method to update the URL assigned for movie set artwork in the video DB
    def updateDatabase(self, setId, filename, art_type, force_write):
        if (self.useSQL):
            return self.updateDatabaseSQL(setId, filename, art_type, force_write)
        else:
            return self.updateDatabaseJSON(setId, filename, art_type, force_write)
        
    def updateDatabaseJSON(self, setId, filename, art_type, force_write):
        # Check what type is already set
        json = self.json_api.VideoLibrary.GetMovieSetDetails( setid=setId, properties=["art"] )
        set_details = json.get( "setdetails", [] )
        set_art = set_details["art"]

        filename = UrlUtil.denormalise(filename, True)
        
        updated = 0
        if ( art_type in set_art ):
            existing_filename = set_art[art_type]
            log ( "Existing %s: %s" % (art_type, existing_filename) )
            if ( force_write or (existing_filename.lower() != filename.lower()) ):
                log( "Updating artwork:\nType: %s\nExisting: %s\nNew:      %s" % (art_type, existing_filename, filename), xbmc.LOGDEBUG )
                self.json_api.VideoLibrary.SetMovieSetDetails( setid=setId, art={art_type: filename} )
                updated += 1
        else:
            log( "Adding artwork:\nType: %s\nFile: %s" % (art_type, filename), xbmc.LOGDEBUG )
            self.json_api.VideoLibrary.SetMovieSetDetails( setid=setId, art={art_type: filename} )
            updated += 1
        return updated
    
    def updateDatabaseSQL(self, setId, filename, art_type, force_write):
        # Check what type is already set
        cur = self.getCursor()
        self.executeQuery(cur, "SELECT type, url FROM art where media_type = ? and media_id = ? and url != ''", ("set", setId))
        existing_type_map = {}
        rows = cur.fetchall()
        for row in rows:
            existing_type_map[row["type"] ] = row["url"]
        
        # Work out what should be updated
        # log ( "Existing artwork for set %s: %s" % (setId, existing_type_map) )
        if ( art_type in existing_type_map ):
            log ( "Existing %s: %s" % (art_type, existing_type_map[art_type]) )
        update_type = art_type

        # Perform create/update
        updated = 0
        cur = self.getCursor()
        if ( update_type in existing_type_map ):
            if ( existing_type_map[update_type] == filename ):
                if (force_write):
                    log( "Removing existing artwork:\nType: %s\nFile: %s" % (update_type, existing_type_map[update_type]), xbmc.LOGDEBUG )
                    self.executeQuery(cur, "DELETE from art where media_type = ? and media_id = ? and type = ?", \
                                 ("set", setId, update_type) )
                    log( "Adding artwork:\nType: %s\nFile: %s" % (update_type, filename), xbmc.LOGDEBUG )
                    self.executeQuery(cur, "INSERT INTO art(media_id, media_type, type, url) VALUES(?,?,?,?)", \
                                 (setId, "set", update_type, filename) )
                    updated += 1
            else:
                log( "Updating artwork:\nType: %s\nExisting: %s\nNew:      %s" % (update_type, existing_type_map[update_type], filename), xbmc.LOGDEBUG )
                self.executeQuery(cur, "UPDATE art SET url = ? where media_type = ? and media_id = ? and type = ?", \
                             (filename, "set", setId, update_type) )
                updated += 1
        else:
            log( "Adding artwork:\nType: %s\nFile: %s" % (update_type, filename), xbmc.LOGDEBUG )
            self.executeQuery(cur, "INSERT INTO art(media_id, media_type, type, url) VALUES(?,?,?,?)", \
                         (setId, "set", update_type, filename) )
            updated += 1
        self.db_conn.commit()
        cur.close()

        return updated
    