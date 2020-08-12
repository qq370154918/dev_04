
def handel_request_headers(data):
    '''
    处理header，params，data数据，将字典转换为对应格式列表
    :param data:
    :return:
    '''
    data_list=[]
    if data:
        for key in data.keys():
            data_list.append({
                "key":key,
                "value":data.get(key)
            })
    "如果数据中没有，直接返回空列表"
    return data_list

def handel_test_data_variables(test_data,key):
    '''
    处理test里面variables，对应的返回是globalVar
    :param test_data:
    :param key:
    :return:
    '''
    data_list = []
    if key in test_data.keys():
        data = test_data.get(key)  # 列表
        for item in data:
            my_type=type(item[list(item)[0]]).__name__
            if my_type=="int":
                param_type = "int"
            elif my_type=="str":
                param_type = "string"
            elif my_type=="float":
                param_type = "float"
            elif my_type=="bool":
                param_type = "bool"
            data_list.append({
                "key": list(item)[0],
                "value": item[list(item)[0]],
                "param_type": param_type
            })
    "如果数据中没有，直接返回空列表"
    return data_list