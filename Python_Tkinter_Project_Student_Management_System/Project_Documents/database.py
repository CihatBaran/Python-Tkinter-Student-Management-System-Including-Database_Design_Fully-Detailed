import mysql.connector
import cv

class schema:
    def __init__(self,host,user,password):
        self.set_host = host
        self.set_user = user
        self.set_password = password


        self.con = mysql.connector.connect(
            host=self.set_host,
            user=self.set_user,
            passwd=self.set_password)
        self.cursor = self.con.cursor()

        query = "show schemas"
        self.cursor.execute(query)
        self.rows = self.cursor.fetchall()

        self.con.commit()
        self.con.close()

    def check_schema(self):
        for i in self.rows:
            if (i == ('mydb',)):
                return True
        return False

class database_connection:
    def __init__(self, host, user, password):
        self.set_host = host
        self.set_user = user
        self.set_password = password

        self.con = mysql.connector.connect(
            host=self.set_host,
            user=self.set_user,
            passwd=self.set_password)

        self.cursor = self.con.cursor()
        self.__create_tables()
        self.con.commit()
        self.con.close()

    def __create_tables(self):
        query = cv.CREATE_SCHEMA
        self.cursor.execute(query)
        self.cursor.execute(self.__get_student())
        self.cursor.execute(self.__get_course())
        self.cursor.execute(self.__get_professor())
        self.cursor.execute(self.__get_username())
        self.cursor.execute(self.__get_grade())

    def __get_student(self):
        return cv.CREATE_STUDENT_TABLE

    def __get_course(self):
        return cv.CREATE_COURSE_TABLE

    def __get_professor(self):
        return cv.CREATE_PROFESSOR_TABLE

    def __get_username(self):
        return cv.CREATE_USERNAME_AND_PASSWORD_TABLE

    def __get_grade(self):
        return cv.CREATE_GRADE_TABLE

class add_random_data:
    def __init__(self, host, user, password):
        self.set_host = host
        self.set_user = user
        self.set_password = password

        self.con = mysql.connector.connect(
            host=self.set_host,
            user=self.set_user,
            passwd=self.set_password)

        self.cursor = self.con.cursor()
        self.totallines = []
        with open("randomData.txt", "r") as file:
            all_file = file.readlines()
            for line in all_file:
                if (line != ""):
                    self.totallines.append(line)
        for i in self.totallines:
            i = i.strip("\n")
            self.cursor.execute(i)
            #this is the part that I write all the queries, before that to not use empty statement
            #I used strip, then all the random datas were edited to database.
        self.con.commit()
        self.con.close()



class reach_tables_data:
    def __init__(self, host, user, password):
        self.set_host = host
        self.set_user = user
        self.set_password = password


    def course_table(self):
        con = mysql.connector.connect(
            host=self.set_host,
            user=self.set_user,
            passwd=self.set_password)
        cursor = con.cursor()
        query = "select * from `mydb`.`Course`"
        cursor.execute(query)
        rows = cursor.fetchall()
        con.commit()
        con.close()
        return rows

    def grade_table(self):
        con = mysql.connector.connect(
            host=self.set_host,
            user=self.set_user,
            passwd=self.set_password)
        cursor = con.cursor()
        query = "select * from `mydb`.`grade`"
        cursor.execute(query)
        rows = cursor.fetchall()
        con.commit()
        con.close()
        return rows

    def professor_table(self):
        con = mysql.connector.connect(
            host=self.set_host,
            user=self.set_user,
            passwd=self.set_password)
        cursor = con.cursor()
        query = "select * from `mydb`.`Professor`"
        cursor.execute(query)
        rows = cursor.fetchall()
        con.commit()
        con.close()
        return rows

    def student_table(self):
        con = mysql.connector.connect(
            host=self.set_host,
            user=self.set_user,
            passwd=self.set_password)
        cursor = con.cursor()
        query = "select * from `mydb`.`Student`"
        cursor.execute(query)
        rows = cursor.fetchall()
        con.commit()
        con.close()
        return rows

    def username_and_password(self):
        con = mysql.connector.connect(
            host=self.set_host,
            user=self.set_user,
            passwd=self.set_password)
        cursor = con.cursor()
        query = "select * from `mydb`.`usernameandpassword`"
        cursor.execute(query)
        rows = cursor.fetchall()
        con.commit()
        con.close()
        return rows

    def get_course_id_list(self):
        course_id = self.course_table()
        course_id_list = []
        for id in course_id:
            course_id_list.append(id[0])
        return course_id_list

    def grade_table_column_list(self,request):
        self.request = request
        grade_data = self.grade_table()
        if (self.request == "Student_Number"):
            student_id_list = []
            for id in grade_data:
                student_id_list.append(id[0])

            return student_id_list
        elif(self.request == "Professor_ID"):
            professor_id_list = []
            for id in grade_data:
                professor_id_list.append(id[2])

            return professor_id_list

        elif (self.request == "Course_ID"):
            course_id_list = []
            for id in grade_data:
                course_id_list.append(id[1])

            return course_id_list

    def get_professor_id_list(self):
        professor_id = self.professor_table()
        professor_id_list = []
        for id in professor_id:
            professor_id_list.append(id[0])

        return professor_id_list

    def get_student_id_list(self):
        student_id = self.student_table()
        student_id_list = []
        for id in student_id:
            student_id_list.append(id[0])
        return student_id

    def UsernamePasswordList(self):
        usernameAndPassword = self.username_and_password()
        myList = []
        for id in usernameAndPassword:
            myList.append([id[0],id[2],id[1]])
        return myList


class User:

    def __init__(self, username, password,type):
        self.username = username
        self.password = password
        self.type = type

    def __str__(self):
        return "{} {} {}".format(self.username, self.password,self.type)

    def __repr__(self):
        return str(self)

class PasswordData:

    def __init__(self,text,host,user,password):
        self.text = text
        self.set_host = host
        self.set_user = user
        self.set_password = password


        self.users = self.read()


    def read(self):
        # with open(self.text, "r") as f:
        #     text = f.read()
        # lines = text.splitlines()
        # return list([User(*line.split()) for line in lines])
        userlist = []
        database = reach_tables_data(self.set_host,self.set_user,self.set_password)
        userData = database.UsernamePasswordList()
        for data in userData:
            new_user = User(data[0],data[1],data[2])
            userlist.append(new_user)
        return userlist

    def user_exists(self, username):
        for user in self.users:
            if (user.username == username and user.type == self.text):
                return True
        else:
            return False

    def username_matches_password(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password and user.type == self.text:
                return True
        else:
            return False

