﻿import subprocess
import os.path
import locale

class Engine:
    def __init__(self, cmd, connect=True, debug=False):
        self.cmd = cmd
        self.debug = debug
        if connect:
            self.connect()
        else:
            self.proc = None
            self.name = None

    def connect(self, listener=None):
        if self.debug: listener = print
        cwd = os.path.dirname(self.cmd)
        self.proc = subprocess.Popen([self.cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd if cwd != '' else None)

        cmd = 'usi'
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

        while True:
            self.proc.stdout.flush()
            line = self.proc.stdout.readline()
            if line == '':
                raise EOFError()
            line = line.strip()
            if line[:7] == b'id name':
                self.name = line[8:].decode('ascii')
            elif line == b'usiok':
                break
        if listener:
            listener(self.name)

    def usi(self, listener=None):
        if self.debug: listener = print
        cmd = 'usi'
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

        lines = []
        while True:
            self.proc.stdout.flush()
            line = self.proc.stdout.readline()
            if line == '':
                raise EOFError()
            line = line.strip().decode(locale.getpreferredencoding())
            if listener:
                listener(line)
            if line == 'usiok':
                break
            lines.append(line)
        return lines

    def setoption(self, name, value, listener=None):
        if self.debug: listener = print
        cmd = 'setoption name ' + name + ' value ' + str(value)
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode(locale.getpreferredencoding()) + b'\n')
        self.proc.stdin.flush()

    def isready(self, listener=None):
        if self.debug: listener = print
        cmd = 'isready'
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

        while True:
            self.proc.stdout.flush()
            line = self.proc.stdout.readline()
            if line == '':
                raise EOFError()
            line = line.strip().decode('shift-jis')
            if listener:
                listener(line)
            if line == 'readyok':
                break

    def usinewgame(self, listener=None):
        if self.debug: listener = print
        cmd = 'usinewgame'
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

    def position(self, moves=None, sfen="startpos", listener=None):
        if self.debug: listener = print
        cmd = 'position ' + sfen
        if moves:
            cmd += ' moves ' + ' '.join(moves)
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

    def go(self, ponder=False, btime=None, wtime=None, byoyomi=None, binc=None, winc=None, nodes=None, listener=None):
        if self.debug: listener = print
        cmd = 'go'
        if ponder:
            cmd += ' ponder'
        if btime is not None:
            cmd += ' btime ' + str(btime)
        if wtime is not None:
            cmd += ' wtime ' + str(wtime)
        if byoyomi is not None:
            cmd += ' byoyomi ' + str(byoyomi)
        else:
            if binc is not None:
                cmd += ' binc ' + str(binc)
            if winc is not None:
                cmd += ' winc ' + str(winc)
        if nodes is not None:
            cmd += ' nodes ' + str(nodes)
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

        while True:
            self.proc.stdout.flush()
            line = self.proc.stdout.readline()
            if line == '':
                raise EOFError()
            line = line.strip().decode(locale.getpreferredencoding())
            if listener:
                listener(line)
            if line[:8] == 'bestmove':
                items = line[9:].split(' ')
                if len(items) == 3 and items[1] == 'ponder':
                    return items[0], items[2]
                else:
                    return items[0], None

    def go_mate(self, byoyomi=None, listener=None):
        if self.debug: listener = print
        cmd = 'go mate'
        if byoyomi is not None:
            cmd += ' ' + str(byoyomi)
        else:
            cmd += ' infinite'
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()
        while True:
            self.proc.stdout.flush()
            line = self.proc.stdout.readline()
            if line == '':
                raise EOFError()
            line = line.strip().decode(locale.getpreferredencoding())
            if listener:
                listener(line)
            if line[:9] == 'checkmate':
                items = line[10:]
                return items

    def ponderhit(self, listener=None):
        if self.debug: listener = print
        cmd = 'ponderhit'
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

    def stop(self, listener=None):
        if self.debug: listener = print
        cmd = 'stop'
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

    def gameover(self, result=None, listener=None):
        if self.debug: listener = print
        cmd = 'gameover'
        if result:
            cmd += ' ' + result
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        self.proc.stdin.flush()

    def quit(self, listener=None):
        if self.debug: listener = print
        cmd = 'quit'
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode('ascii') + b'\n')
        try:
            self.proc.stdin.flush()
        except BrokenPipeError:
            pass
        self.proc.wait()
        self.proc = None

    def eval(self, listener=None):
        if self.debug:
            listener = print
        cmd = "eval"
        if listener:
            listener(cmd)
        self.proc.stdin.write(cmd.encode("ascii") + b"\n")
        self.proc.stdin.flush()

        while True:
            self.proc.stdout.flush()
            line = self.proc.stdout.readline()
            if line == "":
                raise EOFError()
            line = line.strip().decode("shift-jis")
            if listener:
                listener(line)
            if line[0:6] == "eval =":
                return line.split(" ")[2]
