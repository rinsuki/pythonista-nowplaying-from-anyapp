from objc_util import ObjCBlock, ObjCInstance, c, ObjCClass, UIApplication, on_main_thread, ns, NSString, NSDictionary, NSNumber, NSData, nsdata_to_bytes
from ctypes import c_void_p
from threading import Event
import ctypes

NSBoolean = ObjCClass("__NSCFBoolean")
MRMediaRemoteGetNowPlayingInfo = c.MRMediaRemoteGetNowPlayingInfo 
MRMediaRemoteGetNowPlayingInfo.argtypes = [c_void_p, ObjCBlock]
c.dispatch_get_current_queue.restype = c_void_p
UIActivityViewController = ObjCClass("UIActivityViewController")


def getNowPlayingInfo():
    e=Event()
    nowPlayingInfo = None
    def info_cb(_blk,info):
        nonlocal nowPlayingInfo
        try:
            if info:
                nowPlayingInfo = nsDicToPyDic(ObjCInstance(info))
        finally:
            e.set()
    cb=ObjCBlock(info_cb,argtypes=[c_void_p,c_void_p], restype=None)
    MRMediaRemoteGetNowPlayingInfo(c.dispatch_get_current_queue(), cb)
    e.wait()
    return nowPlayingInfo
    

def nsDicToPyDic(nsDic):
    pyDic = {}
    for k in nsDic.allKeys():
        v = nsDic[k]
        if v.isKindOfClass_(NSString):
            v = str(v)
        elif v.isKindOfClass_(NSBoolean):
            v = bool(v)
        elif v.isKindOfClass_(NSNumber):
            vs = v.stringValue()
            if vs.rangeOfString_(ns(".")).length > 0:
                v = float(str(vs))
            else:
                v = v.intValue()
        elif v.isKindOfClass_(NSData):
            v = nsdata_to_bytes(v)
        elif v.isKindOfClass_(NSDictionary):
            v = nsDicToPyDic(v)
        pyDic[str(k)] = v
    return pyDic

@on_main_thread
def showShareSheet(*params):
    vc = UIActivityViewController.alloc().initWithActivityItems_applicationActivities_(ns(list(params)), None)
    rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
    while rootVC.presentedViewController():
        rootVC = rootVC.presentedViewController()
    rootVC.presentViewController_animated_completion_(vc, True, None)
