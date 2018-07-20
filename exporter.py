import argparse
import json
import os
from canvas import Canvas
from string_matcher import StringMatcher
import PDF

commands = ['quizzes']

# TODO : Fix implementation
def quizzes(args):
    """
    This function blah ...

    Args:
        assignmentId (str|int): Unique Canvas ID for the assignment to grade.
        files (list of str):    List of the files containing the quizzes
        usernames (str):        Path to text document containing usernames of students.
    
    Returns:
        blah

    Blah:
        blah
    """

    canvas_conf = loadConfig(args.canvas_config)
    c = Canvas(conf["token"], conf["course_id"], conf["URL"])
    students = c.getStudents()

    with open(args.students) as f:

        grades = {}
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            student = line
            grades[student] = line

        files = [args.solution]
        for student in students:
            student_id = student["id"]
            username = student["login_id"]
            fname = "%s%s.pdf" % (args.folder, username)

            if not os.path.isfile(fname):
                print("File %s does not exist. " % fname)
                grade = 0
            else:
                grade = grades[username]
                files.append(c.uploadFileToSubmission(fname, args.assignment_id, student_id))

            print(c.gradeAssignmentAndComment(student_id, args.assignment_id, grade, files=files))

def quizzes_parser(parser):
    parser.add_argument("assignment_id", help="Unique Canvas ID for the assignment to grade")
    parser.add_argument("folder", help="Path to folder containing all of the quizzes. End with a \"/\".")
    parser.add_argument("usernames", help="Path to text document containing usernames of students,  with their corresponding grade next to their usernames seperated by a space.")
    parser.add_argument("canvas_config", help="Path to configuration file containing token and canvas URL")
    parser.add_argument("solution", nargs="?", help="Optional solution file to attach to each comment")
    parser.add_argument("comment", nargs="?", help="Optional comment to comment on each submission")
    parser.add_argument('-f', nargs = '*', dest = 'files', help = 'List of files contained within the given folder parameter to scan and grade', default = None)

# TODO : Implement, will be used for uploading autolab grades to Canvas. 
def autolab_parser(parser):
    parser.add_argument("assignment_id", help="Unique Canvas ID for the assignment to grade")
    parser.add_argument("grades", help="Path to CSV file exported from autolab containing the grades to the assignment.")
    parser.add_argument("config", help="Path to configuration file containing token and canvas URL")

"""
 HELPER FUNCTIONS: 
"""

def loadConfig(config):
    """
    This function loads a config file into a JSON for use with our program.

    Args:
        config (str): Path to config file including JSON
    
    Returns:
        JSON containing our configuration data    
    """
    with open(config) as conf:
        return json.load(conf)

def main():
    __globals__ = globals()
    descr = "Use to automate grading for Canvas"
    parser = argparse.ArgumentParser(description=descr)
    subparsers = parser.add_subparsers()
    for cmd in commands:
        cmdf = __globals__[cmd]
        subp = subparsers.add_parser(cmd, help=cmdf.__doc__)
        __globals__[cmd + '_parser'](subp)
        subp.set_defaults(func=cmdf)
    args = parser.parse_args()

    if 'func' in args:
        args.func(args)
    else:
        parser.error("Please speecify at least one command")


if __name__ == "__main__":
    main()