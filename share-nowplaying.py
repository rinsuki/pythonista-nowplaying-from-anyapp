from nowplayinglib import getNowPlayingInfo, showShareSheet

nowPlayingInfo = getNowPlayingInfo()

if nowPlayingInfo == None:
    print("何も再生してませんが…")
    exit(1)

msg = nowPlayingInfo["kMRMediaRemoteNowPlayingInfoTitle"]
artist = nowPlayingInfo.get("kMRMediaRemoteNowPlayingInfoArtist")
if artist != None:
    msg += " by " + artist
album = nowPlayingInfo.get("kMRMediaRemoteNowPlayingInfoAlbum")
if album != None:
    msg += " (Album: " + album + ")"
msg += " #nowplaying"

del nowPlayingInfo["kMRMediaRemoteNowPlayingInfoArtworkData"]
print(nowPlayingInfo)

print(msg)

showShareSheet(msg)

# ---
