from dataclasses import dataclass

def load_config(local_config_path='config.yaml'):
    default_config_path = 'default_config.yaml'
    import yaml
    with open(default_config_path, 'r') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)

    # Try to load config.yaml
    try:
        with open(local_config_path, 'r') as f:
            local_config = yaml.load(f.read(), Loader=yaml.FullLoader)
    except FileNotFoundError:
        print('No config.yaml found, using default config.')

    # Update config with local_config
    config.update(local_config)
    
    return config

@dataclass
class PositionType:
    x0: float
    y0: float
    width: float
    height: float

    def __post_init__(self) -> None:
        self.x1 = self.x0 + self.width
        self.y1 = self.y0 + self.height
        self.x_center = self.x0 + self.width/2
        self.y_center = self.y0 + self.height/2

    def __repr__(self) -> str:
        return f'PositionType(x0={self.x0}, y0={self.y0}, width={self.width}, height={self.height})'
    
    def __iter__(self) -> iter:
        yield self.x0
        yield self.y0
        yield self.width
        yield self.height