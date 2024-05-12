from hakoirimusume.db import DB

db = DB("test.db")
# db.setup()
db.print_table()
# db.remove_user("test_user")
print(db.get_state("test_user"))
db.set_state("test_user", 1)
db.set_authority_level("test_user", 2)
db.print_table()
# db.add_user("test_user")
# db.print_table()
