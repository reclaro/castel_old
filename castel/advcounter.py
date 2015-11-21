import argparse
import sys

from configparser import SafeConfigParser
from stevedore import driver


def get_config_section(config_file, section, key):
    config = SafeConfigParser()
    config.read(config_file)
    return config.get(section, key)

def get_driver(config_file):
    """
    Load the backend driver according to the value specified in the
    configuration file
    """
    driver_name = get_config_section(config_file, 'default', 'driver')
    mgr = driver.DriverManager(namespace='advcounter.plugin',
                               name=driver_name,
                               invoke_on_load=True,
                               )
    return mgr.driver    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Name of the file to parse")
    parser.add_argument("-d",
                        "--decimal",
                        metavar="integer",
                        default=1,
                        type=int,
                        help="Number of decimal digits returned by"
                             " calculations, default is 1")
    parser.add_argument("-c",
                        "--config",
                        default="advcounter.conf",
                        help="Path for the config file, default"
                              " is advcounter.conf")
                        
    args = parser.parse_args()
    engine_driver = get_driver(args.config)
    engine_driver.precision = args.decimal
    try:
        wr = engine_driver.open_file(args.file)
    except FileNotFoundError:
        print("File \'%s\' not found" % args.file)
        sys.exit(1)

#    print("PARAMETRI file %s decimal %s %s" % (args.file, args.decimal, s.precision))
    print("Number of lines", engine_driver.get_total_lines(wr))
    wr.seek(0)
    print("Number of words", engine_driver.get_total_words(wr))
    wr.seek(0)
    print("most common letter", engine_driver.most_common_letter(wr))
    wr.seek(0)
    print("average letter per word", engine_driver.get_avg_letters_per_word(wr))
    print("total letters", engine_driver.get_total_letters(wr))
    wr.close()
