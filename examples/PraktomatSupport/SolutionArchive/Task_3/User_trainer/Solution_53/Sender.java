package ami;

/** Interface fuer einen Sender der AMI-Codierung.
 *
 */
public interface Sender {
    /** Codiert eine bit-Folge durch das AMI-Verfahren.
     * 
     * @param toSend  Die zu codierende bit-Folge, als boolesches Array.
     * @return  Die resultierende Signalfolge. 
     */
    String send(boolean[] toSend);
    
    /** Beendet die Uebertragung und codiert alle noch unbehandelten bits.
     *
     * @return  Die resultierende Signalfolge. 
     */
    String flush();
    
    /** Liefert den diskretisierten Gleichstromanteil der aktuellen 
     * Uebertragung.
     * 
     * @return Der Gleichstromanteil - diskret als 0, 1 oder -1
     */
    int getDC();
    
    /** Liefert das Signal, mit dem die letzte '1' codiert wurde.
     * 
     * @return  Eins der beiden Signale, mit dem '1' codiert wird.
     */
    char getLastPulse();
}
