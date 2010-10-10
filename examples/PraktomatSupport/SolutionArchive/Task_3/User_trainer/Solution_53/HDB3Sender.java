package ami;

/** Realisiert einen HDB3-Sender fuer das AMI-Verfahren.
 * Der Sender ist als endlicher Automat realisiert.
 */
public class HDB3Sender implements Sender {
    
    /** Codiert die vier Zustaende des Sendeautomaten. 
     */
    public enum State {
        /** Die vier moeglichen Zustaende. */
        START, 
        /** Die vier moeglichen Zustaende. */
        ONE_ZERO,
        /** Die vier moeglichen Zustaende. */
        TWO_ZEROS,
        /** Die vier moeglichen Zustaende. */
        THREE_ZEROS;
                
        /** Liefert den Nachfolgezustand des aktuellen Zustands.
         * START       -->  ONE_ZERO
         * ONE_ZERO    -->  TWO_ZEROS
         * TWO_ZEROS   -->  THREE_ZEROS
         * THREE_ZEROS -->  START
         * 
         * @return Der Nachfolgezustand.
         */
        State next() {
            if (this == ONE_ZERO) {
                return TWO_ZEROS;
                
            } else if (this == TWO_ZEROS) {
                return THREE_ZEROS;
                
            } else if (this == START) {
                return ONE_ZERO;
            }
            
            return null;
        }
    }
    
    private State state;
    private ZeroBuffer zeroBuffer;
    private AMI.Medium medium;  
    
    private int dc;
    private char last;
    
    /**
     * Erzeugt einen neuen HDB3Sender.
     *
     * @param medium  Die Signalcodierung, anbhaengig vom Uebertragungsmedium.
     */
    public HDB3Sender(AMI.Medium medium) {
        this.dc = 0;
        this.last = medium.minus();
                
        this.state = HDB3Sender.State.START;
        this.medium = medium;
        this.zeroBuffer = new ZeroBuffer();
    }
    
    /** Codiert eine bit-Folge durch das AMI-Verfahren.
     * 
     * @param toSend  Die zu codierende bit-Folge, als boolesches Array.
     * @return  Die resultierende Signalfolge. 
     */
    public String send(boolean[] toSend) {
        StringBuilder output = new StringBuilder();
     
        for (int i = 0; i < toSend.length; i++) {
            boolean b = toSend[i];
            if (!b) {
                if (state != HDB3Sender.State.THREE_ZEROS) {
                    state = state.next();
                    zeroBuffer.buffer(medium.zero());
     
                } else {
                    if (dc == 0 && last == medium.plus()) {
                        output.append(zeroBuffer.read());
                        output.append(medium.plus());
                        dc += 1;
                        last = medium.plus();
 
                    } else if (dc == 0 && last == medium.minus()) {
                        output.append(zeroBuffer.read());
                        output.append(medium.minus());
                        dc -= 1;
                        last = medium.minus();
     
                    } else if (dc == 1) {
                        output.append("-==-");
                        dc -= 2;
                        last = medium.minus();
 
                    } else if (dc == -1) {
                        output.append("+==+");
                        dc += 2;
                        last = medium.plus();
                        
                    } 
     
                    state = HDB3Sender.State.START;
                    zeroBuffer.clear();
                }
                
            } else {
                if (dc == 0 && last == medium.plus()) {
                    output.append(zeroBuffer.read());
                    output.append(medium.minus());
                    dc -= 1;
                    last = medium.minus();

                } else if (dc == 0 && last == medium.minus()) {
                    output.append(zeroBuffer.read());
                    output.append(medium.plus());
                    dc += 1;
                    last = medium.plus();
     
                } else if (dc == 1) {
                    output.append(zeroBuffer.read());
                    output.append(medium.minus());
                    dc -= 1;
                    last = medium.minus();
     
                } else if (dc == -1) {
                    output.append(zeroBuffer.read());
                    output.append(medium.plus());
                    dc += 1;
                    last = medium.plus();
                    
                } 
     
                state = HDB3Sender.State.START;
                zeroBuffer.clear();
            }
        }
     
        return output.toString();
    }
    
    /** Beendet die Uebertragung und codiert alle noch unbehandelten bits.
     *
     * @return  Die resultierende Signalfolge. 
     */
    public String flush() {     
        CharSequence tmp = zeroBuffer.read();
        zeroBuffer.clear();
        state = HDB3Sender.State.START;
        dc = 0;
        last = medium.minus();
        return tmp.toString();
    }
    
    /** Liefert den diskretisierten Gleichstromanteil der aktuellen 
     * Uebertragung.
     * 
     * @return Der Gleichstromanteil - diskret als 0, 1 oder -1
     */
    public int getDC() {
        return dc;
    }
    
    /** Liefert das Signal, mit dem die letzte '1' codiert wurde.
     * 
     * @return  Eins der beiden Signale, mit dem '1' codiert wird.
     */
    public char getLastPulse() {
        return last;
    }
    
    /** Ein Puffer fuer unverarbeitete Nullen.
     * Hat Groesse 4. 
     */    
    private class ZeroBuffer {
        private StringBuilder buffer;
        private int pointer; // zeigt auf aktuelles element
        
        /** Erzeugt einen neuen Puffer der Groesse 4. 
         */
        ZeroBuffer() {
            buffer = new StringBuilder(4);
            pointer = -1;
        }
        
        /** Puffert das erhaltene Signal.
         *
         * @param c  Das zu puffernde Signal.
         */
        void buffer (char c) {
            pointer++;
            buffer.insert(pointer, c);
        }
        
        /** Liest den aktuellen Pufferinhalt aus.
         *
         * @return Der Pufferinhalt als CharSequence.
         */
        CharSequence read() {
            return buffer.subSequence(0, pointer + 1);
        }
        
        /** Leert den Puffer.
         */
        void clear() {
            pointer = -1;
        }
    }
}
