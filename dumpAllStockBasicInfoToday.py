import baostock as bs
import pandas as pd

def getStockBasic(code):
    # 获取证券基本资料
    rs = bs.query_stock_basic(code=code)
    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    return pd.DataFrame(data_list, columns=rs.fields)


# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)


rs = bs.query_all_stock(day="2021-4-9")
print('query_all_stock respond error_code:'+rs.error_code)
print('query_all_stock respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

for row in range(result.shape[0]):
    code_name=result.loc[row]["code_name"]
    code=result.loc[row]["code"]
    
    code_basic_info=getStockBasic(code)
    print("Getting info:",code,code_name)
    # print(code_basic_info)
    for col in code_basic_info:
        if col not in result.columns.tolist():
            result[col]=""
            result.loc[row][col]=code_basic_info.loc[0][col]
        else:
            result.loc[row][col]=code_basic_info.loc[0][col]

#### 结果集输出到csv文件 ####   
result.to_csv("output/all_stock_basic_info.csv", encoding="utf-8", index=False)
print(result)

# 登出系统
bs.logout()