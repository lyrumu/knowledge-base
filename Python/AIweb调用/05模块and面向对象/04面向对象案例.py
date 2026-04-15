class Student:
    def __init__(self,name,chinese,math,english):
        self.name=name
        self.chinese = chinese
        self.math = math
        self.english = english
    def __str__(self):
        return f"姓名：{self.name} | 语文：{self.chinese} | 数学：{self.math} | 英语：{self.english}"
    #修改成绩方法
    def update_score(self,chinese=None,math=None,english=None):
        if chinese is not None:
            self.chinese = chinese
        if math is not None:
            self.math = math
        if english is not None:
            self.english = english


class EduManagement:
    system_version = 1.0
    system_name = "教务管理系统"#类属性
    def __init__(self):
        self.student_list=[]

    def add_student(self):
        name = input("请输入学生姓名")
        for s in self.student_list:
            if name == s.name:
                print("学生已在系统中")
                return
        chinese = float(input("请输入语文成绩"))
        math = float(input('请输入数学成绩'))
        english = float(input("请输入英语成绩"))
        if 0<=chinese<=100 and 0<=math<=100 and 0<=english<=100:
            #创建学生实例
            stu = Student(name,chinese,math,english)
            self.student_list.append(stu)
            print("添加成功")
        else:
            print("学生成绩不合理")

    def update_student(self):
        name = input("请输入要修改的学生姓名")
        for s in self.student_list:
            if name == s.name:
                print(f"当前成绩：{s}")
                chinese = float(input("请输入修改后语文成绩"))
                math = float(input('请输入修改后数学成绩'))
                english = float(input("请输入修改后英语成绩"))
                if 0<=chinese<=100 and 0<=math<=100 and 0<=english<=100:
                    #调用学生类的方法
                    s.update_score(chinese,math,english)
                    print("修改成功")
                    print(f"当前成绩：{s}")
                    return
                else:
                    print("学生成绩不合理")
                    return
        print("未找到该学生")

    def delete_student(self):
        name = input("请输入要删除的学生姓名")
        for s in self.student_list:
            if name == s.name:
                self.student_list.remove(s)
                print("删除成功")
                return
        print("未找到该学生 删除失败")

    def find_student(self):
        name = input("请输入查询的学生姓名")
        for s in self.student_list:
            if name == s.name:
                #得益于__str__方法
                print(f"{s}")
                return
        print("未找到学生")

    def list_student(self):
        for s in self.student_list:
            print(s)

    def run(self):
        print(f"欢迎使用{EduManagement.system_name} {EduManagement.system_version}")
        while True:
            print()
            print("###########################################################")
            print("1.添加学生 2.修改学生 3.删除学生 4.查询指定学生 5.查询所有学生 6.退出系统")
            print("###########################################################")
            oper = int(input("请输入操作数字"))
            try:
                match oper:
                    case 1:
                        self.add_student()
                    case 2:
                        self.update_student()
                    case 3:
                        self.delete_student()
                    case 4:
                        self.find_student()
                    case 5:
                        self.list_student()
                    case 6:
                        print("已退出系统")
                        break
                    case _:
                        print("非法操作")
            except Exception as e:
                print(e)

#启动
edu = EduManagement()
edu.run()