top = '.'
out = 'build'

name=arxiv_download

def options(opt):
    opt.load('python')

def configure(conf):
    conf.load('python')
    conf.check_python_version((2,7,0))

    try:
        conf.check_python_module('urllib')
    except:
        print('%s missing: pip install urllib'%name)

    try:
        conf.check_python_module('feedparser')
    except:
        print('%s missing: pip install feedparser'%name)

    try:
        conf.check_python_module('wget')
    except:
        print('%s missing: pip install wget'%name)

        try:
        conf.check_python_module('argparse')
    except:
        print('%s missing: pip install argparse'%name)

def build(bld):
    bld(features='py',
        source=bld.path.ant_glob('arxiv.py'),
        install_from='.')
