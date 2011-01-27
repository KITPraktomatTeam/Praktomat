import java.util.BitSet;

/** Realisiert einen HDB3-Empfaenger fuer das AMI-Verfahren.
 * Der Empfaenger ist als endlicher Automat realisiert.
 */
public class HDB3Receiver implements Receiver {
    
    /** Codiert die vier Zustaende des Sendeautomaten. 
     */
    public enum State {
        /** Die vier moeglichen Zustaende. */
        START, 
        /** Die vier moeglichen Zustaende. */
        STATE_1,
        /** Die vier moeglichen Zustaende. */
        STATE_2,
        /** Die vier moeglichen Zustaende. */
        STATE_3;
          
        /** Liefert den Nachfolgezustand des aktuellen Zustands.
         * START    -->  STATE_1
         * STATE_1  -->  STATE_2
         * STATE_2  -->  STATE_3
         * STATE_3  -->  START
         * 
         * @return Der Nachfolgezustand.
         */
        State next() {
            if (this == START) {
                return STATE_1;
                
            } else if (this == STATE_1) {
                return STATE_2;
                
            } else if (this == STATE_2) {
                return STATE_3;
            }
            
            return null;
        }
    }
    
    /** Codiert die drei Ergebnisse des Lookaheads.
     * 
     */ 
    public enum Lookahead {
        /** Codierung einer '1'*/
        ONE,
        /** Codierung von '0000' */
        FOUR_ZEROS,
        /** Signalfolge ist zu Kurz fuer konkretes Ergebnis. */
        TOO_SHORT;
    }
    
    private State state;
    private ZeroBuffer zeroBuffer;
    private String buffer;
    private AMI.Medium medium;
    
    private char last;
    
    /**
     * Erzeugt einen neuen HDB3Emnpfaenger.
     *
     * @param medium  Die Signalcodierung, anbhaengig vom Uebertragungsmedium.
     */
    public HDB3Receiver(AMI.Medium medium) {
        this.last = medium.minus(); 
        this.medium = medium;
        this.state = HDB3Receiver.State.START;       
        this.zeroBuffer = new ZeroBuffer();
        this.buffer = "";
    }
    
    /** Decodiert eine Signalfolge durch das AMI-Verfahren in eine bit-Folge.
     * 
     * @param toDecode Die zu decodierende Signalfolge.
     * @return  Die resultierende bit-Folge, als boolesches Array. 
     * @throws InvalidSignalException bei ungueltigen Signalfolgen.
     */
    public boolean[] receive(String toDecode) throws InvalidSignalException {
        BitSet output = new BitSet();
        toDecode = buffer + toDecode;
        int pos = -1;        
        buffer = "";
     
        for (int i = 0; i < toDecode.length(); i++) {
            try {
                char c = toDecode.charAt(i);
     
                switch (c) {
                    case '=':
                        if (state != HDB3Receiver.State.STATE_3) {
                            state = state.next();
                            zeroBuffer.buffer(false);
     
                        } else {
                            reset();
                            throw new InvalidSignalException
                            ("Error! Wrong signal in " 
                                    + toDecode + " at index " + i);
                        }
                        break;
     
                    case '+':
                        if (state == HDB3Receiver.State.START 
                                && last == medium.minus()) {
                            HDB3Receiver.Lookahead la = 
                                    lookahead(toDecode, c, i + 1);
                            
                            if (la == HDB3Receiver.Lookahead.FOUR_ZEROS) {
                                i += 3;
                                
                                // add "0000";
                                output.set(pos + 1, pos + 4, false);
                                pos += 4;
                                last = medium.plus();
     
                            } else if (la == HDB3Receiver.Lookahead.ONE) {
                                pos++;
                                output.set(pos, true); // add "1";
                                last = medium.plus();

                            } else {
                                // puffern
                                puffern(toDecode, i + 1);
                            }
     
                        } else if (state == HDB3Receiver.State.STATE_3 
                                && last == medium.plus()) {
                            
                            // null
                            // add "0000";
                            output.set(pos + 1, pos + 4, false);
                            pos += 4;
                            last = medium.plus();
                            zeroBuffer.clear();
                            state = HDB3Receiver.State.START;
     
                        } else if (last == medium.minus()) {
                            // add buffer
                            for (int y = 0; y < zeroBuffer.size(); y++) { 
                                pos++;
                                output.set(pos, zeroBuffer.get(y));
                            }
                            
                            pos++;
                            output.set(pos, true);  // add "1""
                            last = medium.plus();
                            zeroBuffer.clear();
                            state = HDB3Receiver.State.START;
     
                        } else {
                            reset();
                            throw new InvalidSignalException
                            ("Error! Wrong signal in " 
                                    + toDecode + " at index " + i);
                        }
                        break;
     
                    case '-':                        
                        if (state == HDB3Receiver.State.START 
                                && last == medium.plus()) {
                            
                            HDB3Receiver.Lookahead la = 
                                    lookahead(toDecode, c, i + 1);
                            
                            if (la == HDB3Receiver.Lookahead.FOUR_ZEROS) {
                                i += 3;
                                
                                // add "0000";
                                output.set(pos + 1, pos + 4, false);
                                pos += 4;
                                last = medium.minus();
     
                            } else if (la == HDB3Receiver.Lookahead.ONE) {
                                pos++;
                                output.set(pos, true); // add "1";
                                last = medium.minus();
                                
                            } else {
                                puffern(toDecode, i + 1);
                            }
                            
     
                        } else if (state == HDB3Receiver.State.STATE_3 
                                && last == medium.minus()) {
                            
                            // null
                            // add "0000";
                            output.set(pos + 1, pos + 4, false);
                            pos += 4;
                            last = medium.minus();
                            zeroBuffer.clear();
                            state = HDB3Receiver.State.START;
     
                        } else if (last == medium.plus()) {
                            // add buffer
                            for (int y = 0; y < zeroBuffer.size(); y++) { 
                                pos++;
                                output.set(pos, zeroBuffer.get(y));
                            }
                            
                            pos++;
                            output.set(pos, true);  // add "1""
                            last = medium.minus();
                            zeroBuffer.clear();
                            state = HDB3Receiver.State.START;
     
                        } else {
                            reset();
                            throw new InvalidSignalException
                                    ("Error! Wrong signal in "
                                    + toDecode + " at index " + i);
                        }
                        break;
     
                    default: reset();
                             throw new InvalidSignalException
                             ("Error! Wrong signal in " 
                             + toDecode + " at index " + i);
                }
     
            } catch (StringIndexOutOfBoundsException e) {
                puffern(toDecode, i);
                return convertToBoolArray(output, pos + 1);
            }
        }
        return convertToBoolArray(output, pos + 1);
    }
    
    /** Erzeugt ein boolesches Array aus einem BitSet.
     *
     * @param b  Das zu konvertierende BitSet.
     * @param i  Der Offset fuer den zu konvertierenden Teil von 'b' 
     *           (Position 'i' exklusive).
     * @return  Ein boolesches Array.
     */
    private boolean[] convertToBoolArray(BitSet b, int i) {
        boolean[] bool = new boolean[i];
        
        for (int x = 0; x < i; x++) {
            bool[x] = b.get(x);
        }
        
        return bool;
    }
       
    /** Beendet die Uebertragung und decodiert alle noch unbehandelten Signale.
     *
     * @return  Die resultierende bit-Folge, als boolesches Array. 
     */
    public boolean[] flush() {
        boolean[] bool = new boolean[zeroBuffer.size() + buffer.length()];
        int pos = 0;
        
        for (int i = 0; i < zeroBuffer.size(); i++) {
            bool[i] = zeroBuffer.get(i);
            pos++;
        }
        
        for (int i = 0; i < buffer.length(); i++) {
            if (buffer.charAt(i) == '+' || buffer.charAt(i) == '-') {
                bool[pos] = true;                
                
            } else if (buffer.charAt(i) == '=') {
                bool[pos] = false;
            }
            
            pos++;
        }
        
        reset();
        return bool;
    }
    
    /** Realisiert das Lookahead-Verfahren.
     * 
     * @param str  Die Eingabe.
     * @param c  Das zuletzt eingelesene Signal.
     * @param pos  Die Position im Eingabewort.
     * @return  Das Ergebnis des Lookaheads.
     */
    private HDB3Receiver.Lookahead lookahead(String str, char c, int pos) {
        try {
            for (int i = 0; i < 3; i++) {
                char la = str.charAt(pos + i);

                if (la != c && (la != medium.zero() || i == 2)) {

                    return HDB3Receiver.Lookahead.ONE;

                    // vier nullen
                } else if (la == c && i == 2) {
                    return HDB3Receiver.Lookahead.FOUR_ZEROS;
                }
            }
        
        } catch (ArrayIndexOutOfBoundsException e) {
            return HDB3Receiver.Lookahead.TOO_SHORT;
        } 
        
        return HDB3Receiver.Lookahead.TOO_SHORT;
    }
    
    /** Puffert den Suffix des erhaltenen Strings.
     *
     * @param str  Der String.
     * @param abPos  Der Start des zu puffernden Suffixes.
     */
    private void puffern(String str, int abPos) {
        for (int i = abPos; i < str.length(); i++) {
            buffer += str.charAt(i);
        }        
    }
    
    /** Stellt die Ausgangskonfiguration her.
     */
    private void reset() {
        this.state = HDB3Receiver.State.START;
        this.last = medium.minus();
        this.zeroBuffer.clear();
        this.buffer = "";
    }
      
    /** Liefert das Signal, mit dem die letzte '1' codiert wurde.
     * 
     * @return  Eins der beiden Signale, mit dem '1' codiert wird.
     */
    public char getLastPulse() {
        return this.last;
    }    
    
    /** Ein Puffer fuer unverarbeitete bits.
     * Hat Groesse 4. 
     */  
    private class ZeroBuffer {
        private boolean[] buffer;
        private int pointer; // zeigt auf aktuelles element
        
        /** Erzeugt einen neuen Puffer der Groesse 4. 
         */
        ZeroBuffer() {
            buffer = new boolean[4];
            pointer = -1;
        }
        
        /** Puffert das erhaltene bit.
         *
         * @param b  Das zu puffernde bit.
         */
        void buffer(boolean b) {
            pointer++;
            buffer[pointer] = b;
        }
        
        /** Liefert das bit an Position pos.
         *
         * @parma pos  Postion im Puffer.
         * @return  Das bit an Position pos.
         */
        boolean get(int pos) {
            return buffer[pos];
        }
        
        /** Leert den Puffer.
         */
        void clear() {
            pointer = -1;
        }
        
        /** Liefert die aktuell verwendete Groesse.
         *
         * @return  Die aktuell verwendete Groesse.
         */
        int size() {
            return pointer + 1;
        }
    }
}
