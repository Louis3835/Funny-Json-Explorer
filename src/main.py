import argparse
from src.style.Builder import Style_Builder


def parse_args():
    description = "Funny Json Explorer"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-f', '--file', type=str, help='Json file path', required=True)
    parser.add_argument('-s', '--style', type=str, help='style', default='tree')
    parser.add_argument('-i', '--icon-family', type=str, help='icon-family', default='poker-face-icon-family')
    parser.add_argument('-c', '--config', type=str, help='icon family file')
    parser.add_argument('-a', '--available', action='store_const', const=True, default=False, help='print available icon family and styles')
    return parser.parse_args()

def main():
    args = parse_args()
    builder = Style_Builder()
    if args.config is not None:
        builder.load_icon_family(args.config)
    if args.available:
        print(f'available icon families: {builder.available_icon_family()}')
        print(f'available styles: {builder.available_styles()}')

    builder.create_style_node(args.file, args.icon_family, args.style).render_all()


if __name__ == "__main__":
    main()




