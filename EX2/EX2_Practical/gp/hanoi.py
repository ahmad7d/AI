import itertools
import sys


def format_propositions(props):
    return " ".join(props) + "\n"


def format_action(name, preconds, adds, dels):
    return f"Name: {name}\npre: {' '.join(preconds)}\nadd: {' '.join(adds)}\ndelete: {' '.join(dels)}\n"


def add_move_action(file, disk, src, dest):
    name = f'MOVE_{disk}_FROM_{src}_TO_{dest}'
    pre = ['u' + disk, 'u' + dest, f'{disk}-{src}']
    add = [f'{disk}-{dest}', f'u{src}']
    delete = ['u' + dest, f'{disk}-{src}', ]
    file.write(format_action(name, pre, add, delete))


def move_disk_between_disks(file, disks):
    for disk, disk1, disk2 in itertools.combinations(disks, r=3):
        add_move_action(file, disk, disk1, disk2)
        add_move_action(file, disk, disk2, disk1)

def move_disk_between_pegs(file, disks, pegs):
    for disk in disks:
        for peg1, peg2 in itertools.combinations(pegs, r=2):
            add_move_action(file, disk, peg1, peg2)
            add_move_action(file, disk, peg2, peg1)

def move_disk_between_disk_and_peg(file, disks, pegs):
    for main_disk in disks:
        for disk, peg in itertools.product(disks, pegs):
            if int(main_disk.split("_")[1]) < int(disk.split("_")[1]):
                add_move_action(file, main_disk, peg, disk)
                add_move_action(file, main_disk, disk, peg)

def create_actions_section(file, disks, pegs):
    file.write("Actions:\n")
    move_disk_between_disks(file, disks)
    move_disk_between_pegs(file, disks, pegs)
    move_disk_between_disk_and_peg(file, disks, pegs)


def generate_propositions(file, disks, pegs):
    file.write(f'Propositions:\n')
    l = [f'{disk}-{peg}' for disk, peg in itertools.product(disks, pegs)]
    l += [f'{disk1}-{disk2}' for disk1, disk2 in itertools.combinations(disks, r=2)]
    l += ['u' + disk for disk in disks]
    l += ['u' + peg for peg in pegs]
    file.write(format_propositions(l))


def create_domain_file(domain_file_name, n, m):
    disks = [f"d_{i}" for i in range(n)]
    pegs = [f"p_{i}" for i in range(m)]
    with open(domain_file_name, 'w') as file:
        generate_propositions(file, disks, pegs)
        create_actions_section(file, disks, pegs)


def generate_peg_state(disks, pegs, peg_index):
    state = []
    for d1, d2 in itertools.combinations(disks, 2):
        if int(d2.split("_")[1]) == int(d1.split("_")[1]) + 1:
            state.append(f"{d1}-{d2}")
    state.append(f"{disks[-1]}-{pegs[peg_index]}")
    return state


def list_empty_pegs(pegs):
    return [f"u{peg}" for peg in pegs[1:]]


def create_problem_file(problem_file_name, n, m):
    disks = [f"d_{i}" for i in range(n)]
    pegs = [f"p_{i}" for i in range(m)]
    with open(problem_file_name, 'w') as file:
        initial_state = generate_peg_state(disks, pegs, 0) + list_empty_pegs(pegs) + ["ud_0"]
        goal_state = generate_peg_state(disks, pegs, m - 1)
        file.write("Initial state: " + " ".join(initial_state) + "\n")
        file.write("Goal state: " + " ".join(goal_state) + "\n")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(sys.argv[1])
    m = int(sys.argv[2])

    domain_file_name = f'hanoi_{n}_{m}_domain.txt'
    problem_file_name = f'hanoi_{n}_{m}_problem.txt'

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
