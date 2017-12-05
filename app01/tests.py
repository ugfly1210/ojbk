from django.test import TestCase

# Create your tests here.


# 展开多重列表
# L = [["a","b",["c",[1,[2],"d"],"e"]],[3,'f'],4,"g",5]
# # 递归遍历。
# def flattenList(L,new_list=[]):
#     # 展平多重列表
#     for i in L:
#         if not isinstance(i,list):
#             new_list.append(i)
#         else:
#             flattenList(i,new_list)
#     return new_list
# print(flattenList(L))


#递归
# def num(i):
#     if i == 2 :
#         print(i,'nei')
#         return 2
#     # print(i)
#     return i*num(i-1)
# num= num(4)
# print(num)

# '''
# comment_dict:{
#
# 1: {'id': 1, 'content': '...', 'Pid': None, 'chidren_commentList': []},
# 2: {'id': 2, 'content': '...', 'Pid': None, 'chidren_commentList': []},
# 3: {'id': 3, 'content': '...', 'Pid': None, 'chidren_commentList': []},
# 4: {'id': 4, 'content': '...', 'Pid': 1, 'chidren_commentList': []},
# 5: {'id': 5, 'content': '...', 'Pid': 1, 'chidren_commentList': []},
# 6: {'id': 6, 'content': '...', 'Pid': 4, 'chidren_commentList': []},
# 7: {'id': 7, 'content': '...', 'Pid': 3, 'chidren_commentList': []},
# 8: {'id': 8, 'content': '...', 'Pid': 7, 'chidren_commentList': []},
# 9: {'id': 9, 'content': '...', 'Pid': None, 'chidren_commentList': []}
#
# }
# '''



# from app01 import views

# comment_list=[
#
#     {"id":1,"content":"...","Pid":None},
#     {"id":2,"content":"...","Pid":None},
#     {"id":3,"content":"...","Pid":None},
#     {"id":4,"content":"...","Pid":1},
#     {"id":5,"content":"...","Pid":1},
#     {"id":6,"content":"...","Pid":4},
#     {"id":7,"content":"...","Pid":3},
#     {"id":8,"content":"...","Pid":7},
#     {"id":9,"content":"...","Pid":None},
#
# ]
#
#
#
# comment_dict = {}
# for comment in comment_list:
#     comment['child']= []
#     comment_dict[comment["id"]] = comment
#
#
# """
# {'id': 1, 'content': '...', 'Pid': None, 'child': []}
# {'id': 2, 'content': '...', 'Pid': None, 'child': []}
# {'id': 3, 'content': '...', 'Pid': None, 'child': []}
# {'id': 4, 'content': '...', 'Pid': 1, 'child': []}
# {'id': 5, 'content': '...', 'Pid': 1, 'child': []}
# {'id': 6, 'content': '...', 'Pid': 4, 'child': []}
# {'id': 7, 'content': '...', 'Pid': 3, 'child': []}
# {'id': 8, 'content': '...', 'Pid': 7, 'child': []}
# {'id': 9, 'content': '...', 'Pid': None, 'child': []}
# """
#
# """
# 1 {'id': 1, 'content': '...', 'Pid': None, 'child': []}
# 2 {'id': 2, 'content': '...', 'Pid': None, 'child': []}
# 3 {'id': 3, 'content': '...', 'Pid': None, 'child': []}
# 4 {'id': 4, 'content': '...', 'Pid': 1, 'child': []}
# 5 {'id': 5, 'content': '...', 'Pid': 1, 'child': []}
# 6 {'id': 6, 'content': '...', 'Pid': 4, 'child': []}
# 7 {'id': 7, 'content': '...', 'Pid': 3, 'child': []}
# 8 {'id': 8, 'content': '...', 'Pid': 7, 'child': []}
# 9 {'id': 9, 'content': '...', 'Pid': None, 'child': []}
# """
#
#
# import time
# commentL = []
# for comment in comment_list:
#     if comment.get('Pid'):#如果有的话
#
#         # print("comment_dict",comment_dict)
#         # print("comment",comment)
#         comment_dict[comment['Pid']]['child'].append(comment)
#
#     else:
#         commentL.append(comment)
#
# print(commentL)
# [
# {'id': 1, 'content': '...', 'Pid': None, 'child': [{'id': 4, 'content': '...', 'Pid': 1, 'child': [{'id': 6, 'content': '...', 'Pid': 4, 'child': []}]},{'id': 5, 'content': '...', 'Pid': 1, 'child': []}]},
# {'id': 2, 'content': '...', 'Pid': None, 'child': []},
# {'id': 3, 'content': '...', 'Pid': None, 'child': [{'id': 7, 'content': '...', 'Pid': 3, 'child': [{'id': 8, 'content': '...', 'Pid': 7, 'child': []}]}]},
# {'id': 9, 'content': '...', 'Pid': None, 'child': []}
# ]

# for i in comment_dict:
#     print(i,comment_dict[i])

# {
# 1: {'id': 1, 'content': '...', 'Pid': None, 'child': []},
# 2: {'id': 2, 'content': '...', 'Pid': None, 'child': []},
# 3: {'id': 3, 'content': '...', 'Pid': None, 'child': []},
# 9: {'id': 9, 'content': '...', 'Pid': None, 'child': []}
# }





#面向对象的基本方法
class Person:
    height='166'
    def __init__(self,name,age,sex):
        self.name = name
        self._age = age
        self.__sex = sex

    @classmethod
    def get_height(cls):
        return cls.height

    @property
    def get_sex(self):
        return self.__sex

    def self_introduction(self):
        print(' My Name is %s \n I\'m  %s years old \n '%(self.name,self._age))

if __name__ == '__main__':
    person = Person('ff',18,'male')
    print(dir(person))
    #调用类属性(直接用类调用类方法)
    print(Person.get_height())
    #调用静态属性(实例化类对象调用函数)
    print(person.get_sex)
    #调用正常属性(实例化类对象调用类方法)
    person.self_introduction()

#类的继承,推荐用super()
#可以用isinstance(a,b)   a是被继承的类的名称,b是父类名称. 如果a是继承b,会返回True.

#类的多态
#要素 : 1. 继承   2. 重写方法


'''常用的类定义

一般都会在类里面定义一个 __init__的构造函数

对象实例化的过程 : 
def __new__(cls):   创建类对象
def __init__(self):  初始化对象
'''


'''
转换成字符串

__str__  是转换成人看的字符串
__unicode__  是转换成unicode
__repr__  是转换成机器看的字符串'''