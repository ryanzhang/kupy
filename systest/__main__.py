from kupy.config import configs
from kupy.logger import logger
from kupy.dbadaptor import DBAdaptor

def main() -> None:  # pragma: no cover
    logger.info("Start systest")
    logger.debug(f"{configs['postgres_host'].data}")
    db =DBAdaptor()
    print(db)
    print("pass")


if __name__ == "__main__":  # pragma: no cover
    main()
