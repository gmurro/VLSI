import sys

txt_path = "../data/instances_txt"
dzn_path = "../CP/instances_dzn"

#if len(sys.argv) != 3:
    #print('Usage: instances_to_dzn.py <input_file> <output_file>')
    #sys.exit(1)

# if you want to do all the files decomment and indent correctly
for k in range(1, 41):
    output_filename = dzn_path + "/ins-" + str(k) + ".dzn"
    input_filename = txt_path + "/ins-" + str(k) + ".txt"

#input_filename = txt_path + "/" + sys.argv[1]
#output_filename = dzn_path + "/" + sys.argv[2]

    with open(input_filename, 'r') as f_in:
        lines = f_in.read().splitlines()

        w = lines[0]
        n = lines[1]

        x = []
        y = []

        for i in range(int(n)):
            split = lines[i + 2].split(' ')
            x.append(int(split[0]))
            y.append(int(split[1]))

        l_max = sum(y)

        # compute order of magnitude of w
        len_w = len(str(w))
        mag_w = 10**len_w

        with open(output_filename, 'w+') as f_out:
            f_out.write('w = {};\n'.format(w))
            f_out.write('n = {};\n'.format(n))

            f_out.write('x = {};\n'.format(x))
            f_out.write('y = {};\n'.format(y))
            f_out.write('l_max={};\n'.format(l_max))
            f_out.write('mag_w={};\n'.format(mag_w))
