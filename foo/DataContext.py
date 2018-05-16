from sqlalchemy import *
from sqlalchemy.orm import *
from BillInfo import MainTransferVO
from BasicInfo import ClassifyConfig, BaseinfoConfig, ColumnInfo
from Asset import FunctionLocationVO, DeviceVO

engine = create_engine(
    'sqlite:////Users/Peizhong/Downloads/avmt.db', echo=False)
metaData = MetaData(engine)

Session = sessionmaker(bind=engine)
session = Session()


def MainTransfers():
    result = session.query(MainTransferVO).all()
    print('get %d MainTransfers' % len(result))
    return result


classifyDict = {}


def QueryClassify(classifyId):
    if classifyId not in classifyDict.keys():
        classify = session.query(ClassifyConfig).filter(
            ClassifyConfig.Id == classifyId and ClassifyConfig.IsShow == 1).first()
        classifyDict[classifyId] = classify
    return classifyDict[classifyId]


def QueryTechparam(accountObject):
    classify = QueryClassify(accountObject.ClassifyId)
    if not classify or not classify.TechparamConfigs:
        return None
    columns = [tp.ColumnName for tp in classify.TechparamConfigs]
    paramToQuery = ','.join(columns)
    raw = 'select %s from %s where id=:oid and workspace_id=:wid' % (
        paramToQuery, classify.TableName)
    row = engine.execute(text(raw), oid=accountObject.Id,
                         wid=accountObject.WorkspaceId).fetchone()
    if not row:
        return None
    items = [ColumnInfo(col, row[col]) for col in columns]
    return items


deivceDict = {}


def QueryDeiceByWorkspace(workspaceIds):
    formatedId = ','.join(workspaceIds)
    sql = text(
        'select d.* from dm_fl_asset fla, dm_device d '
        'where fla.workspace_id in (:w) and '
        'fla.asset_id = d.id and '
        'fla.workspace_id = d.workspace_id')
    result = []
    for row in engine.execute(sql, w=formatedId).fetchall():
        d = DeviceVO()
        d.Id = row['ID']
        d.WorkspaceId = row['WORKSPACE_ID']
        d.DeviceName = row['DEVICE_NAME']
        d.ClassifyId = row['CLASSIFY_ID']
        d.AssetState = row['ASSET_STATE']
        d.VoltageId = row['BASE_VOLTAGE_ID']
        d.IsShareDevice = row['IS_SHARE_DEVICE']
        d.UpdateTime = row['UPDATE_TIME']
        d.Techparams = QueryTechparam(d)
        deivceDict['%s_%s' % (d.Id, d.WorkspaceId)] = d
    print('get %d devices' % len(deivceDict.keys()))


def QueryDeivce(functionlocation):
    key = '%s_%s' % (functionlocation.AssetId, functionlocation.WorkspaceId)
    if key in deivceDict.keys():
        return deivceDict[key]
    return None


def FillDeviceInfo(functionlocation):
    deivce = QueryDeivce(functionlocation)
    if deivce:
        # 基本信息&技术参数
        functionlocation.AssetObject = deivce


def FillPartInfo(functionlocation):
    pass


def FillFunction(functionlocation):
    if functionlocation.AssetId:
        if functionlocation.FlType == 3:
            FillDeviceInfo(functionlocation)
    else:
        functionlocation.Techparams = QueryTechparam(functionlocation)


def FunctionLocations(workspaceIds):
    QueryDeiceByWorkspace(workspaceIds)
    formatedId = ','.join(workspaceIds)
    sql = text(
        'select f.*, fla.asset_id from dm_function_location f left join dm_fl_asset fla '
        'on f.id = fla.function_location_id and f.workspace_id = fla.workspace_id '
        'where f.workspace_id in (:w)')
    result = []
    for row in engine.execute(sql, w=formatedId).fetchall():
        func = FunctionLocationVO()
        func.Id = row['ID']
        func.WorkspaceId = row['WORKSPACE_ID']
        func.ParentId = row['PARENT_ID']
        func.FlName = row['FL_NAME']
        func.ClassifyId = row['CLASSIFY_ID']
        func.FlType = row['FL_TYPE']
        func.SortNo = row['SORT_NO']
        func.RunningState = row['RUNNING_STATE']
        func.VoltageId = row['BASE_VOLTAGE_ID']
        func.UpdateTime = row['UPDATE_TIME']
        func.AssetId = row['ASSET_ID']
        FillFunction(func)
        result.append(func)
    print('get %d FunctionLocations' % len(result))
    return result