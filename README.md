### Stranger Friends Server

### If you want to run all server side apps in docker - change row number 22 in ./stranger_friends_authorization_server/stranger_friends_authorization_server/settings.py from "os.path.join(BASE_DIR, './etc/' + PROJECT + '.ini.default')" to "os.path.join(BASE_DIR, './etc/' + PROJECT + '_docker.ini.default')"
