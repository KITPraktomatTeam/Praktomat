// HelloDate.java.  
import java.util.*;

/** The second example program, and the first example of a class comment.
 *  Key new ides: (a) Use of import and Java standard library, (b)
 *  use of comment documentation.  Note the openning /**
 *  This example stolen from Bruce Ecke's Thinking in Java.  Most
 *  examples stolen from Pat Troy and modified lightly.  Examples
 *  generally don't have any comments; student code will have
 *  comments, and in particular, class comments.
 *  @author Robert H. Sloan
 */
public class HelloDate {
    /** Sole entry point to application, as always.  
     *  Example of a function comment as well.
     *  @parem args array of strings, ignored here (command line input)
     *  @return No value is returned
     */
    public static void main (String[] args) {
	System.out.println ("Hello, it's: ");
	System.out.println(new Date());
    }
}
