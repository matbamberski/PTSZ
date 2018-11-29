import sys
import os
import time
import subprocess
import csv

def read_file(source):
    file = open(source).read().split()
    return iter(file)


class Task:
    def __init__(self, id, p, a, b):
        self.p = p
        self.a = a
        self.b = b
        self.id = id
        self.diff = a - b
        self.mul = a * b
        self.par = self.diff * self.mul

    def __str__(self):
        return (self.p, self.a, self.b)

    def __repr__(self):
        return "(%s, %s, %s)" % (self.p, self.a, self.b)



def read_objects(file):
    num_instances = int(next(file))
    instances = {}
    for tasks in range(num_instances):
        tasks_num = int(next(file))
        instances[tasks] = [Task(t, int(next(file)), int(next(file)), int(next(file))) for t in range(tasks_num)]
    return instances


def sum_p(task_list):
    return sum(list(map(lambda x: x.p, task_list)))


def due_date(tasklist, h):
    return int(sum_p(tasklist) * h)


def count_penalty(timestamp, d, task):
    if timestamp > d:
        # tardiness
        return (timestamp - d) * task.b
    elif timestamp == d:
        return 0
    else:
        # earliness
        return (d - timestamp) * task.a


def count_time(timestamp, task):
    timestamp += task.p
    return timestamp


def evaluate_sort(tasklist, h, d):
    timestamp = 0
    score = 0
    for task in tasklist:
        timestamp = count_time(timestamp, task)
        score += count_penalty(timestamp, d, task)
    return score

def read_solution(idx, n, k, h, tasklist):
    os.chdir("output/"+idx)
    filename = str(n) + "_" + str(k) + "_" + str(int(h*10))
    #file = read_file(filename + ".txt")
    if os.path.exists(filename + ".txt"):
        file = read_file(filename + ".txt")
    elif os.path.exists(filename + ".csv"):
        file = read_file(filename + ".csv")
    else: print("File not founded")

    result_1 = int(next(file))
    os.chdir("../..")
    return result_1, [tasklist[int(next(file))] for i in range(n)]

def execute_one(testname, n, k, h):
    os.chdir(testname)
    start = time.time()
    subprocess.call(["sh", testname+".sh", str(n), str(k), str(int(h*10))])
    end = time.time()
    print('Odpalono:', testname, 'czas:',end-start)
    os.chdir("..")
    return end-start

def read_boundaries(n, k, h):
    os.chdir("projekt1/boundaries")
    boundaries = {}
    file = read_file("boundaries" + str(n) + ".txt")
    for i in range(10):
        boundaries[i] = {0.2:int(next(file)), 0.4:int(next(file)), 0.6:int(next(file)), 0.8:int(next(file))}
    os.chdir("../..")
    return boundaries[k][h]

def calc_error(n, k, h, res):
    boundary = read_boundaries(n, k, h)
    return (res-boundary)*100/boundary, boundary


def main(idx, n, k, h):
    os.chdir("input")
    instance = read_objects(read_file("sch" + str(n) + ".txt"))[k]
    os.chdir("..")
    elapsed_time = execute_one(idx, n, k, h)
    res, solution = read_solution(idx, n, k, h, instance)
    d = due_date(solution, h)
    checker_res = evaluate_sort(solution, h, d)
    error, boundary = calc_error(n, k, h, checker_res)
    fields = [idx, str(n), str(k), str(h), str(boundary), str(res), str(checker_res), str(error), str(elapsed_time)]
    with open(r'test_results.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    print("N:", n)
    print("K:", k)
    print("H:", h)
    print("Boundary:", boundary)
    print("Result:", res, checker_res)
    print("Error:", error)
    print("Time:", elapsed_time)


if __name__ == "__main__":
    if len(sys.argv)>4:
        main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])/10)
    else:
        print("Error: bad number of arguments, need 4")