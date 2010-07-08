import java.io.IOException;
import javagently.Stream;

/**
 * Class to calculate the greatest common divisor.
 * @author Anon Ymous
 */
final class GgT {
    
    /**
     * The prompt is configurable.
     */
    public static final String PROMPT = "ggT> ";

    /**
     * Calculate the greatest common divisor.
     * @param a first operand.
     * @param b second operand.
     * @return gcd of a and b.
     */
    public static int ggT(int a, int b){
	if (a < 0) {
	    a = -a;
	}
	
	if (b < 0) {
	    b = -b;
	}
	
	while (b != 0) {
	    int t = a % b;
	    a = b;
	    b = t;
	}
	
	return a;
    }
    
    /**
     * Starts the user interface.
     * @param argv list of arguments (unused).
     * @throws IOException should not happen.
     */
    public static void main(String[] argv) throws IOException {
	int arg1;
	int arg2;
	int ggT;
	Stream in = new Stream(System.in);
	
	while (true) {
	    
	    // Prompt
	    System.out.print(PROMPT);
	    
	    // Eingabe Lesen
	    arg1 = in.readInt();
	    arg2 = in.readInt();
	    // StdInput.readLn();
	    
	    // Prüfung Eingabe
	    if ((arg1 == 0) || (arg2 == 0)){
		if (arg1 == 0 && arg2 == 0){
		    System.exit(0);
		} else { 
		    // Null als ein Argument
		    System.out.println("Fehler! ungültiger Wert");
		    continue;
		}
	    }
	    
	    // ggt Ermitteln
	    ggT = ggT(arg1, arg2);
	    
	    // Ergebnis ausgeben
	    System.out.println("ggT(" + arg1 + ", " + arg2 + ") = " + ggT);
	}
    }
}
