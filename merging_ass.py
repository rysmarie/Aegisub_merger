import re
import os
import argparse


def copy_to_style(source):
    copied_texts = ''
    try:
        with open(source, 'r') as f:
            for line in f:
                copied_texts += line
                if re.search('^Format\: ', line):
                    break

    except OSError:
        print("{} not exists.".format(fname))
        raise

    return copied_texts


def get_styles(source):
    styles = []
    try:
        with open(source, 'r') as f:
            for line in f:
                if re.search('^Style\: ', line):
                    styles.append(line.split(','))
    except OSError:
        print("{} not exists.".format(fname))
        raise

    return styles


def get_dialogues(source):
    dialogue = []
    try:
        with open(source, 'r') as f:
            for line in f:
                if re.search('^Dialogue\: ', line):
                    dialogue.append(line.split(','))
    except OSError:
        print("{} not exists.".format(fname))
        raise

    return dialogue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Aegisub merging program')
    parser.add_argument('--folder', '-f', type=str,
                        help='folder name where Aegisub files are stored')
    parser.add_argument('--files', '-n', type=str, nargs='*',
                        help='file names of Aegisub which you want to merge')
    parser.add_argument('--setpos', '-s', type=float,
                        nargs=2, help='set position same.')
    parser.add_argument('--output', '-o', type=str,
                        default='merged_subtitle.ass', help='the name of output Aegisub file')
    args = parser.parse_args()

    if args.folder:
        files = os.listdir(args.folder)
    elif args.files:
        files = args.files
    else:
        print('At least one option (-f or -n) is needed.')
        os.sys.exit()

    styles = []
    stylenames = []
    dialogues = []
    head_to_style = ''
    position_re1 = re.compile(r'{\\pos\(\d+')
    position_re2 = re.compile(r'\d+\)}')
    for filename in files:
        head_to_style = copy_to_style(filename)
        style = get_styles(filename)
        for s in style:
            if s[0] not in stylenames:
                stylenames.append(s[0])
                styles.append(s)
        dialogues += get_dialogues(filename)
    dialogues = sorted(dialogues, key=lambda x: x[2])

    with open(args.output, 'w') as f:
        f.write(head_to_style)
        for style in styles:
            f.write(','.join(style))

        f.write(
            '\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text')
        for dialogue in dialogues:
            if args.setpos:
                dialogue[-2] = position_re1.sub(
                    r'{{\pos({}'.format(args.setpos[0]), dialogue[-2])
                dialogue[-1] = position_re2.sub(r'{})}}'.format(
                    args.setpos[1]), dialogue[-1])

            f.write(','.join(dialogue))
