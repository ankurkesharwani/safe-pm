from managers.setup_manager import SetupManager
from managers.utils.path_utils import get_db_path


def attach_subparser(program_subparser):
    setup_program_parser = program_subparser.add_parser("setup", help="Create a new database for storing passwords")
    setup_program_parser.add_argument("--db", type=str, help="name of the database to create", required=True)


def execute(args):
    setup_manager = SetupManager(db_path=get_db_path(), db_name=args.db)
    return setup_manager.do_setup()
