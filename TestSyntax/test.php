
// booleans ==========================================

True False false true TRUE FALSE null Null NULL;

// int numbers =======================================

0;
1234; // decimal number
-123; // a negative number
0123; // octal number (equivalent to 83 decimal)
0x1A; // hexadecimal number (equivalent to 26 decimal)
0b11111111; // binary number (equivalent to 255 decimal)


// strings ===========================================

'this is a simple string';

'You can also have embedded newlines in 
strings this way as it is
okay to do';

// Outputs: Arnold once said: "I'll be back"
'Arnold once said: "I\'ll be back"';

// Outputs: You deleted C:\*.*?
'You deleted C:\\*.*?';

// Outputs: You deleted C:\*.*?
'You deleted C:\*.*?';

// Outputs: This will not expand: \n a newline
'This will not expand: \n a newline';

// Outputs: Variables do not $expand $either
'Variables do not $expand $either';


// vars ================================================

$_SESSION $var $name;


// function definition =================================

function make();

function make(Model $model, &$var, $type = 123, $name = 'test');

function make_model($a = true, array $b = null, $c, callable $d = null) {}

// fails 

function;

function () {}

function public make() {}

function public(int $a,,b,c,) {}

function make(Model $model = nu, &$var, $type = 0.123, $name = 'test');

function make_model($a, array $b >= null, $c, callable $d null) {}
