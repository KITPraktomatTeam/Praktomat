define("ace/mode/isabelle_highlight_rules",["require","exports","module","ace/lib/oop","ace/mode/text_highlight_rules"], function(require, exports, module) {
"use strict";

var oop = require("../lib/oop");
var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;

var IsabelleHighlightRules = function() {

    var keyword1 = (
        "theory|text|section|subsection|subsubsection|paragraph|" +
        "lemma|proof|assume|then|have|from|with|qed|by|next|using|let|unfolding|hence|" +
        "moreover|ultimately|also|finally|" +
        "locale|abbreviation|definition|fun|function|declare|inductive|inductive_set|" +
        "primrec|datatype|type_synonym|notation|context|interpretation|interpret"
    );
    var keyword2 = (
        "assumes|shows|obtains|and|begin|end|where|in|fixes|for|imports"
    );
    var keyword3 = (
        "case|show|thus|obtain|fix"
    );
    var improper = (
        "apply|done|prefer|defer"
    );
    var builtinVariables = (
        "?thesis"
    );

    var keywordMapper = this.createKeywordMapper({
        "keyword": keyword1,
        "keyword.operator": keyword2,
        "constant.language": keyword3,
        "variable.language": builtinVariables,
        "invalid.deprecated": improper
    }, "identifier");

    this.$rules = {
        "start" : [
            {
                token : "constant.character.escape",
                regex : '\\\\<open>',
                push  : "fact",
            },
            {
                token : "string.quoted",
                regex : '"',
                push  : "string"
            },
            {
                token : keywordMapper,
                regex : "[a-zA-Z_$\\?][a-zA-Z0-9_$]*\\b"
            },
            {
                token : "constant.character.escape",
                regex : '\\\\<\\^?[a-zA-Z0-9]+>'
            },
            {
                token : "text",
                regex : "\\s+"
            },
            {
                defaultToken : "text"
            }
        ],
        "fact" : [
            {
                token : "constant.character.escape",
                regex : '\\\\<close>',
                next  : "pop"
            },
            {
                token : "constant.character.escape",
                regex : '\\\\<open>',
                push  : "fact"
            },
            {
                token : "constant.character.escape",
                regex : '\\\\<\\^?[a-zA-Z0-9]+>'
            },
            {
                defaultToken : "string.regexp"
            }
        ],
        "string" : [
            {
                token : "string.quoted",
                regex : '"',
                next  : "pop"
            },
            {
                token : "constant.character.escape",
                regex : '\\\\<\\^?[a-zA-Z0-9]+>'
            },
            {
                defaultToken : "string"
            }
        ]
    };

    this.normalizeRules();

};

oop.inherits(IsabelleHighlightRules, TextHighlightRules);

exports.IsabelleHighlightRules = IsabelleHighlightRules;
});

define("ace/mode/isabelle",["require","exports","module","ace/lib/oop","ace/mode/text","ace/mode/isabelle_highlight_rules"], function(require, exports, module) {
"use strict";

var oop = require("../lib/oop");
var TextMode = require("./text").Mode;
var IsabelleHighlightRules = require("./isabelle_highlight_rules").IsabelleHighlightRules;

var Mode = function() {
    this.HighlightRules = IsabelleHighlightRules;
};
oop.inherits(Mode, TextMode);

(function() {


}).call(Mode.prototype);

exports.Mode = Mode;
});
