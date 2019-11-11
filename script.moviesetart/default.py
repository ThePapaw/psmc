# -*- coding: utf-8 -*-

import sys, os, fnmatch, re
import xbmcaddon, xbmc

from xbmcvfs import copy as file_copy
from xbmcvfs import exists as vfs_exists
from xbmcvfs import listdir as vfs_listdir
from traceback import print_exc
from urllib import unquote
    
from lib.log import log
from lib.dialog import dialog_msg
from lib.file_item import Thumbnails
from lib.database import Database, ARTWORK_TYPE_THUMB, ARTWORK_TYPE_FANART,\
    ARTWORK_TYPE_LOGO, ARTWORK_TYPE_CLEARART, ARTWORK_TYPE_EXTRAFANART1, ARTWORK_TYPE_BANNER,\
    ARTWORK_TYPE_POSTER

__addon__               = xbmcaddon.Addon( "script.moviesetart" )
__language__            = __addon__.getLocalizedString
__scriptname__          = __addon__.getAddonInfo('name')
__scriptID__            = __addon__.getAddonInfo('id')
__author__              = __addon__.getAddonInfo('author')
__version__             = __addon__.getAddonInfo('version')

enable_force_update     = (__addon__.getSetting("enable_force_update") == 'true')
enable_search_folders   = (__addon__.getSetting("enable_search_folders") == 'true')
enable_artwork_folder   = (__addon__.getSetting("enable_artwork_folder") == 'true')
artwork_folder_path     = xbmc.translatePath( __addon__.getSetting( "artwork_folder_path" ) ).decode('utf-8')
include_set_prefix      = (__addon__.getSetting("include_set_prefix") == 'true')
recurse_artwork_folder  = (__addon__.getSetting("recurse_artwork_folder") == 'true')
setting_thumb_filenames =    [ name.strip() for name in __addon__.getSetting( "filename_thumb" ).split(',') ]
setting_poster_filenames =   [ name.strip() for name in __addon__.getSetting( "filename_poster" ).split(',') ]
setting_fanart_filenames =   [ name.strip() for name in __addon__.getSetting( "filename_fanart" ).split(',') ]
setting_logo_filenames =     [ name.strip() for name in __addon__.getSetting( "filename_logo" ).split(',') ]
setting_clearart_filenames = [ name.strip() for name in __addon__.getSetting( "filename_clearart" ).split(',') ]
setting_banner_filenames =   [ name.strip() for name in __addon__.getSetting( "filename_banner" ).split(',') ]
setting_extrafanart1_filenames =   [ name.strip() for name in __addon__.getSetting( "filename_extrafanart1" ).split(',') ]

DB = Database()
TBN = Thumbnails()
cached_file_maps = {}

def file_exists( file_path ):
    exists = vfs_exists( file_path )
#    if not exists:
#        log( "File doesn't exist: %s" % (file_path) )
    return exists

def join_path ( base, name ):
    # Check if base folder is a network path, if so always use '/' separator
    if re.search("^.*://.*", base):
        return "%s/%s" % (base, name)
    else:
        return os.path.join(base, name)
    
def get_lenient_name ( name ):
    return re.sub("[^a-zA-Z0-9.]", "", name.lower(), 0)
    
def find_images_lenient ( file_map, base, recurse ):
    log( "Looking for artwork in %s" % base )
    dirs, files = vfs_listdir(base)
    dirs = [f.decode('utf-8') for f in dirs]
    files = [f.decode('utf-8') for f in files]
    for filename in files :
        full_path = join_path(base, filename)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            lenient = get_lenient_name( filename)
            if( not( lenient in file_map ) ):
                file_map[ lenient ] = full_path
    if( recurse ):
        for dirname in dirs :
            full_path = join_path(base, dirname)
            find_images_lenient(file_map, full_path, recurse)

def find_image_lenient ( filename, folder_path, set_name ):
    if include_set_prefix:
        filename = "%s-%s" % (set_name, filename)
    filename = get_lenient_name( filename )
    file_map = {}
    if (folder_path in cached_file_maps):
        file_map = cached_file_maps[folder_path]
    else:
        find_images_lenient(file_map, folder_path, False)
        cached_file_maps[folder_path] = file_map
        # log( "Caching artwork found in %s:\n%s" % (folder_path, file_map) )
    if (filename in file_map):
        return file_map[ filename ]
    return ""

# Creates an ordered set from a list of tuples or other hashable items
def ordered_set(alist):
    mmap = {} # implements hashed lookup
    oset = [] # storage for set
    for item in alist:
        #Save unique items in input order
        if item not in mmap:
            mmap[item] = 1
            oset.append(item)
    return oset

# Method to copy artwork to the cache
def copy_artwork( source_path, dest_path ):
    log( "Copying movie set artwork to cache", xbmc.LOGDEBUG )
    if dest_path.startswith("http://"):
        log( "HTTP destination path is unsupported", xbmc.LOGDEBUG )
    if dest_path.startswith("image://"):
        dest_path = unquote(dest_path)[8:-1]

    log( "Source Path: %s" % repr( source_path ), xbmc.LOGDEBUG )
    log( "Destination Path: %s" % repr( dest_path ), xbmc.LOGDEBUG )
    
    if not file_exists( source_path ):
        log( "Source file does not exist", xbmc.LOGDEBUG )
    elif not file_copy( source_path, dest_path ):
        log( "Failed to copy file", xbmc.LOGDEBUG )

def update_movie_set(percent, movieset, art_type, filename):
    log( "Selected %s: %s" % (art_type, filename), xbmc.LOGDEBUG)
    dialog_msg( "update", percent = percent, line1 = __language__( 32006 ), \
                line2 = " %s %s" % ( __language__( 32007 ), movieset[ "label" ] ), \
                line3 = filename )
    return DB.updateDatabase(movieset[ "setid" ], filename, art_type, enable_force_update)
        
# Method to update all the movie set artwork
def update_movie_sets(overwrite = False):
    log( "Updating artwork for Movie Sets", xbmc.LOGNOTICE )
    dialog_msg( "create" )
    found_artwork_count = 0    
    db_update_count = 0    

    # Map of artwork types and their corresponding possible filenames
    artwork_type_filenames = {}
    artwork_type_filenames[ARTWORK_TYPE_THUMB] = setting_thumb_filenames
    artwork_type_filenames[ARTWORK_TYPE_POSTER] = setting_poster_filenames
    artwork_type_filenames[ARTWORK_TYPE_FANART] = setting_fanart_filenames
    artwork_type_filenames[ARTWORK_TYPE_LOGO] = setting_logo_filenames
    artwork_type_filenames[ARTWORK_TYPE_CLEARART] = setting_clearart_filenames
    artwork_type_filenames[ARTWORK_TYPE_BANNER] = setting_banner_filenames
    artwork_type_filenames[ARTWORK_TYPE_EXTRAFANART1] = setting_extrafanart1_filenames
            
    # Get movie sets
    movie_sets = DB.getMovieSets()
    
    if len( movie_sets ) == 0:
        dialog_msg( "okdialog", line1 = __language__(32011) )
        return found_artwork_count, db_update_count

    # Find all images in the artwork folder, mapped by lenient filenames used for matching  
    file_map = {}
    if ( enable_artwork_folder and artwork_folder_path != ""):
        find_images_lenient(file_map, artwork_folder_path, recurse_artwork_folder)
        log( "Artwork folder image map: %s" % file_map )
            
    for countset, movieset in enumerate( movie_sets ):
        try:
            if dialog_msg( "iscanceled" ):
                break
            movieset_name = movieset[ "label" ]
            percent = int( ( countset/float( len( movie_sets ) ) ) * 100 ) 
            dialog_msg( "update", percent = percent, line1 = __language__( 32006 ), \
                        line2 = " %s %s" % ( __language__( 32007 ), movieset_name ) )
            # This sleep isn't needed, just makes UI nicer
            xbmc.sleep( 100 )
            
            log( "------------------------------------------------------------", xbmc.LOGDEBUG )
            log( "Processing movie set: %s" % movieset_name,              xbmc.LOGDEBUG)
            log( "------------------------------------------------------------", xbmc.LOGDEBUG )
            
            # The cache path is no longer correct in Gotham. Need fix or to lookup textures.db
            # videodb://1/7/ -> videodb://movies/sets/
             
            #set_thumb = TBN.get_cached_saga_thumb( movieset[ "setid" ], False )
            #log( "Cached thumb filename: %s" % set_thumb, xbmc.LOGDEBUG )
            #set_fanart = TBN.get_cached_saga_thumb( movieset[ "setid" ], True )
            #log( "Cached fanart filename: %s" % set_fanart, xbmc.LOGDEBUG )

            # If exiting artwork and not overwrite, move on
            #if (not overwrite and (file_exists( set_thumb ) or file_exists( set_fanart )) ):
            #    continue

            artwork_types_copied = []
            artwork_found = {}
            for artwork_type in artwork_type_filenames:
                artwork_found[artwork_type] = []
                
            if ( enable_artwork_folder and artwork_folder_path != ""):
                
                # Check if there is artwork in the search folder matching all the supported artwork types
                log( "== Checking single artwork folder ==", xbmc.LOGDEBUG )
                for artwork_type in artwork_type_filenames:
                    for artwork_filename in artwork_type_filenames[artwork_type]:
                        artwork_filename = get_lenient_name("%s-%s" % (movieset_name, artwork_filename) )
                        # log( "Checking for: %s" % artwork_filename )
                        if (artwork_filename in file_map):
                            artwork_filename = file_map[ artwork_filename ]
                            artwork_found[artwork_type].append(artwork_filename)
                            db_update_count += update_movie_set(percent, movieset, artwork_type, artwork_filename)
                            artwork_types_copied.append(artwork_type)
                            break
                    
                # If we found all artwork types, we can move on
                log( "Found artwork for %s types" % len(artwork_types_copied) )
                if ( len(artwork_types_copied) == len(artwork_type_filenames) ):
                    continue
                
            if ( enable_search_folders ):
                movie_folders = []
                movie_folder_names = []
                
                # Scan the movies in the set and their folders
                log( "== Scanning movies in set for folder names and artwork ==", xbmc.LOGDEBUG )
                movies = DB.getMoviesInSet( movieset[ "setid" ])
                for movie in movies:
                    try:
                        dialog_msg( "update", percent = percent, line1 = __language__( 32006 ), \
                                    line2 = " %s %s" % ( __language__( 32007 ), movieset_name ), \
                                    line3 = " %s %s" % ( __language__( 32010 ), movie[ "title" ] ) )
                        log( "Processing movie: %s" % movie[ "title" ], xbmc.LOGDEBUG )
                
                        movie_folder = os.path.dirname( movie[ "file" ] )
                        movie_folders.append(movie_folder)
                        movie_folder_names.append(os.path.basename(movie_folder))
                        
                        # Check for artwork in the parent folder of the movie folder
                        parent_folder = os.path.dirname( movie_folder )
                        
                        # Remember all artwork found during scan of movies in the set
                        for artwork_type in artwork_type_filenames:
                            if (not artwork_type in artwork_types_copied):
                                for artwork_filename in artwork_type_filenames[artwork_type]:
                                    artwork_filename = find_image_lenient(artwork_filename, parent_folder, movieset_name)
                                    if file_exists( artwork_filename ):
                                        artwork_found[artwork_type].append(artwork_filename)
                                        break
                            
                    except:
                        xbmc.log( "enumerate( movies ): %s" % repr( movie ), xbmc.LOGERROR )
                        print_exc()

                # Check if all movies are actually under one folder name (may be different paths)
                log( "Movie folders found: %s" % movie_folder_names)
                if ( len( set(movie_folder_names) ) == 1 ):
                    log( "== All movies in the set have the same folder name ==", xbmc.LOGDEBUG)
                    for movie_folder in ordered_set(movie_folders):
                        log( "Checking folder for artwork: %s" % movie_folder, xbmc.LOGDEBUG)
                        # Ignore artwork found during scan and look in the single folder                        
                        for artwork_type in artwork_type_filenames:
                            if (not artwork_type in artwork_types_copied):
                                for artwork_filename in artwork_type_filenames[artwork_type]:
                                    artwork_filename = find_image_lenient(artwork_filename, movie_folder, movieset_name)
                                    if file_exists( artwork_filename ):
                                        artwork_found[artwork_type].append(artwork_filename)
                                        db_update_count += update_movie_set(percent, movieset, artwork_type, artwork_filename)
                                        artwork_types_copied.append(artwork_type)
                                        break
                                    
                # Else movies are in different folders
                else:
                    # Use the most popular artwork amongst movies in the set
                    log( "== Selecting artwork found during scan ==", xbmc.LOGDEBUG )
                    for artwork_type in artwork_type_filenames:
                        if (not artwork_type in artwork_types_copied):
                            artwork = artwork_found[artwork_type]
                            if ( len(artwork) > 0):
                                log( "Possible artwork: %s" % list(set(artwork)), xbmc.LOGDEBUG)
                                artwork_filename = max( set(artwork), key=artwork.count )
                                db_update_count += update_movie_set(percent, movieset, artwork_type, artwork_filename)
                                artwork_types_copied.append(artwork_type)
                            
        except:
            xbmc.log( "enumerate( movie_sets ): %s" % repr( movieset ), xbmc.LOGERROR )
            print_exc()

        finally:
            log( "------------------------------------------------------------", xbmc.LOGDEBUG )
            log( "All artwork found for set:\n%s" % artwork_found, xbmc.LOGDEBUG)
            artwork_found_no_empty = dict((k, v) for k, v in artwork_found.iteritems() if v)
            if ( len(artwork_found_no_empty) > 0 ):
                found_artwork_count += 1

            
    # dialog_msg( "update", percent = 100, line1 = __language__( 32009 ) )
    # xbmc.sleep( 1000 )
    dialog_msg( "close" )
    return found_artwork_count, db_update_count
    
if ( __name__ == "__main__" ):
    
    xbmc.executebuiltin('Dialog.Close(all, true)')
    
    log( "############################################################", xbmc.LOGNOTICE )
    log( "#    %-50s    #" % __scriptname__, xbmc.LOGNOTICE )
    log( "#    %-50s    #" % __scriptID__, xbmc.LOGNOTICE )
    log( "#    %-50s    #" % __author__, xbmc.LOGNOTICE )
    log( "#    %-50s    #" % __version__, xbmc.LOGNOTICE )
    log( "#    %-50s    #" % "", xbmc.LOGNOTICE )
    log( "#    %-50s    #" % "Thanks to Frost (passion-xbmc.org) for example ", xbmc.LOGNOTICE )
    log( "#    %-50s    #" % "code used in this addon", xbmc.LOGNOTICE )
    log( "############################################################", xbmc.LOGNOTICE )

    log( "Search common folders: %d" % enable_search_folders, xbmc.LOGDEBUG )
    log( "Include set prefix: %d" % include_set_prefix, xbmc.LOGDEBUG )
    log( "Enable artwork folder: %d" % enable_artwork_folder, xbmc.LOGDEBUG )
    log( "Artwork folder: %s" % artwork_folder_path, xbmc.LOGDEBUG )
    log( "Include sub folders: %d" % recurse_artwork_folder, xbmc.LOGDEBUG )
    log( "Thumb filenames: %s" % setting_thumb_filenames, xbmc.LOGDEBUG )
    log( "Poster filenames: %s" % setting_poster_filenames, xbmc.LOGDEBUG )
    log( "Fanart filenames: %s" % setting_fanart_filenames, xbmc.LOGDEBUG )
    log( "Logo filenames: %s" % setting_logo_filenames, xbmc.LOGDEBUG )
    log( "Clearart filenames: %s" % setting_clearart_filenames, xbmc.LOGDEBUG )
    log( "Banner filenames: %s" % setting_banner_filenames, xbmc.LOGDEBUG )
    log( "Extrafanart1 filenames: %s" % setting_extrafanart1_filenames, xbmc.LOGDEBUG )
    
    try:
        xbmc.executebuiltin('Dialog.Close(all, true)') 
        xbmc.sleep( 1000 )

        # Check the XBMC version to determine DB or JSON
        xbmcVersion = xbmc.getInfoLabel( "system.buildversion" )
        log( "XBMC build version: %s" % xbmcVersion )
        if xbmcVersion.startswith("12"):
            log( "Using Frodo SQL database" )
            useSQL = True
        else:
            log( "Using Gotham JSON" )
            useSQL = False

        # Before accessing database, check that HTTP server is running
        if ( not useSQL and not xbmc.getCondVisibility( "System.GetBool(services.esenabled)" ) ):
            dialog_msg( "okdialog", line1 = __language__(32014) )
            xbmc.executebuiltin( "ActivateWindow(servicesettings)" )
                    
        elif (not (enable_artwork_folder or enable_search_folders) ):
            dialog_msg( "okdialog", line1 = __language__(32012) )
            
        else:
            # In Frodo, there is always artwork for movie sets, so no overwrite means no point running
            overwrite = dialog_msg( "yesno", line1 = __language__(32008) )
            if (overwrite):
                DB.initialise(useSQL)
                found_artwork_count, db_update_count = update_movie_sets(overwrite)
                dialog_msg( "okdialog", line1 = __language__(32013) % (found_artwork_count, db_update_count) )
    except:
        print "Unexpected error: ", sys.exc_info()
        dialog_msg( "okdialog", line1 = str(sys.exc_info()[0]), \
                    line2 = str(sys.exc_info()[1]) )
        raise
    
    xbmc.executebuiltin('Dialog.Close(all, true)') 
