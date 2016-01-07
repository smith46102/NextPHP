
import php_syntax;
import php_scaner;


def test_entity():
	ent = php_syntax.PHPEntity('ent', '../testing/test.php');
	ent.log();

def test_variable():
	var = php_syntax.PHPVariable('var', '../testing/test.php', 'class.func');
	var.log();

def test_file():
	file = php_scaner.File('../testing/test.php');
	file.log();

def test_project():
	project = php_scaner.Project(['../']);
	project.scan();
	project.log();


# print('================== test php2 ===================');
# test_entity();
# test_variable();
# test_file();

print('================== test php2 project ===========');
test_project();

