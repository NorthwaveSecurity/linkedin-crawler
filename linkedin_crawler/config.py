import os
from dynaconf import Dynaconf
from pathlib import Path

dir = Path(__file__).parent

settings = Dynaconf(
    envvar_prefix="LINKEDIN_CRAWLER",
    settings_files=[
        dir / '../settings.toml',
        Path(os.environ['HOME']) / '.config' / 'linkedin_crawler' / 'settings.toml'
    ],
)
