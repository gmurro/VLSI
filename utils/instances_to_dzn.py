import sys

txt_path = "../data/instances_txt"
dzn_path = "../data/instances_dzn"


if len(sys.argv) != 3:
    print('Usage: instances_to_dzn.py <input_file> <output_file>')
    sys.exit(1)


input_filename = txt_path + "/" + sys.argv[1]
output_filename = dzn_path + "/" + sys.argv[2]

with open(input_filename, 'r') as f_in:
    lines = f_in.read().splitlines()

    w = lines[0]
    n = lines[1]

    cx = []
    cy = []

    for i in range(int(n)):
        split = lines[i + 2].split(' ')
        cx.append(int(split[0]))
        cy.append(int(split[1]))

    with open(output_filename, 'w+') as f_out:
        f_out.write('w = {};\n'.format(w))
        f_out.write('n = {};\n'.format(n))

        f_out.write('cx = {};\n'.format(cx))
        f_out.write('cy = {};\n'.format(cy))