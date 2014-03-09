import sys
import os

def parser(input_file_path):
    c_dict = {}
    j_dict = {}
    max_num_preferenct = -sys.maxint - 1
    with open(input_file_path) as input:
        for line in input:
            if line.startswith('C'):
                item = {}
                arr = line.split()
                key = arr[1]
                H = int(arr[2][2:])
                E = int(arr[3][2:])
                P = int(arr[4][2:])
                item['key'] = key
                item['H'] = H
                item['E'] = E
                item['P'] = P
                c_dict[key] = item
            elif line.startswith('J'):
                item = {}
                arr = line.split()
                key = arr[1]
                H = int(arr[2][2:])
                E = int(arr[3][2:])
                P = int(arr[4][2:])
                preference = arr[5].split(',')
                item['key'] = key
                item['H'] = H
                item['E'] = E
                item['P'] = P
                item['preference'] = preference
                max_num_preferenct = max(max_num_preferenct, len(preference))
                j_dict[key] = item
        return (c_dict, j_dict, max_num_preferenct)


def preference_score(c_dict, j_dict):
    for key in j_dict:
        item = j_dict[key]
        preference = item['preference']
        score = {}
        for circle in preference:
            H = item['H'] * c_dict[circle]['H']
            E = item['E'] * c_dict[circle]['E']
            P = item['P'] * c_dict[circle]['P']
            tmp_score = H + E + P
            score[circle] = tmp_score
        item['preference_score'] = score


def add_additional_properties(c_dict, j_dict):
    for key in c_dict:
        item = c_dict[key]
        item['candidates'] = []
    for key in j_dict:
        item = j_dict[key]
        item['is_assigned'] = False


def assign(c_dict, j_dict, num_jugglers_per_circle, max_num_preferenct):
    for i in range(max_num_preferenct):
        for key in j_dict:
            juggler = j_dict[key]
            if juggler['is_assigned']:
                continue
            preference = juggler['preference']
            pref = preference[i]
            _max_n_list(c_dict[pref]['candidates'],
                        juggler, pref, num_jugglers_per_circle)
        for key in c_dict:
            circle = c_dict[key]
            candidates = circle['candidates']
            for juggler in candidates:
                juggler['is_assigned'] = True


def assign_left_jugglers(c_dict, j_dict, num_jugglers_per_circle):
    jugglers_left = []
    for key in j_dict:
        item = j_dict[key]
        if not item['is_assigned']:
            jugglers_left.append(item)

    circles_left = []
    for key in c_dict:
        item = c_dict[key]
        if len(item['candidates']) < num_jugglers_per_circle:
            circles_left.append(item)

    if circles_left and jugglers_left:
        curr_circle = circles_left.pop()
        while circles_left or jugglers_left:
            while len(curr_circle['candidates']) < num_jugglers_per_circle \
                    and jugglers_left:
                juggler = jugglers_left.pop()
                juggler['is_assigned'] = True
                curr_circle['candidates'].append(juggler)
            if circles_left:
                curr_circle = circles_left.pop()


def _max_n_list(mylist, juggler, pref, n):
    num = len(mylist)
    if num < n:
        mylist.append(juggler)
    else:
        tmp = juggler
        for i in range(n):
            if mylist[i]['preference_score'][pref] \
                    < tmp['preference_score'][pref] \
                    and not mylist[i]['is_assigned']:
                mylist[i], tmp = tmp, mylist[i]


def output(c_dict, j_dict, output_file_path):
    output_list = []
    for key_c in c_dict:
        circle = c_dict[key_c]
        candidates = circle['candidates']
        candidates_list = []
        for candidate in candidates:
            key_j = candidate['key']
            preference_score = candidate['preference_score']
            candidates_prefs = []
            for key in preference_score:
                score = preference_score[key]
                pref_score_str = '%s:%s' % (key, score)
                candidates_prefs.append(pref_score_str)
            candidates_prefs_str = ' '.join(candidates_prefs)
            candidates_list.append(key_j + ' ' + candidates_prefs_str)
        candidates_list_str = ', '.join(candidates_list)
        item_str = '%s %s' % (key_c, candidates_list_str)
        output_list.append(item_str)
    output_list = sorted(output_list, key=_get_key_num, reverse=True)
    output_list_str = os.linesep.join(output_list)
    with open(output_file_path, 'w+') as output:
        output.write(output_list_str)


def _get_key_num(item):
    key_str = item.split()[0]
    return int(key_str[1:])


def get_email(c_dict):
    key = 'C1970'
    candidates = c_dict[key]['candidates']
    count = 0
    for candidate in candidates:
        tmp = int(candidate['key'][1:])
        count += tmp
    return '%d@yodle.com' % count


if __name__ == '__main__':
    if len(sys.argv) != 3:
        msg = 'Usage: python jugglefest.py <input_file> <output_file>'
        print msg
        exit(1)
    c_dict, j_dict, max_num_preferenct = parser(sys.argv[1])
    # print max_num_preferenct
    num_jugglers_per_circle = len(j_dict) / len(c_dict)
    preference_score(c_dict, j_dict)
    add_additional_properties(c_dict, j_dict)
    assign(c_dict, j_dict, num_jugglers_per_circle, max_num_preferenct)
    assign_left_jugglers(c_dict, j_dict, num_jugglers_per_circle)
    output(c_dict, j_dict, sys.argv[2])
    email = get_email(c_dict)
    print 'result: %s' % email
