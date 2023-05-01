# -*- coding:utf-8 -*-
import os
import uvicorn
from src.config.environments import config


def main():
    os.environ["ENV"] = config.ENV
    os.environ["DEBUG"] = "True" if config.ENV != "prod" else "False"
    uvicorn.run(
        app="src.server:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=False,
        workers=1,
    )


if __name__ == "__main__":
    main()
