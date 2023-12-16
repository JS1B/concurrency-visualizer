def load_config(path='config.yaml'):
    import yaml
    with open(path, 'r') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
    return config