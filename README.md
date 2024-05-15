1、pip install -r requirements.txt

2、用例存在./lib目录，支持所有用例写在一个表格，支持多个页面


3、运行主入口 mainrunner
   基本都封装完毕，要调整的地方有以下几个
   casename = "apptest" #执行用例的用例名，暂时只支持xlsx格式的用例
    conf = "./lib/conf/conf.properties" #配置文件
    usecase = './lib/%s.xlsx'  #执行的用例
    resultusecase = './lib/%s%s.xlsx'#执行完后生成的结果用例
    
4、邮件模板或者其他配置在 conf.properties


