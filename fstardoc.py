from pprint import pprint as print


class fst_parsed:

    def __init__(self):
        self.comment_nest_level = 0
        self.current_comment = []
        self.current_code = []
        self.current_comment_type = None
        self.output = []

    def _state(self):
        state = {
            'comment_nest_level': self.comment_nest_level,
            'current_comment': self.current_comment,
            'current_code': self.current_code,
            'current_comment_type': self.current_comment_type,
            'output': self.output,
        }
        return state

    def error(self, err, line=None):
        from pprint import pformat
        if line is not None:
            err += '\nLine: ' + repr(line)
        err += '\nState: ' + pformat(self._state())
        assert False, err

    def flush(self):
        if self.comment_nest_level != 0:
            self.error("Invalid nesting")
        if self.current_comment_type is None:
            # TODO: FIXME
            pass
        elif self.current_comment_type == 'fsdoc':
            # TODO: FIXME
            pass
        elif self.current_comment_type == 'fslit':
            # TODO: FIXME
            pass
        elif self.current_comment_type == 'h1':
            # TODO: FIXME
            pass
        elif self.current_comment_type == 'h2':
            # TODO: FIXME
            pass
        elif self.current_comment_type == 'h3':
            # TODO: FIXME
            pass
        elif self.current_comment_type == 'normal':
            # TODO: FIXME
            pass
        else:
            self.error("Unknown comment type.")
        # TODO: FIXME
        print(self._state())
        self.comment_nest_level = 0
        self.current_comment = []
        self.current_code = []
        self.current_comment_type = None
        pass

    def flush_if_not_and_set(self, typ):
        if self.current_comment_type != typ:
            self.flush()
            self.current_comment_type = typ

    def add_line(self, line):
        if '\n' in line:
            self.error("Newline in line", line)
        if self.comment_nest_level > 0:
            nest_level = self.comment_nest_level - line.count('*)')
            if nest_level > 0:
                self.current_comment.append(line)
            elif nest_level == 0:
                self.current_comment.append(
                    line[:line.rindex('*)')].rstrip())
            else:
                self.error("More close comments than opened", line)
            self.comment_nest_level = nest_level
            return
        elif self.comment_nest_level < 0:
            self.error("More close comments than opened", line)
        # Now we are at 0 nesting
        if line.strip() == '':
            self.current_code.append('')
            self.flush()
            return
        if line.startswith('/// '):
            self.flush_if_not_and_set('fslit')
            self.current_comment.append(line[len('/// '):])
            return
        lstripped = line.strip(' \t')
        if lstripped.startswith('(***** '):
            # heading 3
            self.flush_if_not_and_set('h3')
            if lstripped.count('(*') == lstripped.count('*)'):
                self.current_comment.append(
                    lstripped[len('(***** '):-len('*)')])
                self.flush()
            else:
                self.error("Unsupported multiline heading", line)
            return
        if lstripped.startswith('(**** '):
            # heading 2
            self.flush_if_not_and_set('h2')
            if lstripped.count('(*') == lstripped.count('*)'):
                self.current_comment.append(
                    lstripped[len('(**** '):-len('*)')])
                self.flush()
            else:
                self.error("Unsupported multiline heading", line)
            return
        if lstripped.startswith('(*** '):
            # heading 1
            self.flush_if_not_and_set('h3')
            if lstripped.count('(*') == lstripped.count('*)'):
                self.current_comment.append(
                    lstripped[len('(*** '):-len('*)')])
                self.flush()
            else:
                self.error("Unsupported multiline heading", line)
            return
        if lstripped.startswith('(** '):
            # fsdoc comment
            self.flush_if_not_and_set('fsdoc')
            if lstripped.count('(*') == lstripped.count('*)'):
                self.current_comment.append(
                    lstripped[len('(** '):-len('*)')])
                self.flush()
            else:
                self.current_comment.append(
                    lstripped[len('(** '):])
                self.comment_nest_level = (
                    lstripped.count('(*') - lstripped.count('*)'))
            return
        if lstripped.startswith('(*'):
            # normal comment
            self.flush_if_not_and_set('normal')
            if lstripped.count('(*') == lstripped.count('*)'):
                self.current_comment.append(
                    lstripped[len('(*'):-len('*)')])
                self.flush()
            else:
                self.current_comment.append(
                    lstripped[len('(*'):])
                self.comment_nest_level = (
                    lstripped.count('(*') - lstripped.count('*)'))
            return
        if lstripped.startswith('//'):
            # normal comment
            self.flush_if_not_and_set('normal')
            self.current_comment.append(lstripped[len('//'):])
            return
        # not comment
        if self.comment_nest_level == 0:
            if lstripped.count('(*') == lstripped.count('*)'):
                self.current_code.append(lstripped)
            elif lstripped.count('(*') > lstripped.count('*)'):
                self.current_code.append(lstripped[:lstripped.index('(*')])
                self.add_line(lstripped[:lstripped.index('(*')])
            else:
                self.error("More closes than opens", line)
            return
        self.error("Impossible to reach", line)

    def generate_output(self):
        self.flush()
        return '\n'.join(self.output)


def fst2md(fst):
    fst = fst.split('\n')
    fstp = fst_parsed()

    for line in fst:
        fstp.add_line(line)

    return fstp.generate_output()


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input",
                        type=argparse.FileType('r'),
                        help="Input F* file")
    args = parser.parse_args()

    fst = args.input.read()
    args.input.close()
    print(fst2md(fst))


if __name__ == '__main__':
    main()
