import sys
import subprocess
def main():
    parse(sys.argv[1])


def parse(file):
    content =""
    with open(file) as f:
        content = f.readlines()
    print content
    i = 0
    for line in content:
        command("say", line, "-o" + str(i) + line[1:5] + line[-5:-3])
        i += 1

def command(cmd, message, args):

    subprocess.Popen(cmd+" \"%s\""%message +" " +args, shell=True, stdout=subprocess.PIPE).stdout.read()
    return

main()
