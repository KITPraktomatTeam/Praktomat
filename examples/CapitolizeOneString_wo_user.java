/** This program will get a line of input 
 * and will print a copy of the line in which the first
 * character of each word has been changed to upper case.
 * The program was written to test the printCapitalized
 * subroutine.  It depends on the non-standard TextIO class.
 */
public class CapitolizeOneString_wo_user {
	    
	/** Sole entry point to application, as always.  
	 *  @param args array of strings, ignored here (command line input)
	 */
	public static void main(String[] args) {
		String line;  // Line of text entered.
		TextIO.putln("Enter a line of text.");
		line = TextIO.getln();
		TextIO.putln();
		TextIO.putln("Capitalized version:");
		printCapitalized(line);
	}  // end main()
	
	/** Subroutine to calulate an Capitalised String. 
	 *  @param str sring to be capitalized
	 */
	static void printCapitalized(String str) {
		// Print a copy of str to standard output, with the
		// first letter of each word in upper case.
		char ch;       // One of the characters in str.
		char prevCh;   // The character that comes before ch in the string.
		int i;         // A position in str, from 0 to str.length()-1.
		prevCh = '.';  // Prime the loop with any non-letter character.
		for (i = 0;  i < str.length();  i++) {
			ch = str.charAt(i);
			if (Character.isLetter(ch)  &&  !Character.isLetter(prevCh)) {
                System.out.print(Character.toUpperCase(ch));
			} else {
                System.out.print(ch);
			}
			prevCh = ch;  // prevCh for next iteration is ch.
		}
		System.out.println();
	}
	
}  // end class