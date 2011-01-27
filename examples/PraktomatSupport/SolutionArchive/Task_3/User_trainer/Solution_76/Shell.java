import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

/** Die Shell fuer das AMI-Programm.
 */
public final class Shell {
    
    /**
     * Erzeugt eine neue Shell.
     */
    private Shell() {
        
    }
    
    /** Die Main-Methode.
     * Erwartet keine Parameter.
     *
     * @param args  Parameter - sollten leer sein.
     * @throws IOException falls die Verbindung zur Konsole gestoert ist.
     */
    public static void main(String[] args) throws IOException {
        Sender sender = new HDB3Sender(AMI.Medium.ELECTRIC);
        Receiver receiver = new HDB3Receiver(AMI.Medium.ELECTRIC);
        AMI ami = new AMI(sender, receiver);
        BufferedReader read = new BufferedReader(
                new InputStreamReader(System.in));
        
        while (true) {
            System.out.print("AMI> ");
            String input = read.readLine();
            String[] token = input.split("\\s");
            
            if (token.length == 0) {
                continue;
            }
            
            if (token[0].equals("send") || token[0].equals("s")) {
                if (token.length == 1) {
                    System.out.println(ami.send(null));
                    
                } else {                      
                    if (!java.util.regex.Pattern.matches(
                            ami.getCharsetRegExp(), token[1])) {
                        
                        System.out.println("Error! Invalid input character");
                        
                    } else {
                        System.out.println(ami.send(token[1]));
                    }
                }
                
            } else if (token[0].equals("receive") || token[0].equals("r")) {
                try {
                    if (token.length == 1) {
                        System.out.println(ami.receive(null));
                        
                    } else {                
                        System.out.println(ami.receive(token[1]));
                    } 
                    
                } catch (AMIException amiEx) {
                    System.out.println(amiEx.getMessage());
                }
                
            } else if (token[0].equals("rpulse") || token[0].equals("rp")) {
                System.out.println(ami.getLastPulseOfReceiver());
                
            } else if (token[0].equals("spulse") || token[0].equals("sp")) {
                System.out.println(ami.getLastPulseOfSender());
                
            } else if (token[0].equals("dc")) {
                System.out.println(ami.getDC());
                
            } else if (token[0].equals("bitform") || token[0].equals("b")) {
                if (token.length == 1) {
                    wrongParameter();
                    
                } else {
                    boolean[] b = ami.bitform(token[1]);
                    
                    for (int y = 0; y < b.length; y++) {
                        if (b[y]) {
                            System.out.print(1);
                        
                        } else {
                            System.out.print(0);
                        }
                    }
                    
                    System.out.println();
                }
                
            } else if (token[0].equals("charform") || token[0].equals("c")) {
                if (token.length == 1) {
                    wrongParameter();
                    
                } else {
                    boolean[] bits = inputToBits(token[1]);
                    System.out.println(ami.charform(bits));
                }
                
            } else if (token[0].equals("help") || token[0].equals("h")) {
                System.out.println(help());
                
            } else if (token[0].equals("quit") || token[0].equals("q")) {
                break;
                 
            } else {
                wrongCommand();
            }
        }
    }
    
    private static boolean[] inputToBits(String str) {
        boolean[] bits = new boolean[str.length()];
                
        for (int pos = 0; pos < str.length(); pos++) {
            if (str.charAt(pos) == '1') {
                bits[pos] = true;
                
            } else if (str.charAt(pos) == '0') {
                bits[pos] = false;
                
            } else {
                System.out.println("Error! Not a boolean input stream.");
            }
        }
        
        return bits;
    }
    
    private static void wrongCommand() {
        System.out.println("Error! Unknown command. Type 'h' for help.");
    }
    
    private static void wrongParameter() {
        System.out.println("Error! Wrong number of params. " 
                + "Type 'h' for help.");
    }
        
    private static String help() {
        return  "send/s word:       Encode that word\n"
                + "send/s:            End connection and reset sender\n"
                + "receive/r word:    Decode that word\n"
                + "receive/r:         End connection and reset receiver\n"
                + "rpulse/rp    :     Print last pulse of receiver\n"
                + "spulse/sp    :     Print last pulse of sender\n"
                + "dc:                Print rate of DC generated by sender\n"
                + "bitform/b          Convert input into a sequence of bits\n"
                + "charform/c         Convert bits into characters\n"
                + "help/h:            This help\n"
                + "quit/q:            Quit program\n";
    }
}               