def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input",
                        type=argparse.FileType('r'),
                        help="Input F* file")
    args = parser.parse_args()

    print(args)


if __name__ == '__main__':
    main()
