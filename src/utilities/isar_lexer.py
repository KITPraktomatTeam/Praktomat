import re
from pygments.lexers.theorem import IsabelleLexer
from pygments.lexer import RegexLexer, inherit, bygroups, words
from pygments.token import *

from . import encoding

__all__ = ['IsarLexer']

class IsarLexer(IsabelleLexer):
    name = 'Isabelle/Isar'

    keyword_cartouche_text = ('text', 'txt', 'text_raw',
        'chapter', 'section', 'subsection', 'subsubsection',
        'paragraph', 'subparagraph',
    )
    tokens = {
        'root': [
            (words(keyword_cartouche_text, prefix=r'\b', suffix=r'(%\w+)?(\s*\\<open>)'), bygroups(Keyword, Comment.Preproc, Comment), 'cartouche-text'),
            (r'\\<comment>.*$', Comment),
            (r'%\w+', Comment.Preproc),
            (r'\\<open>', String.Other, 'fact'),
            inherit,
        ],
        'cartouche-text': [
            (r'[^\\@]', Comment),
            (r'(@\{)(\w+)', bygroups(String.Other, Keyword), 'antiquotation'),
            (r'\\<open>', Text, '#push'),
            (r'\\<close>', Comment, '#pop'),
            (r'\\<[\^\w]+>', Comment.Symbol),
            (r'\\', Comment),
        ],
        'antiquotation': [
            (r'[^\{\}\\]', Text),
            (r'\{', String.Other, '#push'),
            (r'\}', String.Other, '#pop'),
            (r'\\<[\^\w]+>', String.Symbol),
            (r'\\', Text),
        ],
        'fact': [
            (r'\\<close>', String.Other, '#pop'),
            inherit,
        ],
    }

    def get_tokens_unprocessed(self, text):
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text):
            value = isar_decode(value)
            yield index, token, value


def isar_decode(raw):
    global symbol_table
    if symbol_table is None:
        symbol_table = {}
        for line in symbols_raw.splitlines():
            if line:
                if re.match(r"^#", line):
                    continue
                m = re.match(r"^(\\<.*>)\s+code:\s+0x([0-9a-f]+).*$", line)
                assert m, "Failed to parse " + line
                n = int(m.group(2), 16)
                if n < 0x10000:
                    symbol_table[m.group(1)] = chr(n)

    if isinstance(raw, str):
        raw = encoding.get_unicode(raw)
    def repl(m):
        if m.group(0) in symbol_table:
            return symbol_table[m.group(0)]
        else:
            return m.group(0)
    return re.sub(r"\\<[\^a-zA-Z]+>", repl, raw)


# ~~/etc/symbols from Isabelle2016
symbol_table = None
symbols_raw = """
\<zero>                 code: 0x01d7ec  group: digit
\<one>                  code: 0x01d7ed  group: digit
\<two>                  code: 0x01d7ee  group: digit
\<three>                code: 0x01d7ef  group: digit
\<four>                 code: 0x01d7f0  group: digit
\<five>                 code: 0x01d7f1  group: digit
\<six>                  code: 0x01d7f2  group: digit
\<seven>                code: 0x01d7f3  group: digit
\<eight>                code: 0x01d7f4  group: digit
\<nine>                 code: 0x01d7f5  group: digit
\<A>                    code: 0x01d49c  group: letter
\<B>                    code: 0x00212c  group: letter
\<C>                    code: 0x01d49e  group: letter
\<D>                    code: 0x01d49f  group: letter
\<E>                    code: 0x002130  group: letter
\<F>                    code: 0x002131  group: letter
\<G>                    code: 0x01d4a2  group: letter
\<H>                    code: 0x00210b  group: letter
\<I>                    code: 0x002110  group: letter
\<J>                    code: 0x01d4a5  group: letter
\<K>                    code: 0x01d4a6  group: letter
\<L>                    code: 0x002112  group: letter
\<M>                    code: 0x002133  group: letter
\<N>                    code: 0x01d4a9  group: letter
\<O>                    code: 0x01d4aa  group: letter
\<P>                    code: 0x01d4ab  group: letter
\<Q>                    code: 0x01d4ac  group: letter
\<R>                    code: 0x00211b  group: letter
\<S>                    code: 0x01d4ae  group: letter
\<T>                    code: 0x01d4af  group: letter
\<U>                    code: 0x01d4b0  group: letter
\<V>                    code: 0x01d4b1  group: letter
\<W>                    code: 0x01d4b2  group: letter
\<X>                    code: 0x01d4b3  group: letter
\<Y>                    code: 0x01d4b4  group: letter
\<Z>                    code: 0x01d4b5  group: letter
\<a>                    code: 0x01d5ba  group: letter
\<b>                    code: 0x01d5bb  group: letter
\<c>                    code: 0x01d5bc  group: letter
\<d>                    code: 0x01d5bd  group: letter
\<e>                    code: 0x01d5be  group: letter
\<f>                    code: 0x01d5bf  group: letter
\<g>                    code: 0x01d5c0  group: letter
\<h>                    code: 0x01d5c1  group: letter
\<i>                    code: 0x01d5c2  group: letter
\<j>                    code: 0x01d5c3  group: letter
\<k>                    code: 0x01d5c4  group: letter
\<l>                    code: 0x01d5c5  group: letter
\<m>                    code: 0x01d5c6  group: letter
\<n>                    code: 0x01d5c7  group: letter
\<o>                    code: 0x01d5c8  group: letter
\<p>                    code: 0x01d5c9  group: letter
\<q>                    code: 0x01d5ca  group: letter
\<r>                    code: 0x01d5cb  group: letter
\<s>                    code: 0x01d5cc  group: letter
\<t>                    code: 0x01d5cd  group: letter
\<u>                    code: 0x01d5ce  group: letter
\<v>                    code: 0x01d5cf  group: letter
\<w>                    code: 0x01d5d0  group: letter
\<x>                    code: 0x01d5d1  group: letter
\<y>                    code: 0x01d5d2  group: letter
\<z>                    code: 0x01d5d3  group: letter
\<AA>                   code: 0x01d504  group: letter
\<BB>                   code: 0x01d505  group: letter
\<CC>                   code: 0x00212d  group: letter
\<DD>                   code: 0x01d507  group: letter
\<EE>                   code: 0x01d508  group: letter
\<FF>                   code: 0x01d509  group: letter
\<GG>                   code: 0x01d50a  group: letter
\<HH>                   code: 0x00210c  group: letter
\<II>                   code: 0x002111  group: letter
\<JJ>                   code: 0x01d50d  group: letter
\<KK>                   code: 0x01d50e  group: letter
\<LL>                   code: 0x01d50f  group: letter
\<MM>                   code: 0x01d510  group: letter
\<NN>                   code: 0x01d511  group: letter
\<OO>                   code: 0x01d512  group: letter
\<PP>                   code: 0x01d513  group: letter
\<QQ>                   code: 0x01d514  group: letter
\<RR>                   code: 0x00211c  group: letter
\<SS>                   code: 0x01d516  group: letter
\<TT>                   code: 0x01d517  group: letter
\<UU>                   code: 0x01d518  group: letter
\<VV>                   code: 0x01d519  group: letter
\<WW>                   code: 0x01d51a  group: letter
\<XX>                   code: 0x01d51b  group: letter
\<YY>                   code: 0x01d51c  group: letter
\<ZZ>                   code: 0x002128  group: letter
\<aa>                   code: 0x01d51e  group: letter
\<bb>                   code: 0x01d51f  group: letter
\<cc>                   code: 0x01d520  group: letter
\<dd>                   code: 0x01d521  group: letter
\<ee>                   code: 0x01d522  group: letter
\<ff>                   code: 0x01d523  group: letter
\<gg>                   code: 0x01d524  group: letter
\<hh>                   code: 0x01d525  group: letter
\<ii>                   code: 0x01d526  group: letter
\<jj>                   code: 0x01d527  group: letter
\<kk>                   code: 0x01d528  group: letter
\<ll>                   code: 0x01d529  group: letter
\<mm>                   code: 0x01d52a  group: letter
\<nn>                   code: 0x01d52b  group: letter
\<oo>                   code: 0x01d52c  group: letter
\<pp>                   code: 0x01d52d  group: letter
\<qq>                   code: 0x01d52e  group: letter
\<rr>                   code: 0x01d52f  group: letter
\<ss>                   code: 0x01d530  group: letter
\<tt>                   code: 0x01d531  group: letter
\<uu>                   code: 0x01d532  group: letter
\<vv>                   code: 0x01d533  group: letter
\<ww>                   code: 0x01d534  group: letter
\<xx>                   code: 0x01d535  group: letter
\<yy>                   code: 0x01d536  group: letter
\<zz>                   code: 0x01d537  group: letter
\<alpha>                code: 0x0003b1  group: greek
\<beta>                 code: 0x0003b2  group: greek
\<gamma>                code: 0x0003b3  group: greek
\<delta>                code: 0x0003b4  group: greek
\<epsilon>              code: 0x0003b5  group: greek
\<zeta>                 code: 0x0003b6  group: greek
\<eta>                  code: 0x0003b7  group: greek
\<theta>                code: 0x0003b8  group: greek
\<iota>                 code: 0x0003b9  group: greek
\<kappa>                code: 0x0003ba  group: greek
\<lambda>               code: 0x0003bb  group: greek  abbrev: %
\<mu>                   code: 0x0003bc  group: greek
\<nu>                   code: 0x0003bd  group: greek
\<xi>                   code: 0x0003be  group: greek
\<pi>                   code: 0x0003c0  group: greek
\<rho>                  code: 0x0003c1  group: greek
\<sigma>                code: 0x0003c3  group: greek
\<tau>                  code: 0x0003c4  group: greek
\<upsilon>              code: 0x0003c5  group: greek
\<phi>                  code: 0x0003c6  group: greek
\<chi>                  code: 0x0003c7  group: greek
\<psi>                  code: 0x0003c8  group: greek
\<omega>                code: 0x0003c9  group: greek
\<Gamma>                code: 0x000393  group: greek
\<Delta>                code: 0x000394  group: greek
\<Theta>                code: 0x000398  group: greek
\<Lambda>               code: 0x00039b  group: greek
\<Xi>                   code: 0x00039e  group: greek
\<Pi>                   code: 0x0003a0  group: greek
\<Sigma>                code: 0x0003a3  group: greek
\<Upsilon>              code: 0x0003a5  group: greek
\<Phi>                  code: 0x0003a6  group: greek
\<Psi>                  code: 0x0003a8  group: greek
\<Omega>                code: 0x0003a9  group: greek
\<bool>                 code: 0x01d539  group: letter
\<complex>              code: 0x002102  group: letter
\<nat>                  code: 0x002115  group: letter
\<rat>                  code: 0x00211a  group: letter
\<real>                 code: 0x00211d  group: letter
\<int>                  code: 0x002124  group: letter
\<leftarrow>            code: 0x002190  group: arrow  abbrev: <.
\<longleftarrow>        code: 0x0027f5  group: arrow  abbrev: <.
\<longlongleftarrow>    code: 0x00290e  group: arrow  abbrev: <.
\<longlonglongleftarrow> code: 0x0021e0 group: arrow  abbrev: <.
\<rightarrow>           code: 0x002192  group: arrow  abbrev: .>  abbrev: ->
\<longrightarrow>       code: 0x0027f6  group: arrow  abbrev: .>  abbrev: -->
\<longlongrightarrow>   code: 0x00290f  group: arrow  abbrev: .>  abbrev: --->
\<longlonglongrightarrow> code: 0x0021e2 group: arrow abbrev: .>  abbrev: --->
\<Leftarrow>            code: 0x0021d0  group: arrow  abbrev: <.
\<Longleftarrow>        code: 0x0027f8  group: arrow  abbrev: <.
\<Lleftarrow>           code: 0x0021da  group: arrow  abbrev: <.
\<Rightarrow>           code: 0x0021d2  group: arrow  abbrev: .>  abbrev: =>
\<Longrightarrow>       code: 0x0027f9  group: arrow  abbrev: .>  abbrev: ==>
\<Rrightarrow>          code: 0x0021db  group: arrow  abbrev: .>
\<leftrightarrow>       code: 0x002194  group: arrow  abbrev: <>  abbrev: <->
\<longleftrightarrow>   code: 0x0027f7  group: arrow  abbrev: <>  abbrev: <->  abbrev: <-->
\<Leftrightarrow>       code: 0x0021d4  group: arrow  abbrev: <>
\<Longleftrightarrow>   code: 0x0027fa  group: arrow  abbrev: <>
\<mapsto>               code: 0x0021a6  group: arrow  abbrev: .>  abbrev: |->
\<longmapsto>           code: 0x0027fc  group: arrow  abbrev: .>  abbrev: |-->
\<midarrow>             code: 0x002500  group: arrow  abbrev: <>
\<Midarrow>             code: 0x002550  group: arrow  abbrev: <>
\<hookleftarrow>        code: 0x0021a9  group: arrow  abbrev: <.
\<hookrightarrow>       code: 0x0021aa  group: arrow  abbrev: .>
\<leftharpoondown>      code: 0x0021bd  group: arrow  abbrev: <.
\<rightharpoondown>     code: 0x0021c1  group: arrow  abbrev: .>
\<leftharpoonup>        code: 0x0021bc  group: arrow  abbrev: <.
\<rightharpoonup>       code: 0x0021c0  group: arrow  abbrev: .>
\<rightleftharpoons>    code: 0x0021cc  group: arrow  abbrev: <> abbrev: ==
\<leadsto>              code: 0x00219d  group: arrow  abbrev: .> abbrev: ~>
\<downharpoonleft>      code: 0x0021c3  group: arrow
\<downharpoonright>     code: 0x0021c2  group: arrow
\<upharpoonleft>        code: 0x0021bf  group: arrow
#\<upharpoonright>       code: 0x0021be  group: arrow
\<restriction>          code: 0x0021be  group: punctuation
\<Colon>                code: 0x002237  group: punctuation
\<up>                   code: 0x002191  group: arrow
\<Up>                   code: 0x0021d1  group: arrow
\<down>                 code: 0x002193  group: arrow
\<Down>                 code: 0x0021d3  group: arrow
\<updown>               code: 0x002195  group: arrow
\<Updown>               code: 0x0021d5  group: arrow
\<langle>               code: 0x0027e8  group: punctuation  abbrev: <<
\<rangle>               code: 0x0027e9  group: punctuation  abbrev: >>
\<lceil>                code: 0x002308  group: punctuation  abbrev: [.
\<rceil>                code: 0x002309  group: punctuation  abbrev: .]
\<lfloor>               code: 0x00230a  group: punctuation  abbrev: [.
\<rfloor>               code: 0x00230b  group: punctuation  abbrev: .]
\<lparr>                code: 0x002987  group: punctuation  abbrev: (|
\<rparr>                code: 0x002988  group: punctuation  abbrev: |)
\<lbrakk>               code: 0x0027e6  group: punctuation  abbrev: [|
\<rbrakk>               code: 0x0027e7  group: punctuation  abbrev: |]
\<lbrace>               code: 0x002983  group: punctuation  abbrev: {|
\<rbrace>               code: 0x002984  group: punctuation  abbrev: |}
\<guillemotleft>        code: 0x0000ab  group: punctuation  abbrev: <<
\<guillemotright>       code: 0x0000bb  group: punctuation  abbrev: >>
\<bottom>               code: 0x0022a5  group: logic
\<top>                  code: 0x0022a4  group: logic
\<and>                  code: 0x002227  group: logic  abbrev: /\  abbrev: &
\<And>                  code: 0x0022c0  group: logic  abbrev: !!
\<or>                   code: 0x002228  group: logic  abbrev: \/  abbrev: |
\<Or>                   code: 0x0022c1  group: logic  abbrev: ??
\<forall>               code: 0x002200  group: logic  abbrev: !  abbrev: ALL
\<exists>               code: 0x002203  group: logic  abbrev: ?  abbrev: EX
\<nexists>              code: 0x002204  group: logic  abbrev: ~?
\<not>                  code: 0x0000ac  group: logic  abbrev: ~
\<box>                  code: 0x0025a1  group: logic
\<diamond>              code: 0x0025c7  group: logic
\<diamondop>            code: 0x0022c4  group: operator
\<turnstile>            code: 0x0022a2  group: relation  abbrev: |-
\<Turnstile>            code: 0x0022a8  group: relation  abbrev: |=
\<tturnstile>           code: 0x0022a9  group: relation  abbrev: |-
\<TTurnstile>           code: 0x0022ab  group: relation  abbrev: |=
\<stileturn>            code: 0x0022a3  group: relation  abbrev: -|
\<surd>                 code: 0x00221a  group: relation
\<le>                   code: 0x002264  group: relation  abbrev: <=
\<ge>                   code: 0x002265  group: relation  abbrev: >=
\<lless>                code: 0x00226a  group: relation  abbrev: <<
\<ggreater>             code: 0x00226b  group: relation  abbrev: >>
\<lesssim>              code: 0x002272  group: relation
\<greatersim>           code: 0x002273  group: relation
\<lessapprox>           code: 0x002a85  group: relation
\<greaterapprox>        code: 0x002a86  group: relation
\<in>                   code: 0x002208  group: relation  abbrev: :
\<notin>                code: 0x002209  group: relation  abbrev: ~:
\<subset>               code: 0x002282  group: relation
\<supset>               code: 0x002283  group: relation
\<subseteq>             code: 0x002286  group: relation  abbrev: (=
\<supseteq>             code: 0x002287  group: relation  abbrev: )=
\<sqsubset>             code: 0x00228f  group: relation
\<sqsupset>             code: 0x002290  group: relation
\<sqsubseteq>           code: 0x002291  group: relation  abbrev: [=
\<sqsupseteq>           code: 0x002292  group: relation  abbrev: ]=
\<inter>                code: 0x002229  group: operator  abbrev: Int
\<Inter>                code: 0x0022c2  group: operator  abbrev: Inter  abbrev: INT
\<union>                code: 0x00222a  group: operator  abbrev: Un
\<Union>                code: 0x0022c3  group: operator  abbrev: Union  abbrev: UN
\<squnion>              code: 0x002294  group: operator
\<Squnion>              code: 0x002a06  group: operator  abbrev: SUP
\<sqinter>              code: 0x002293  group: operator
\<Sqinter>              code: 0x002a05  group: operator  abbrev: INF
\<setminus>             code: 0x002216  group: operator
\<propto>               code: 0x00221d  group: operator
\<uplus>                code: 0x00228e  group: operator
\<Uplus>                code: 0x002a04  group: operator
\<noteq>                code: 0x002260  group: relation  abbrev: ~=
\<sim>                  code: 0x00223c  group: relation
\<doteq>                code: 0x002250  group: relation  abbrev: .=
\<simeq>                code: 0x002243  group: relation
\<approx>               code: 0x002248  group: relation
\<asymp>                code: 0x00224d  group: relation
\<cong>                 code: 0x002245  group: relation
\<smile>                code: 0x002323  group: relation
\<equiv>                code: 0x002261  group: relation  abbrev: ==
\<frown>                code: 0x002322  group: relation
\<Join>                 code: 0x0022c8
\<bowtie>               code: 0x002a1d
\<prec>                 code: 0x00227a  group: relation
\<succ>                 code: 0x00227b  group: relation
\<preceq>               code: 0x00227c  group: relation
\<succeq>               code: 0x00227d  group: relation
\<parallel>             code: 0x002225  group: punctuation  abbrev: ||
\<bar>                  code: 0x0000a6  group: punctuation  abbrev: ||
\<plusminus>            code: 0x0000b1  group: operator
\<minusplus>            code: 0x002213  group: operator
\<times>                code: 0x0000d7  group: operator  abbrev: <*>
\<div>                  code: 0x0000f7  group: operator
\<cdot>                 code: 0x0022c5  group: operator
\<star>                 code: 0x0022c6  group: operator
\<bullet>               code: 0x002219  group: operator
\<circ>                 code: 0x002218  group: operator
\<dagger>               code: 0x002020
\<ddagger>              code: 0x002021
\<lhd>                  code: 0x0022b2  group: relation
\<rhd>                  code: 0x0022b3  group: relation
\<unlhd>                code: 0x0022b4  group: relation
\<unrhd>                code: 0x0022b5  group: relation
\<triangleleft>         code: 0x0025c3  group: relation
\<triangleright>        code: 0x0025b9  group: relation
\<triangle>             code: 0x0025b3  group: relation
\<triangleq>            code: 0x00225c  group: relation
\<oplus>                code: 0x002295  group: operator
\<Oplus>                code: 0x002a01  group: operator
\<otimes>               code: 0x002297  group: operator
\<Otimes>               code: 0x002a02  group: operator
\<odot>                 code: 0x002299  group: operator
\<Odot>                 code: 0x002a00  group: operator
\<ominus>               code: 0x002296  group: operator
\<oslash>               code: 0x002298  group: operator
\<dots>                 code: 0x002026  group: punctuation abbrev: ...
\<cdots>                code: 0x0022ef  group: punctuation
\<Sum>                  code: 0x002211  group: operator  abbrev: SUM
\<Prod>                 code: 0x00220f  group: operator  abbrev: PROD
\<Coprod>               code: 0x002210  group: operator
\<infinity>             code: 0x00221e
\<integral>             code: 0x00222b  group: operator
\<ointegral>            code: 0x00222e  group: operator
\<clubsuit>             code: 0x002663
\<diamondsuit>          code: 0x002662
\<heartsuit>            code: 0x002661
\<spadesuit>            code: 0x002660
\<aleph>                code: 0x002135
\<emptyset>             code: 0x002205
\<nabla>                code: 0x002207
\<partial>              code: 0x002202
\<flat>                 code: 0x00266d
\<natural>              code: 0x00266e
\<sharp>                code: 0x00266f
\<angle>                code: 0x002220
\<copyright>            code: 0x0000a9
\<registered>           code: 0x0000ae
\<hyphen>               code: 0x0000ad  group: punctuation
\<inverse>              code: 0x0000af  group: punctuation
\<onequarter>           code: 0x0000bc  group: digit
\<onehalf>              code: 0x0000bd  group: digit
\<threequarters>        code: 0x0000be  group: digit
\<ordfeminine>          code: 0x0000aa
\<ordmasculine>         code: 0x0000ba
\<section>              code: 0x0000a7
\<paragraph>            code: 0x0000b6
\<exclamdown>           code: 0x0000a1
\<questiondown>         code: 0x0000bf
\<euro>                 code: 0x0020ac
\<pounds>               code: 0x0000a3
\<yen>                  code: 0x0000a5
\<cent>                 code: 0x0000a2
\<currency>             code: 0x0000a4
\<degree>               code: 0x0000b0
\<amalg>                code: 0x002a3f  group: operator
\<mho>                  code: 0x002127  group: operator
\<lozenge>              code: 0x0025ca
\<wp>                   code: 0x002118
\<wrong>                code: 0x002240  group: relation
\<acute>                code: 0x0000b4
\<index>                code: 0x000131
\<dieresis>             code: 0x0000a8
\<cedilla>              code: 0x0000b8
\<hungarumlaut>         code: 0x0002dd
\<bind>                 code: 0x00291c  abbrev: >>=
\<then>                 code: 0x002aa2  abbrev: >>
\<some>                 code: 0x0003f5
\<hole>                 code: 0x002311
\<newline>              code: 0x0023ce
\<comment>              code: 0x002015  group: document  font: IsabelleText
\<open>                 code: 0x002039  group: punctuation  font: IsabelleText  abbrev: <<
\<close>                code: 0x00203a  group: punctuation  font: IsabelleText  abbrev: >>
\<here>                 code: 0x002302  font: IsabelleText
\<^undefined>           code: 0x002756  font: IsabelleText
\<^noindent>            code: 0x0021e4  group: document  font: IsabelleText
\<^smallskip>           code: 0x002508  group: document  font: IsabelleText
\<^medskip>             code: 0x002509  group: document  font: IsabelleText
\<^bigskip>             code: 0x002501  group: document  font: IsabelleText
\<^item>                code: 0x0025aa  group: document  font: IsabelleText
\<^enum>                code: 0x0025b8  group: document  font: IsabelleText
\<^descr>               code: 0x0027a7  group: document  font: IsabelleText
\<^footnote>            code: 0x00204b  group: document  font: IsabelleText
\<^verbatim>            code: 0x0025a9  group: document  font: IsabelleText
\<^theory_text>         code: 0x002b1a  group: document  font: IsabelleText
\<^emph>                code: 0x002217  group: document  font: IsabelleText
\<^bold>                code: 0x002759  group: control  group: document  font: IsabelleText
\<^sub>                 code: 0x0021e9  group: control  font: IsabelleText
\<^sup>                 code: 0x0021e7  group: control  font: IsabelleText
\<^bsub>                code: 0x0021d8  group: control_block  font: IsabelleText  abbrev: =_(
\<^esub>                code: 0x0021d9  group: control_block  font: IsabelleText  abbrev: =_)
\<^bsup>                code: 0x0021d7  group: control_block  font: IsabelleText  abbrev: =^(
\<^esup>                code: 0x0021d6  group: control_block  font: IsabelleText  abbrev: =^)
"""
