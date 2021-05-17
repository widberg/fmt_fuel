from inc_noesis import *
from inc_fuel import *

def registerNoesisTypes():
	handle = noesis.register('FUEL Skeleton','.Skel_Z')
	noesis.setHandlerTypeCheck(handle, CheckType)
	noesis.setHandlerLoadModel(handle, LoadModel)	
	return 1
	
def CheckType(data):
	return fuel.assertClass(data, 3611002348)

def LoadModel(data, mdlList):
	ctx = rapi.rpgCreateContext()
	
	header, baseClassData, derivedClassData = fuel.readObject(data)
	bs = NoeBitStream(derivedClassData)

	bs.seek(20,1)	
	jointCount = bs.readUInt()
	bs.seek(24,1)
	
	jointList = []	
	for i in range(jointCount):
		start = bs.tell()
		bs.seek(140,1)
		mat = NoeMat44.fromBytes(bs.readBytes(64)).toMat43()		
		unk = bs.readInt()
		parent = bs.readInt()		
		joint = NoeBone(i, str(i), mat, None, parent)
		jointList.append(joint)
		bs.seek(start + 248)
	
	try:
		mdl = rapi.rpgConstructModel()
	except:
		mdl = NoeModel()
		
	mdl.setBones(jointList)
	mdlList.append(mdl)
	
	return 1
