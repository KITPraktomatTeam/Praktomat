package ami;

/** Eine Exception, die von einem AMI-Empfaenger geworfen wird,
 * falls dieser eine ungueltige Signalfolge empfangen hat. 
 */
public class InvalidSignalException extends Exception {
    
    /**
     * Erzeugt eine neue InvalidSignalException.
     *
     * @param message  Eine Fehlernachricht.
     */
    public InvalidSignalException(String message) {
        super(message);
    }
    
}
