
class PHPEntity:

	name = '';
	file = '';

	def __init__(self, name, file):
		self.name = name;
		self.file = file;

	def log(self, prefix = ''):
		print(prefix + "[entity] " + self.name);

	def snippet(self):
		return self.name;


class PHPClass(PHPEntity):

	extends = '';
	namespace = '';
	constants = None;
	properties = None;
	functions = None;

	def __init__(self, name, file, namespace = '', extends = ''):
		PHPEntity.__init__(self, name, file);
		self.namespace = namespace;
		self.extends = extends;
		self.constants = [];
		self.properties = [];
		self.functions = [];

	def log(self, prefix = ''):
		str = prefix + "[class] " + self.namespace + "\\" + self.name;
		if self.extends:
			str += ' extends ' + self.extends;
		print(str);
		for p in self.properties: p.log(prefix + '  ');
		for f in self.functions: f.log(prefix + '  ');
		for c in self.constants: c.log(prefix + '  ');


	def snippet(self):
		return self.name;


class PHPFunction(PHPEntity):

	static = False;
	public = True;
	arguments = None;

	def __init__(self, name, file, arguments = '', static = False, public = True):
		PHPEntity.__init__(self, name, file);
		self.arguments = self.parse_arguments(arguments);
		self.static = static;
		self.public = public;

	def log(self, prefix = ''):
		str = "[function] " + self.name + "()";
		if self.public:
			str += " public";
		if self.static:
			str += " static";
		print(prefix + str);

	def parse_arguments(self, arguments):
		pass;

	def snippet(self):
		return self.name;


class PHPVariable(PHPEntity):

	scope = '';

	def __init__(self, name, file, scope = ''):
		PHPEntity.__init__(self, name, file);
		self.scope = scope;

	def log(self, prefix = ''):
		print(prefix + "[var] " + self.name);

	def snippet(self):
		return self.name;


class PHPProperty(PHPEntity):

	static = False;
	public = True;

	def __init__(self, name, file, static = False, public = True):
		PHPEntity.__init__(self, name, file);
		self.static = static;
		self.public = public;

	def snippet(self):
		return self.name;


class PHPNamespace(PHPEntity):

	def __init__(self, name, file):
		PHPEntity.__init__(self, name, file);
		self.name = name.strip('/');

	def snippet(self):
		return self.name;

	def log(self, prefix = ''):
		print(prefix + "[namespace] " + self.name);


class PHPConstant(PHPEntity):

	def snippet(self):
		return self.name;
