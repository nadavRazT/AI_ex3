import sys


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    is_disk_on_peg = []
    isnt_disk_on_peg = []

    domain_file.write("Propositions:\n")
    for disk in disks:
        curr_pos = []
        curr_neg = []
        for peg in pegs:
            curr_pos.append(disk + "_" + peg)
            curr_neg.append("not_" + disk + "_" + peg)
            domain_file.write(curr_pos[-1] + " " + curr_neg[-1] + " ")
        is_disk_on_peg.append(curr_pos)
        isnt_disk_on_peg.append(curr_neg)

    domain_file.write("\nActions:\n")
    for disk_idx, disk in enumerate(disks):
        for peg_1_idx, peg_1 in enumerate(pegs):
            for peg_2_idx, peg_2 in enumerate(pegs):
                if peg_1 == peg_2:
                    continue
                domain_file.write("Name: M_" + disk + "from" + peg_1 + "to" + peg_2 + "\n")
                domain_file.write("pre: " + is_disk_on_peg[disk_idx][peg_1_idx] + " ")
                for i in range(disk_idx):
                    domain_file.write(isnt_disk_on_peg[i][peg_1_idx] + " " + isnt_disk_on_peg[i][peg_2_idx] + " ")
                domain_file.write("\nadd: " + is_disk_on_peg[disk_idx][peg_2_idx] + " " + isnt_disk_on_peg[disk_idx][peg_1_idx] + "\n")
                domain_file.write("delete: " + is_disk_on_peg[disk_idx][peg_1_idx] + " " + isnt_disk_on_peg[disk_idx][peg_2_idx] + "\n")
    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    is_disk_on_peg = []
    isnt_disk_on_peg = []
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file

    for disk in disks:
        curr_pos = []
        curr_neg = []
        for peg in pegs:
            curr_pos.append(disk + "_" + peg)
            curr_neg.append("not_" + disk + "_" + peg)
        is_disk_on_peg.append(curr_pos)
        isnt_disk_on_peg.append(curr_neg)

    problem_file.write("Initial state: ")
    for i in range(n_):
        problem_file.write(is_disk_on_peg[i][0] + " ")
    for i in range(n_):
        for j in range(1, m_):
            problem_file.write(isnt_disk_on_peg[i][j] + " ")
    problem_file.write("\nGoal state: ")
    for i in range(n_):
        problem_file.write(is_disk_on_peg[i][m_ - 1] + " ")
    problem_file.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
