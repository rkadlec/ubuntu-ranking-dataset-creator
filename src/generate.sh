python create_ubuntu_dataset.py "$@" --output 'train.csv' 'train'
python create_ubuntu_dataset.py "$@" --output 'test.csv' 'test'
python create_ubuntu_dataset.py "$@" --output 'valid.csv' 'valid'
