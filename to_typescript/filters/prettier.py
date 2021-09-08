import os.path

from to_typescript.core.filter import FilterAbstract


class FilterApplyPrettierIfPossible(FilterAbstract):
    OUT_DIRECTORY = 'output'

    def apply(self):
        prettier_relative_path = os.path.join('node_modules', '.bin',
                                              'prettier')
        prettier_path = os.path.join(self.OUT_DIRECTORY,
                                     prettier_relative_path)
        if os.path.exists(prettier_path):
            print(
                f'Found \x1b[34m{prettier_relative_path}'
                f'\x1b[0m inside output directory. Applying prettier...'
            )

            os.chdir(self.OUT_DIRECTORY)
            exit_code = os.spawnl(os.P_WAIT, f'./{prettier_relative_path}',
                                  prettier_relative_path, '--write', '.')
            if exit_code == 0:
                print('Prettier \x1b[32msuccessfully\x1b[0m applied')
            else:
                print(
                    f'Prettier \x1b[31failed\x1b[0m with exit code: '
                    f'\x1b[34m{exit_code}\x1b[0m'
                )

            os.chdir('..')
            return

        print(
            f'\x1b[31mCannot find\x1b[0m '
            f'\x1b[34m{prettier_relative_path}\x1b[0m inside output directory'
        )
