/** Wird von Klasse AMI geworfen, wenn ein nicht behandelbarer
 * Fehler auftritt, etwa der Empfang ungueltiger Signalfolgen.
 */
public class AMIException extends Exception {
    
    /**
     * Erzeugt eine neue InvalidSignalException.
     *
     * @param message  Eine Fehlernachricht.
     */
    public AMIException(String message) {
        super(message);
    }
    
}
