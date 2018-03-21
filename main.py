from spider import Student

if __name__ == '__main__':
    # initialize
    student = Student('username', 'password')
    student.get_personal_info()
    student.show_personal_info()
    student.get_class_table()
    student.get_personal_score()
    student.show_jidian()
    student.score_to_GPA()
    student.show_personal_score()
    student.show_class_table()
    student.score_pdf_generate()
    student.get_personal_credit_required()
    student.get_personal_credit_electives()
    student.show_credit_required()
    student.show_credit_electives()

    # Don't forget this
    student.exit()
