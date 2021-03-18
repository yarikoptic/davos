from subprocess import CalledProcessError

from davos import davos


class DavosError(Exception):
    pass


class DavosParserError(DavosError):
    # class for errors raised during the parsing step
    pass


class SmugglerError(DavosError):
    # class for errors raised during the smuggle step
    pass


class InstallerError(SmugglerError, CalledProcessError):
    # class for problems encountered by the installer (pip/conda) itself
    # (e.g., failed to connect to internet, resolve environment, find
    # package with given name, etc.)
    def __init__(self, msg, *args, output=None, stderr=None,
                 show_stdout=None):
        cpe_or_retcode = args[0]
        if isinstance(cpe_or_retcode, CalledProcessError):
            returncode = cpe_or_retcode.returncode
            cmd = cpe_or_retcode.cmd
            output = output or cpe_or_retcode.output
            stderr = stderr or cpe_or_retcode.stderr
        else:
            try:
                returncode, cmd = args
            except ValueError:
                # TODO: raise this from the line of the constructor's
                #  signature
                raise TypeError(
                    "InstallerError requires, at minimum, either a "
                    "'subprocess.CalledProcessError' object or a return code "
                    "[int] and cmd [str]"
                ) from None
        super().__init__(returncode=returncode, cmd=cmd, output=output,
                         stderr=stderr)
        self.msg = msg
        if show_stdout is None:
            if davos.suppress_stdout and output is not None:
                show_stdout = True
            else:
                show_stdout = False
        if show_stdout:
            # TODO: change this so the command's stdout is inserted as
            #  a FrameSummary object in the stack trace at the line
            #  where davos.run_shell_command was called
            self.args = (*self.args, output)

    def __str__(self):
        return self.msg + '\n\t' + super().__str__()


class OnionError(SmugglerError):
    # general class for errors related to the Onion structure/object
    pass


class OnionTypeError(OnionError, TypeError):
    # class analogous to TypeError, but for invalid params specified in
    # Onion construct
    pass


class OnionValueError(OnionError, ValueError):
    # class analogous to ValueError, but for bad values passed to Onion
    # construct params
    pass


class OnionSyntaxError(OnionError, SyntaxError):
    # class analogous to SyntaxError, but for invalid Syntax in Onion
    # construct
    def __init__(self, msg, *args, filename=None, lineno=None, offset=None):
        # TODO: format kwargs into tuple to init super() with correct
        #  format to raise at specific location, see
        #  https://stackoverflow.com/questions/33717804/python-raise-syntaxerror-with-lineno
        super().__init__(msg, *args)
        self.filename = filename
        self.lineno = lineno
        self.offset = offset