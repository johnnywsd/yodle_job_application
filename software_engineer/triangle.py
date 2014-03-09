import sys


def foo(input_file_path):
    triangle = []
    with open(input_file_path, 'r') as input:
        for line in input:
            triangle.append([int(x) for x in line.split()])
    curr_max = [triangle[0][0]]
    prev_max = [triangle[0][0]]
    num_line = len(triangle)
    i = 1
    while i < num_line:
        curr_max = [None] * (len(prev_max) + 1)
        j = 0
        num_item_prev = len(prev_max)
        num_item_curr = num_item_prev + 1
        while j < num_item_curr:
            if j == 0:
                curr_max[j] = prev_max[j] + triangle[i][j]
            elif 0 < j < num_item_curr - 1:
                curr_max[j] = max(prev_max[j - 1],
                                  prev_max[j]) + triangle[i][j]
            else:
                curr_max[j] = prev_max[j - 1] + triangle[i][j]
            j += 1
        prev_max = curr_max
        i += 1
    return max(curr_max)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        msg = 'Usage: python trangle.py <inputfile>'
        print msg
        exit(1)
    rtn = foo(sys.argv[1])
    print 'result: %s' % str(rtn)
