import logging

from render.cli import APPFactory
from render.log import setting


def main():
    setting.logging_setting()
    parser = APPFactory.get_parser()
    args = parser.parse_args()
    try:
        print("""
        WELCOME TO RENDER
        """)
        args.func(args)
    except AttributeError:
        parser.print_help()
    except Exception as e:
        logging.error(e, exc_info=True)
        exit(1)


if __name__ == '__main__':
    main()
