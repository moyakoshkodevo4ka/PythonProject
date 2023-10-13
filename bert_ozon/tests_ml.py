import os
from pathlib import Path
import json
root_dir = Path(__file__).parent.parent.parent.resolve()  # directory of source root


def model_weights_check():
    weights_path = Path(root_dir)
    weights_path /= Path('Projects')
    weights_path /= Path('bert_ozon/src/TESTING/model_weights/model')
    return os.stat(weights_path).st_size


def dictionary_correctness_check():
    product_path = Path(root_dir)
    product_path /= Path('Projects')
    product_path /= Path('bert_ozon/src/TESTING/example_product.json')

    with open(product_path) as f:
        dictionary = json.load(f)

    keys = ["name", "description", "size", "marketplace"]

    try:
        for key in keys:
            value = dictionary[key]
    except KeyError:
        return False
    return True


if __name__ == '__main__':
    if model_weights_check():
        print('OK')
    else:
        print("Start train the model")

    if dictionary_correctness_check():
        print("OK")
    else:
        print("Make correct dictionary")