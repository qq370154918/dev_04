
def handel_request_data(request_data,key):
    '''
    处理header，params，data数据，将字典转换为对应格式列表
    :param data:
    :return:
    '''
    data_list=[]
    "如果数据中有header，params，data，进行处理并返回"
    if key in request_data.keys():
        data=request_data.get(key)  #字典
        for key in data.keys():
            data_list.append({
                "key":key,
                "value":data.get(key)
            })
    "如果数据中没有，直接返回空列表"
    return data_list

def handel_test_data(test_data,key):
    '''
    处理test里面parameters，extract,variables，validate，将列表转换为对应格式列表
    :param test_data:
    :param key:
    :return:
    '''
    data_list = []
    "如果数据中有header，params，data，进行处理并返回"
    if key in test_data.keys():
        data = test_data.get(key)  # 列表
        for item in data:
            data_list.append({
                "key": list(item)[0],
                "value": item[list(item)[0]]
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

def handel_test_data_validate(test_data,key):
    '''
    处理test里面validate，将列表转换为对应格式列表
    :param test_data:
    :param key:
    :return:
    '''
    data_list = []
    "如果数据中有header，params，data，进行处理并返回"
    if key in test_data.keys():
        data = test_data.get(key)  # 列表
        for item in data:
            my_type = type(item["expected"]).__name__
            if my_type == "int":
                param_type = "int"
            elif my_type == "str":
                param_type = "string"
            elif my_type == "float":
                param_type = "float"
            elif my_type == "bool":
                param_type = "bool"

            data_list.append({
                "key": item["check"],
                "value": item["expected"],
                "param_type": my_type,
                "comparator":item["comparator"],
            })
    "如果数据中没有，直接返回空列表"
    return data_list
def handel_test_data_hooks(test_data,key):
    '''
    处理test里面validate，将列表转换为对应格式列表
    :param test_data:
    :param key:
    :return:
    '''
    data_list = []
    "如果数据中有header，params，data，进行处理并返回"
    if key in test_data.keys():
        data = test_data.get(key)  # 列表
        for item in data:
            data_list.append({
                "key": item,
            })
    "如果数据中没有，直接返回空列表"
    return data_list

if __name__ == '__main__':
    data = {
            "headers":{
                "uname":"keyou",
                "age":"18"
                    }
            }
    print(handel_request_data(data,'headers'))
    print(handel_request_data(data,'data'))

    data = {
           "validate":[
            {
                "check":"status_code",
                "expected":200,
                "comparator":"equals"
            },
            {
                "check":"love",
                "expected":"lemon",
                "comparator":"equals"
            }
        ],
    }

    print(handel_test_data(data, 'parameters'))
    print(handel_test_data_validate(data, 'validate'))