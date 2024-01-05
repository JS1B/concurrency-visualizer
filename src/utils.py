from dataclasses import dataclass

def load_config(path='config.yaml'):
    import yaml
    with open(path, 'r') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
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