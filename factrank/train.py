from factrank.log import init_package_logger
from factrank.options import Options
from factrank.factnet import FactNet, FactNetTransformer


def main():
    options = Options().parse()
    init_package_logger(options)
    factnet = FactNet(options)
    factnet.fit()


if __name__ == "__main__":
    main()
