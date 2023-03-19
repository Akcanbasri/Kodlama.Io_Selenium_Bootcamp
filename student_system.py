import sys

# A list to store the information of all students
students_info = list()


# Function to display the available operations
def system_ope():
    print("""********************************
    1- Add student
    2- Delete student
    3- Add more than one student
    4- Show all students
    5- Delete students more than one
    'Q' or 'q' to quit from system. 
    ********************************""")


# Function to add a single student to the list
def add_student():
    try:
        student_id = int(input("Enter student id"))
        name = input("Enter name")
        last_name = input("Enter last name")
        into_list = list()
        into_list.append(student_id)
        into_list.append(name)
        into_list.append(last_name)
        students_info.append(into_list)
        print("Student is added to system. \n")
    except ValueError:
        print("ID number can not be string")


# Function to delete a single student from the list
def delete_student():
    id = int(input("Enter id which you want to delete from system: "))
    for student in students_info:
        if student[0] == id:
            students_info.remove(student)
            print("Student is deleted.")
            return
    print("Student is not found! ")


# Function to add multiple students to the list
def add_more_student():
    num = input("how many student you would like to add? ")
    i = 0
    while i < int(num):
        try:
            student_id = int(input("Enter student id"))
            name = input("Enter name")
            last_name = input("Enter last name")
            into_list = list()
            into_list.append(student_id)
            into_list.append(name)
            into_list.append(last_name)
            students_info.append(into_list)
            print("Student is added to system. \n")
        except ValueError:
            print("ID number can not be string")
        i += 1
    print(f"Total {num} students is added to system.")


# Function to display all students in the list
def show_students():
    print("---------------Student lists---------------")
    for i, j, k in students_info:
        print(i, j, k)


# Function to delete multiple students from the list
def delete_more_students():
    num = int(input("how many student you would like to delete? "))
    i = 0
    while i < num:
        id = int(input("Enter id which you want to delete from system: "))
        for student in students_info:
            if student[0] == id:
                students_info.remove(student)
                print("Student is deleted.")
                break
        else:
            print("Student is not found!")
        i += 1
    print(f"Total {num} students is deleted to system.")


# Main function that drives the program
def main():
    print(students_info)
    system_ope()

    while True:
        operation = input("Enter Which process number:  ")
        if operation.upper() == 'Q':
            sys.exit()
        elif operation == '1':
            add_student()
        elif operation == '2':
            delete_student()
        elif operation == '3':
            add_more_student()
        elif operation == '4':
            show_students()
        elif operation == '5':
            delete_more_students()
        else:
            sys.stderr.write("Wrong process number.")
            sys.stderr.flush()


if __name__ == '__main__':
    main()
