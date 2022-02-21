from kupy import *

def main() -> None:  # pragma: no cover
    logger.info("Start systest")
    logger.debug(f"{configs['sqlalchemy_db_string'].data}")
    db =DBAdaptor()
    print(db)
    print("pass")


if __name__ == "__main__":  # pragma: no cover
    main()
