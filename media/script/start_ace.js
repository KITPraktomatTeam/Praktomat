/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 *
 * The contents of this file are subject to the Mozilla Public License Version
 * 1.1 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Original Code is Mozilla Skywriter.
 *
 * The Initial Developer of the Original Code is
 * Mozilla.
 * Portions created by the Initial Developer are Copyright (C) 2009
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s):
 *      Fabian Jakobs <fabian AT ajax DOT org>
 *      Kevin Dangoor (kdangoor@mozilla.com)
 *      Julian Viereck <julian DOT viereck AT gmail DOT com>
 *
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 *
 * ***** END LICENSE BLOCK ***** */


define(function(require, exports, module) {

exports.launch = function(env) {
    var canon = require("pilot/canon");
    var event = require("pilot/event");
    var Range = require("ace/range").Range;
    var Editor = require("ace/editor").Editor;
    var Renderer = require("ace/virtual_renderer").VirtualRenderer;
    var theme = require("ace/theme/textmate");
    var EditSession = require("ace/edit_session").EditSession;

    var JavaScriptMode = require("ace/mode/javascript").Mode;
    var CssMode = require("ace/mode/css").Mode;
    var HtmlMode = require("ace/mode/html").Mode;
    var XmlMode = require("ace/mode/xml").Mode;
    var PythonMode = require("ace/mode/python").Mode;
    var PhpMode = require("ace/mode/php").Mode;
    var JavaMode = require("ace/mode/java").Mode;
    var CSharpMode = require("ace/mode/csharp").Mode;
    var RubyMode = require("ace/mode/ruby").Mode;
    var CCPPMode = require("ace/mode/c_cpp").Mode;
    var CoffeeMode = require("ace/mode/coffee").Mode;
    var PerlMode = require("ace/mode/perl").Mode;
    var OcamlMode = require("ace/mode/ocaml").Mode;
    var SvgMode = require("ace/mode/svg").Mode;
    var TextileMode = require("ace/mode/textile").Mode;
    var TextMode = require("ace/mode/text").Mode;
    var UndoManager = require("ace/undomanager").UndoManager;

    var vim = require("ace/keyboard/keybinding/vim").Vim;
    var emacs = require("ace/keyboard/keybinding/emacs").Emacs;

    var keybindings = {
      // Null = use "default" keymapping
      ace: null,
      vim: vim,
      emacs: emacs,
    }

   var modes = {
	   text: new TextMode(),
	   textile: new TextileMode(),
	   svg: new SvgMode(),
	   xml: new XmlMode(),
	   html: new HtmlMode(),
	   css: new CssMode(),
	   javascript: new JavaScriptMode(),
	   python: new PythonMode(),
	   php: new PhpMode(),
	   java: new JavaMode(),
	   ruby: new RubyMode(),
	   c_cpp: new CCPPMode(),
	   coffee: new CoffeeMode(),
	   perl: new PerlMode(),
	   ocaml: new OcamlMode(),
	   csharp: new CSharpMode()
   };
	   
    var docs = {};
	// get text from text areas    
	$("[id^='id_attestfiles'][id$='id']").each(function(index) {
		
		solutionfile_id = $("[id='id_attestfiles-"+index+"-solution_file']")[0].value 
		content = $("[id='id_attestfiles-"+index+"-content']");

		docs[solutionfile_id] = new EditSession(content.text());
		var name = $("#doc > [value="+solutionfile_id+"]").text();

		docs[solutionfile_id].setMode(getMode(name));
		docs[solutionfile_id].setUndoManager(new UndoManager());
		docs[solutionfile_id].on('change',function(){somethingWasChanged = true;});
	});
	// restore text areas   
	$("form").submit(function() {

		$("[id^='id_attestfiles'][id$='id']").each(function(index) {
			solutionfile_id = $("[id='id_attestfiles-"+index+"-solution_file']")[0].value 
			content = $("[id='id_attestfiles-"+index+"-content']");

			content.text(docs[solutionfile_id].getValue());
		});
	});

	

	var container = document.getElementById("editor");
    env.editor = new Editor(new Renderer(container, theme));

    function getMode() {
        return modes[modeEl.value];
    }

    var modeEl = document.getElementById("mode");
    var wrapModeEl = document.getElementById("soft_wrap");
	   
   bindDropdown("doc", function(value) {
        var doc = docs[value];
        env.editor.setSession(doc);

        var mode = doc.getMode();
        if (mode instanceof JavaMode) {
            modeEl.value = "java";
        }
        else if (mode instanceof CssMode) {
            modeEl.value = "css";
        }
        else if (mode instanceof HtmlMode) {
            modeEl.value = "html";
        }
        else if (mode instanceof XmlMode) {
            modeEl.value = "xml";
        }
        else if (mode instanceof PythonMode) {
            modeEl.value = "python";
        }
        else if (mode instanceof PhpMode) {
            modeEl.value = "php";
        }
        else if (mode instanceof JavaScriptMode) {
            modeEl.value = "javascript";
        }
        else if (mode instanceof RubyMode) {
            modeEl.value = "ruby";
        }
        else if (mode instanceof CCPPMode) {
            modeEl.value = "c_cpp";
        }
        else if (mode instanceof CoffeeMode) {
            modeEl.value = "coffee";
        }
        else if (mode instanceof PerlMode) {
            modeEl.value = "perl";
        }
        else if (mode instanceof OcamlMode) {
            modeEl.value = "ocaml";
        }
        else if (mode instanceof CSharpMode) {
            modeEl.value = "csharp";
        }
        else if (mode instanceof SvgMode) {
            modeEl.value = "svg";
        }
        else if (mode instanceof TextileMode) {
            modeEl.value = "textile";
        }
        else {
            modeEl.value = "text";
        }

        if (!doc.getUseWrapMode()) {
            wrapModeEl.value = "off";
        } else {
            wrapModeEl.value = doc.getWrapLimitRange().min || "free";
        }
        env.editor.focus();
    });

    bindDropdown("mode", function(value) {
        env.editor.getSession().setMode(modes[value] || modes.text);
    });

    bindDropdown("theme", function(value) {
        env.editor.setTheme(value);
    });
	

    bindDropdown("keybinding", function(value) {
        env.editor.setKeyboardHandler(keybindings[value]);
    });

    bindDropdown("fontsize", function(value) {
        document.getElementById("editor").style.fontSize = value;
    });
/*
    bindDropdown("tabsize", function(value) {
        env.editor.getSession().setTabSize(value);
	for (var i in docs) {
		docs[i].setTabSize(value);
	}
    });
*/ 

    bindDropdown("soft_wrap", function(value) {
        var session = env.editor.getSession();
        var renderer = env.editor.renderer;
        switch (value) {
            case "off":
                session.setUseWrapMode(false);
                renderer.setPrintMarginColumn(120);
                break;
            case "80":
                session.setUseWrapMode(true);
                session.setWrapLimitRange(80, 80);
                renderer.setPrintMarginColumn(80);
                break;
			case "120":
				 session.setUseWrapMode(true);
				 session.setWrapLimitRange(120, 120);
				 renderer.setPrintMarginColumn(120);
				 break;
            case "free":
                session.setUseWrapMode(true);
                session.setWrapLimitRange(null, null);
                renderer.setPrintMarginColumn(120);
                break;
        }
    });

    bindCheckbox("select_style", function(checked) {
        env.editor.setSelectionStyle(checked ? "line" : "text");
    });

    bindCheckbox("highlight_active", function(checked) {
        env.editor.setHighlightActiveLine(checked);
    });

    bindCheckbox("show_hidden", function(checked) {
        env.editor.setShowInvisibles(checked);
    });

    bindCheckbox("show_gutter", function(checked) {
        env.editor.renderer.setShowGutter(checked);
    });

    bindCheckbox("show_print_margin", function(checked) {
        env.editor.renderer.setShowPrintMargin(checked);
    });

    bindCheckbox("highlight_selected_word", function(checked) {
        env.editor.setHighlightSelectedWord(checked);
    });

    bindCheckbox("show_hscroll", function(checked) {
        env.editor.renderer.setHScrollBarAlwaysVisible(checked);
    });

    bindCheckbox("soft_tab", function(checked) {
        env.editor.getSession().setUseSoftTabs(checked);
    });

    bindDropdown("editor_height", function(value) {
        $("#editor").css("height",value);
	env.editor.resize();
    });

    function bindCheckbox(id, callback) {
        var el = document.getElementById(id);
        var onCheck = function() {
            callback(!!el.checked);
	   		$.Storage.set(id, String(el.checked));
        };
        el.onclick = onCheck;
	   	storred_setting = $.Storage.get(id);
	   	if (storred_setting) el.checked = (storred_setting == "true");
        onCheck();
    }

    function bindDropdown(id, callback) {
        var el = document.getElementById(id);
        var onChange = function() {
            callback(el.value);
			if (id != "doc" && id != "mode") $.Storage.set(id, el.value);
        };
        el.onchange = onChange;
	   	storred_setting = $.Storage.get(id);
	   	if (storred_setting) el.value = storred_setting;
        onChange();
    }

    function onResize() {
        //container.style.width = (document.documentElement.clientWidth) + "px";
        //container.style.height = (document.documentElement.clientHeight - 22) + "px";
        env.editor.resize();
    };

    window.onresize = onResize;
    onResize();

	// doesnt work   
	//window.onresize = env.editor.resize;
	   
   function getMode(filename) {
	   var mode = "text";
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
	   }

	   return modes[mode];
   }
	   
    window.env = env;

};

});
