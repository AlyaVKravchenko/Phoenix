import pickle

def save_data(data, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

def load_data(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        print("File not found")
    return {}