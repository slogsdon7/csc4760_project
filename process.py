from preprocessing import db_loader

if __name__ == '__main__':
    db_loader.load_categories()
    db_loader.load_data()