from setuptools import find_packages, setup


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


version_file = 'mmseg/version.py'


def get_version():
    with open(version_file, 'r') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


def parse_requirements(fname='requirements.txt', with_version=True):
    import sys
    from os.path import exists
    import re

    require_fpath = fname

    def parse_line(line):
        """Parse information from a line in a requirements text file."""
        line = line.strip()
        if not line or line.startswith('#'):
            return
        if line.startswith('-r '):  # Allow nested requirements files
            target = line.split(' ', 1)[1]
            for info in parse_require_file(target):
                yield info
        else:
            # Remove versioning from the package if needed
            if with_version:
                yield line
            else:
                # Strip version specifiers like >=, ==, >, <=
                match = re.match(r'^([a-zA-Z0-9_\-\.\[\]]+)', line)
                if match:
                    yield match.group(1)

    def parse_require_file(fpath):
        if not exists(fpath):
            return
        with open(fpath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    for item in parse_line(line):
                        yield item

    return list(gen_packages_items())


if __name__ == '__main__':
    setup(
        name='mmsegmentation',
        version=get_version(),
        description='Open MMLab Semantic Segmentation Toolbox and Benchmark',
        long_description=readme(),
        long_description_content_type='text/markdown',
        author='MMSegmentation Authors',
        author_email='openmmlab@gmail.com',
        keywords='computer vision, semantic segmentation',
        url='http://github.com/open-mmlab/mmsegmentation',
        packages=find_packages(exclude=('configs', 'tools', 'demo')),
        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        license='Apache License 2.0',
        setup_requires=parse_requirements('requirements/build.txt'),
        tests_require=parse_requirements('requirements/tests.txt'),
        install_requires=parse_requirements('requirements/runtime.txt'),
        extras_require={
            'all': parse_requirements('requirements.txt'),
            'tests': parse_requirements('requirements/tests.txt'),
            'build': parse_requirements('requirements/build.txt'),
            'optional': parse_requirements('requirements/optional.txt'),
        },
        ext_modules=[],
        zip_safe=False)
