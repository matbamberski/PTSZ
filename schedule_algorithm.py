import urllib
from random import shuffle
import operator
import sys
import os

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


def random(task_list):
    return shuffle(task_list)


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


def variable_sort(tasklist, attr, reverse=False):
    return sorted(tasklist, key=operator.attrgetter(attr), reverse=reverse)


def evaluate_sort(tasklist, h, d):
    timestamp = 0
    score = 0
    for task in tasklist:
        timestamp = count_time(timestamp, task)
        score += count_penalty(timestamp, d, task)
    return score


def swap_2_check(tasklist, d):
    timestamp = 0
    i = 0
    while (i + 1 < len(tasklist)):
        temp_time = timestamp
        timestamp = count_time(timestamp, tasklist[i])
        score_1 = count_penalty(timestamp, d, tasklist[i])
        timestamp = count_time(timestamp, tasklist[i + 1])
        score_1 += count_penalty(timestamp, d, tasklist[i + 1])
        # print('score1: ',score_1)

        temp_time = count_time(temp_time, tasklist[i + 1])
        score_2 = count_penalty(temp_time, d, tasklist[i + 1])
        temp_time = count_time(temp_time, tasklist[i])
        score_2 += count_penalty(temp_time, d, tasklist[i])
        # print('score2: ', score_2)

        if score_2 < score_1:
            tasklist[i], tasklist[i + 1] = tasklist[i + 1], tasklist[i]
            timestamp = temp_time
        timestamp -= tasklist[i + 1].p
        # print('time: ', timestamp)
        i += 1
    return tasklist


def schedule_alg(instance, h, d):
    #print('due_date: ', d)
    results = {}
    sort_a = variable_sort(instance, 'a')
    # print('sort_a:', sort_a)
    key_a = evaluate_sort(sort_a, h, d)
    results[key_a] = sort_a
    #print('result a: ', key_a)
    sort_b = variable_sort(instance, 'b', reverse=True)
    key_b = evaluate_sort(sort_b, h, d)
    results[key_b] = sort_b
    #print('result b: ', key_b)
    sort_1 = variable_sort(instance, 'par')
    key_1 = evaluate_sort(sort_1, h, d)
    results[key_1] = sort_1
    #print('result par: ', key_1)
    best_result = 99999999999
    for key in results:
        if key < best_result:
            best_result = key
    # print("Best result: ", best_result, " sort: ", results[best_result])
    bubble = results[best_result]
    for n in range(len(instance)):
        bubble = swap_2_check(bubble, d)
        res = evaluate_sort(bubble, h, d)
        if res == best_result:
            break
        else:
            best_result = res
    #print('result after alg: ', res)
    return best_result, " ".join(str(task.id) for task in bubble)


def main(n, k, h):
    os.chdir("input")
    instances = read_objects(read_file("sch" + str(n) + ".txt"))
    result, schedule = schedule_alg(instances[k], h, due_date(instances[k], h))
    os.chdir("../output")
    if not os.path.exists("109893"):
        os.makedirs("109893")
    os.chdir("109893")
    f = open(str(n) + "_" + str(k) + "_" + str(int(h*10)) + ".txt", "w+")
    f.write(str(result) + "\n")
    f.write(schedule)
    f.close()

if __name__ == "__main__":
    if len(sys.argv)>3:
        main(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])/10)
    else:
        print("Error: bad number of arguments, need 3")