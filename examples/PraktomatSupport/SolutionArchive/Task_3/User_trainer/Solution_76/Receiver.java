/** Interface fuer einen Empfaenger der AMI-Codierung.
 *
 */
public interface Receiver {
    /** Decodiert eine Signalfolge durch das AMI-Verfahren in eine bit-Folge.
     * 
     * @param toReceive Die zu decodierende Signalfolge.
     * @return  Die resultierende bit-Folge, als boolesches Array.
     * @throws InvalidSignalException bei ungueltigen Signalfolgen.
     */
    boolean[] receive(String toReceive) throws InvalidSignalException;
    
    /** Beendet die Uebertragung und decodiert alle noch unbehandelten Signale.
     *
     * @return  Die resultierende bit-Folge, als boolesches Array. 
     */
    boolean[] flush();
    
    /** Liefert das Signal, mit dem die letzte '1' codiert wurde.
     * 
     * @return  Eins der beiden Signale, mit dem '1' codiert wird.
     */
    char getLastPulse();
}
