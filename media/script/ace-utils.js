function guessMode(filename) {
   var mode;
   if (/^.*\.js$/i.test(filename)) {
	mode = "javascript";
   } else if (/^.*\.xml$/i.test(filename)) {
	mode = "xml";
   } else if (/^.*\.html$/i.test(filename)) {
	mode = "html";
   } else if (/^.*\.css$/i.test(filename)) {
	mode = "css";
   } else if (/^.*\.py$/i.test(filename)) {
	mode = "python";
   } else if (/^.*\.php$/i.test(filename)) {
	mode = "php";
   } else if (/^.*\.cs$/i.test(filename)) {
	mode = "csharp";
   } else if (/^.*\.java$/i.test(filename)) {
	mode = "java";
   } else if (/^.*\.rb$/i.test(filename)) {
	mode = "ruby";
   } else if (/^.*\.(c|cpp|h|hpp|cxx)$/i.test(filename)) {
	mode = "c_cpp";
   } else if (/^.*\.coffee$/i.test(filename)) {
	mode = "coffee";
   } else if (/^.*\.(pl|pm)$/i.test(filename)) {
	mode = "perl";
   } else if (/^.*\.(ml|mli)$/i.test(filename)) {
	mode = "ocaml";
   } else if (/^.*\.(hs|lhs)$/i.test(filename)) {
	mode = "haskell";
   } else if (/^.*\.R$/.test(filename)) {
	mode = "r";
   } else if (/^.*\.thy$/.test(filename)) {
	mode = "isabelle";
   } else  {
	mode = "plain_text";
   }

   return "ace/mode/" + mode;
}
