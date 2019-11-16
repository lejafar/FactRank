from factrank.log import init_package_logger
from factrank.options import Options
from factrank.factnet import FactNetBert

def main():
    options = Options().parse()
    init_package_logger(options)
    factnet = FactNetBert(options)
    factnet.fit()

if __name__ == "__main__":
    main()
