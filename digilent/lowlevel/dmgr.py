import ctypes
import sys

from common import ERC, DINFO, HIF, DTP, DVC

if sys.platform.startswith("win"):
	_dmgr = ctypes.cdll.dmgr
else:
	_dmgr = ctypes.cdll.LoadLibrary("libdmgr.so")

tmsWaitInfinite = 0xFFFFFFFF

_DmgrGetVersion = _dmgr.DmgrGetVersion
_DmgrGetVersion.argtypes = [ctypes.POINTER(ctypes.c_char * 256)]
_DmgrGetVersion.restype = bool

def DmgrGetVersion():
	buf = ctypes.create_string_buffer(256)
	return (_DmgrGetVersion(ctypes.byref(buf)), buf.value)

#DmgrGetLastError returns the last error per process which is updated when a DVC API function fails.
DmgrGetLastError = _dmgr.DmgrGetLastError
DmgrGetLastError.argtypes = []
DmgrGetLastError.restype = ERC

_DmgrSzFromErc = _dmgr.DmgrSzFromErc
_DmgrSzFromErc.argtypes = [ERC, ctypes.POINTER(ctypes.c_char * 48), ctypes.POINTER(ctypes.c_char * 128)]
_DmgrSzFromErc.restype = bool

def DmgrSzFromErc(erc):
	buf_a = ctypes.create_string_buffer(48)
	buf_b = ctypes.create_string_buffer(128)
	return (_DmgrSzFromErc(erc, ctypes.byref(buf_a), ctypes.byref(buf_b)), buf_a.value, buf_b.value)


#OPEN & CLOSE functions
_DmgrOpen = _dmgr.DmgrOpen
_DmgrOpen.argtypes = [ctypes.POINTER(HIF), ctypes.c_char_p]
_DmgrOpen.restype = bool

def DmgrOpen(szSel):
	hif = HIF()
	tmp = ctypes.create_string_buffer(szSel)
	return (_DmgrOpen(ctypes.byref(hif), ctypes.byref(tmp)), hif)

_DmgrOpenEx = _dmgr.DmgrOpenEx
_DmgrOpenEx.argtypes = [ctypes.POINTER(HIF), ctypes.c_char_p, DTP, DTP]
_DmgrOpenEx.restype = bool

def DmgrOpenEx(szSel, dtpTable, dtpDisc):
	hif = HIF()
	tmp = ctypes.create_string_buffer(szSel)
	return (_DmgrOpenEx(ctypes.byref(hif), ctypes.byref(tmp), dtpTable, dtpDisc), hif)

DmgrClose = _dmgr.DmgrClose
DmgrClose.argtypes = [HIF]
DmgrClose.restype = bool


#ENUMERATION functions
_DmgrEnumDevices = _dmgr.DmgrEnumDevices
_DmgrEnumDevices.argtypes = [ctypes.POINTER(ctypes.c_int)]
_DmgrEnumDevices.restype = bool

def DmgrEnumDevices():
	value = ctypes.c_int()
	return (_DmgrEnumDevices(ctypes.byref(value)), value.value)

_DmgrEnumDevicesEx = _dmgr.DmgrEnumDevicesEx
_DmgrEnumDevicesEx.argtypes = [ctypes.POINTER(ctypes.c_int), DTP, DTP, DINFO, ctypes.c_void_p]
_DmgrEnumDevicesEx.restype = bool

def DmgrEnumDevicesEx(dtpTable, dtpDisc, dinfoSel, vInfoSel):
	value = DVC()
	return (_DmgrEnumDevicesEx(ctypes.byref(value), dtpTable, dtpDisc, dinfoSel, vInfoSel), value)

DmgrStartEnum = _dmgr.DmgrStartEnum
DmgrStartEnum.argtypes = [DTP, DTP, DINFO, ctypes.c_void_p]
DmgrStartEnum.restype = bool

DmgrIsEnumFinished = _dmgr.DmgrIsEnumFinished
DmgrIsEnumFinished.argtypes = []
DmgrIsEnumFinished.restype = bool

DmgrStopEnum = _dmgr.DmgrStopEnum
DmgrStopEnum.argtypes = []
DmgrStopEnum.restype = bool

_DmgrGetEnumCount = _dmgr.DmgrGetEnumCount
_DmgrGetEnumCount.argtypes = [ctypes.POINTER(ctypes.c_int)]
_DmgrGetEnumCount.restype = bool

def DmgrGetEnumCount():
	value = ctypes.c_int()
	return (_DmgrGetEnumCount(ctypes.byref(value)), value.value)

_DmgrGetDvc = _dmgr.DmgrGetDvc
_DmgrGetDvc.argtypes = [ctypes.c_int, ctypes.POINTER(DVC)]
_DmgrGetDvc.restype = bool

def DmgrGetDvc(idvc):
	value = DVC()
	return (_DmgrGetDvc(idvc, ctypes.byref(value)), value)

DmgrFreeDvcEnum = _dmgr.DmgrFreeDvcEnum
DmgrFreeDvcEnum.argtypes = []
DmgrFreeDvcEnum.restype = bool


#TRANSFER status and control functions
_DmgrGetTransResult = _dmgr.DmgrGetTransResult
_DmgrGetTransResult.argtypes = [HIF, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32]
_DmgrGetTransResult.restype = bool

def DmgrGetTransResult(hif, tmsWait):
	value_a = ctypes.c_uint32()
	value_b = ctypes.c_uint32()
	return (_DmgrGetTransResult(hif, ctypes.byref(value_a), ctypes.byref(value_b), tmsWait), value_a.value, value_b.value)

DmgrCancelTrans = _dmgr.DmgrCancelTrans
DmgrCancelTrans.argtypes = [HIF]
DmgrCancelTrans.restype = bool

DmgrSetTransTimeout = _dmgr.DmgrSetTransTimeout
DmgrSetTransTimeout.argtypes = [HIF, ctypes.c_uint32]
DmgrSetTransTimeout.restype = bool

_DmgrGetTransTimeout = _dmgr.DmgrGetTransTimeout
_DmgrGetTransTimeout.argtypes = [HIF, ctypes.POINTER(ctypes.c_uint32)]
_DmgrGetTransTimeout.restype = bool

def DmgrGetTransTimeout(hif):
	value = ctypes.c_uint32()
	return (_DmgrGetTransTimeout(hif, ctypes.byref(value)), value.value)


#DVC Table manipulation functions
if sys.platform.startswith("win"):
	DmgrOpenDvcMg = _dmgr.DmgrOpenDvcMg  # opens device manager dialog box
	DmgrOpenDvcMg.argtypes = ['dunno']
	DmgrOpenDvcMg.restype = bool

DmgrDvcTblAdd = _dmgr.DmgrDvcTblAdd
DmgrDvcTblAdd.argtypes = [ctypes.POINTER(DVC)]
DmgrDvcTblAdd.restype = bool

_DmgrDvcTblRem = _dmgr.DmgrDvcTblRem
_DmgrDvcTblRem.argtypes = [ctypes.c_char_p]
_DmgrDvcTblRem.restype = bool

def DmgrDvcTblRem(szAlias):
	tmp = ctypes.create_string_buffer(szAlias)
	return _DmgrDvcTblRem(ctypes.byref(tmp))

DmgrDvcTblSave = _dmgr.DmgrDvcTblSave
DmgrDvcTblSave.argtypes = []
DmgrDvcTblSave.restype = bool


#Device transport type management functions
DmgrGetDtpCount = _dmgr.DmgrGetDtpCount
DmgrGetDtpCount.argtypes = []
DmgrGetDtpCount.restype = int

_DmgrGetDtpFromIndex = _dmgr.DmgrGetDtpFromIndex
_DmgrGetDtpFromIndex.argtypes = [ctypes.c_int, ctypes.POINTER(DTP)]
_DmgrGetDtpFromIndex.restype = bool

def DmgrGetDtpFromIndex(idtp):
	dtp = DTP()
	return (_DmgrGetDtpFromIndex(idtp, ctypes.byref(dtp)), dtp)

_DmgrGetDtpString = _dmgr.DmgrGetDtpString
_DmgrGetDtpString.argtypes = [DTP, ctypes.c_char_p]
_DmgrGetDtpString.restype = bool

def DmgrGetDtpString(dtp):
	tmp = ctypes.create_string_buffer(16)
	return (_DmgrGetDtpString(dtp, tmp), tmp.value)


#Miscellaneous functions
DmgrSetInfo = _dmgr.DmgrSetInfo
DmgrSetInfo.argtypes = [ctypes.POINTER(DVC), DINFO, ctypes.c_void_p]
DmgrSetInfo.restype = bool

DmgrGetInfo = _dmgr.DmgrGetInfo
DmgrGetInfo.argtypes = [ctypes.POINTER(DVC), DINFO, ctypes.c_void_p]
DmgrGetInfo.restype = bool


_DmgrGetDvcFromHif = _dmgr.DmgrGetDvcFromHif
_DmgrGetDvcFromHif.argtypes = [HIF, ctypes.POINTER(DVC)]
_DmgrGetDvcFromHif.restype = bool

def DmgrGetDvcFromHif(hif):
	dvc = DVC()
	return (_DmgrGetDvcFromHif(hif, ctypes.byref(dvc)), dvc)


__all__ = [
	'tmsWaitInfinite', 'DmgrGetVersion', 'DmgrGetLastError', 'DmgrSzFromErc', 'DmgrOpen',
	'DmgrOpenEx', 'DmgrClose', 'DmgrEnumDevices', 'DmgrEnumDevicesEx', 'DmgrStartEnum',
	'DmgrIsEnumFinished', 'DmgrStopEnum', 'DmgrGetEnumCount', 'DmgrGetDvc', 'DmgrFreeDvcEnum',
	'DmgrGetTransResult', 'DmgrCancelTrans', 'DmgrSetTransTimeout', 'DmgrGetTransTimeout',
	'DmgrDvcTblAdd', 'DmgrDvcTblRem', 'DmgrDvcTblSave', 'DmgrGetDtpCount', 'DmgrGetDtpFromIndex',
	'DmgrGetDtpString', 'DmgrSetInfo', 'DmgrGetInfo', 'DmgrGetDvcFromHif'
]
