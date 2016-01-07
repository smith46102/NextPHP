
import os, re, threading;

import php_syntax;

'''
	
	When Scaner scans file - it makes mini-format
		- remove \n\r
		- clean comments
		- break in new lines by ';' '{}'
		- then scan code

	Scaner scans project and collects php entities:

	- File [name]
		- Constant [name, line]
		- Variable [name, line]
		- Function [name, signature, line]
		- Namespace [name, line]
		- Class [name, parent, line, namespace]
			- Static property [name, line]
			- Static method [name, line]
			- Object property [name, line]
			- Object method [name, line]

	Completer uses Scaner to get completions for different situations and contexts
	Completer will use [line] to detect scope and visibility of completion

'''


class File:


	project = None;
	path = '';

	variables = None;
	functions = None;
	classes = None;
	constants = None;
	namespaces = None;

	class_scope = None;
	func_scope = None;
	namespace_scope = '';


	def __init__(self, path, project = None):
		self.path = path;
		self.project = project;
		self.variables = [];
		self.functions = [];
		self.classes = [];
		self.constants = [];
		self.namespaces = [];


	def __str__(self):
		return "[php file] path=" + self.path;

	
	def log(self):
		print('---------------------');
		print(self);
		for v in self.variables: v.log('  ');
		for f in self.functions: f.log('  ');
		for c in self.classes: c.log('  ');
		for o in self.constants: o.log('  ');
		for n in self.namespaces: n.log('  ');


	def scan(self):
		content = self.read_and_clear()
		if content != False:
			self.clear_entities();
			self.scan_entities(content);


	def clear_entities(self):
		self.class_scope = None;
		self.func_scope = None;
		self.namespace_scope = '';
		self.variables = [];
		self.functions = [];
		self.classes = [];
		self.constants = [];
		self.namespaces = [];
		

	def read_and_clear(self):
		file = self.path;
		size = os.path.getsize(file);
		if size > 50000:
			return False;

		# read
		content = '';
		lines = open(file, 'rU');
		for line in lines:
			content += line;

		# clean
		content = re.sub(r"(\<\?php|\?\>)", "", content);
		content = re.sub(r"\/\/(.*?)\n", "", content);
		content = re.sub(r"[\t]", "", content);
		content = re.sub(r"[\n\r]", " ", content);
		content = re.sub(r"\/\*(.*?)\*\/", "", content);
		content = re.sub(r"{", "\n{\n", content);
		content = re.sub(r";", ";\n", content);
		content = re.sub(r"}", "}\n", content);
		content = re.sub(r"(^|\n)[ ]*", "\n", content);
		return content;


	def scan_entities(self, content):
		lines = content.split('\n');
		self.namespace_scope = '';

		for line in lines:
			if line == '{':
				# scope
				pass;
			elif line == '}':
				# scope
				pass;
			elif re.search(r"(function|class|interface|namespace|const|public|protected|private|static)", line):
				if self.scan_function(line):
					continue;
				if self.scan_class(line):
					continue;
				if self.scan_namespace(line):
					continue;
				if self.scan_const(line):
					continue;
			else:
				# scan other variables and properties and define-consts
				pass;


	def scan_function(self, line):
		match = re.search(r"function\s+(\w+)\s*\((.*?)\)", line);
		if not match:
			return False;

		name = match.group(1);
		signature = match.group(2);
		static = "static" in line;
		public = "public" in line;
		func = php_syntax.PHPFunction(name, self.path, signature, static, public);

		if self.class_scope:
			self.class_scope.functions.append(func);
		else:
			self.functions.append(func);

		self.func_scope = func;
		return True;


	def scan_class(self, line):
		match = re.search(r"class\s+(\w+)", line);
		if not match:
			return False;
		
		name = match.group(1);
		match = re.search(r"extends\s+(\w+)", line);
		extends = match.group(1) if match else None;

		cl = php_syntax.PHPClass(name, self.path, self.namespace_scope, extends);
		self.classes.append(cl);
		self.class_scope = cl;
		return True;


	def scan_namespace(self, line):
		match = re.search(r"namespace\s+([\w\\]+)", line);
		if not match:
			return False;

		name = match.group(1);
		nm = php_syntax.PHPNamespace(name, self.path);
		self.namespaces.append(nm);
		self.namespace_scope = nm.name;
		return nm;


	def scan_const(self, line):
		pass;



class Project:

	folders = None;
	files = None;

	def __init__(self, folders):
		self.folders = folders;
		self.files = [];

	def scan(self):
		for folder in self.folders:
			files = self._getFilesFromFolder(folder);
			for fileName in files:
				file = self._scanFile(fileName);
				file and self.files.append(file);

	def log(self):
		print("project log. folders: ");
		print(self.folders);
		for file in self.files:
			file.log();

	def _getFilesFromFolder(self, dir_name, *args):
		list = [];
		mask = '(php)';
		for file in os.listdir(dir_name):
			node = os.path.join(dir_name, file);

			if os.path.isfile(node):
				fname, fext = os.path.splitext(node);
				if re.search(mask, fext):
					list.append(node);

			elif os.path.isdir(node):
				# exclude git hidden folder
				if not re.search('^\.', file):
					list += self._getFilesFromFolder(node, *args);

		return list

	def _scanFile(self, name):
		file = File(name, self);
		file.scan();
		return file;

	def getVariables(self, scope):
		pass;

	def getConstants(self):
		pass;

	def getClasses(self, path):
		pass;

	def getNamespaces(self, path):
		pass;

	def getFunctions(self):
		pass;

	def getClassProperties(self, name):
		pass;

	def getClassFunctions(self, name):
		pass;
