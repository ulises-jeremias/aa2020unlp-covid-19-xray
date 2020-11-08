import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Generate splits for datasets")

    parser.add_argument("--seed", type=int, default=42)

    # dataset info
    parser.add_argument("--dataset", type=str, default="", help="Dataset name")
    parser.add_argument("--version", type=str, default="", help="Dataset version")
    parser.add_argument("--data_dir", type=str, default="",
                        help="Directory to load and store data")
    
    # split config
    parser.add_argument("--split", type=str)
    parser.add_argument("--splits_dir", type=str,
                        default="/tmp/splits", help="Output dir to save the splits")
    parser.add_argument("--train_size", type=float, default=0)
    parser.add_argument("--test_size", type=float, default=0.2)
    parser.add_argument("--n_train_per_class", type=int, default=0)
    parser.add_argument("--n_test_per_class", type=int, default=0)
    
    # flags
    parser.add_argument("-w", help="Store new dataset based on generated splits", dest="write_dataset", action="store_true")
    parser.add_argument("--balanced", dest="balanced", action="store_true")
    parser.add_argument("--no-balanced", dest="balanced", action="store_false")
    parser.add_argument("--gs", dest="generate_splits", action="store_true")
    parser.add_argument("--no-gs", dest="generate_splits", action="store_false")

    # default values
    parser.set_defaults(generate_splits=True, balanced=False)

    args = vars(parser.parse_args())

    return args
