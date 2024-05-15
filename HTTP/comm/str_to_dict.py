# -*- coding: utf-8 -*-
# Powered By: ECHO
# @Time : 2020/12/20 12:52
import json
import traceback

from common.logger import logger


def str_to_dict(datas):
    if datas == "" or datas is None:
        datas = None
        return None
    try:
        datas = json.loads(datas)
    except Exception as e:
        logger.error(traceback.format_exc())

    return datas


if __name__ == "__main__":
    datas = '{"took":2,"timed_out":false,"_shards":{"total":5,"successful":5,"skipped":0,"failed":0},"hits":{"total":1,"max_score":1.0,"hits":[{"_index":"hdb-prod-build-v3","_type":"prodesdoc","_id":"1695693385039705989","_score":1.0,"_source":{"id":"1695693385039705989","projGuid":"94ff8b2a-4cea-4d1c-bf3d-002d4e7aa59b","buildName":"旷超ES专项测试楼盘","buildCover":"https://hdbbmp-dev.oss-cn-shenzhen.aliyuncs.com/hdb/2020/12/17/ad6222a260124802ba37fcb937529e82","gpsPoint":{"lat":27.23258,"lon":112.73876},"buildSearchLabels":["售罄","宜居养生","生态大盘"],"buildShowLabels":["售罄","宜居养生","生态大盘"],"buildSearchLabelIds":[3,1269884937813655553,1269884935745863681],"buildShowLabelIds":[3,1269884937813655553,1269884935745863681],"buildScreenLabels":["6","6","别墅户型","未开盘","低密居所","APP楼盘频道","66","add"],"buildScreenLabelIds":[1316911118084030466,1316910873367363585,1274966390561873922,1,1269884937398419458,1277225286290694146,1280461905281953794,1339128467700621314],"isNew":0,"buildCompany":"案场宝-TEST-公司","buildCompanyId":"2008200000001182","buildTypes":["高层","洋房","别墅","公寓","商铺","写字楼"],"buildTypeIds":["1","2","3","4","5","6"],"examinedStatus":3,"buildPrice":"88888","buildArea":"999999999","areaScope":"1-9999","buildSellPoint":"尊贵 至尊","buildSalesStatus":1,"buildSalesStatusName":"未开盘","buildTel":"18617099614","lastUpdateDate":"2020-12-17 17:26:16","lastUpdateBy":"张智伟","onlineId":"1339494873491275778","buildOnlineStatus":1,"onlineExaminedStatus":1,"belongProvinceName":"湖南省","belongProvinceCode":"430000","belongCityName":"衡阳市","belongCityCode":"430400","belongAreaName":"衡阳县","belongAreaCode":"430421","buildOnlineCityCodes":["120100","110100","430400"],"buildOnlineCityNames":["天津市","北京市","衡阳市"],"buildOnlineProvCodes":["120000","110000","430000"],"showCity":null,"showCityIds":null,"jointMarketInfo":null,"jointMarketCity":null,"jointMarketCityCode":null,"buildOnlineDate":"2020-12-17 16:57:43","buildSort":1,"isSpecialAisle":0,"isJointMarketing":0,"newOpenSort":null,"popularBuildingId":null,"isPopular":null,"isGroupClass":null,"regionSort":null,"groupSort":null,"otherOnlineConfigAttr":null,"otherBaseAttrs":null,"buildSubDate":null,"buildOpenDate":"2020-12-17","hftBuildId":null,"authorityTenantId":1,"authorityCompanyId":2008200000001182,"authorityCorpId":2008170000000466,"authorityProjectId":1695693385039705989,"buildDevType":"1","buildDevName":"旷超自建"}}]}}'
    dic = str_to_dict(datas)
    print(logger.info(dic))
