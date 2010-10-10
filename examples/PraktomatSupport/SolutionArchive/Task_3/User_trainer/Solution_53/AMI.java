package ami;

/** Stellt die Schnittstelle zur Codierung von Zeichen in
 * HDB3 dar. 
 *
 *
 */
public class AMI {

    /** Dieses Enum codiert die drei Signale, in die AMI codiert.
     */
    public enum Medium {
        /** Spannungssignale. */
        ELECTRIC ('+', '-', '=');
        
        private final char plus;
        private final char minus;
        private final char zero;
        
        /** Konstruiert eine neue Signalrepraesentation.
         */
        Medium(char plus, char minus, char zero) {
            this.plus = plus;
            this.minus = minus;
            this.zero = zero;
        }
         
        /** Liefert die Darstellung fuer den Plus-Wert.
         * 
         * @return Die Darstellung fuer den Plus-Wert.
         */
        public char plus() {
            return plus;
        }
        
        /** Liefert die Darstellung fuer den Minus-Wert.
         * 
         * @return Die Darstellung fuer den Minus-Wert.
         */
        public char minus() {
            return minus;
        }
        
        /** Liefert die Darstellung fuer den Null-Wert.
         * 
         * @return Die Darstellung fuer den Null-Wert.
         */
        public char zero() {
            return zero;
        }
    }
    
    /** Codiert die Laenge der Bitdarstellung.
     */
    public enum BitAmount {
        /** Default-Laenge ist 7.*/
        DEFAULT(7);
        
        private final int length;
        
        /** Konstruiert eine neue Bitdarstellung. 
         *
         * @param length  Die Laenge der Bitdarstellung.
         */
        BitAmount(int length) {
            this.length = length;
        }
        
        /** Liefert die Laenge der Bitdarstellung.
         *
         * @return  Die Laenge der Bitdarstellung.
         */
        public int getLength() {
            return length;
        }
    }
    
    /** Die zu codierenden Alphabete.
     */
    public enum Charset {
        /** Alphabet ohne Umlaute. */
        DEFAULT("[a-zA-Z]*");
        
        private final String regexp;
        
        /** Erzeugt den zu codierenden Zeichensatz. */
        Charset(String str) {
            regexp = str;
        }
        
        /** Liefert den zu codierenden Zeichensatz als regulaeren Ausdruck. 
         *
         * @return Der zu codierende Zeichensatz als regulaerer Ausdruck. 
         */
        public String getRegExp() {
            return regexp;
        }
    }
    
    private Sender sender;
    private Receiver receiver;
    private BitAmount bits;
    private BitBuffer buffer;
    private Charset charset;
    
    /**
     * Erzeugt ein neues AMI-verfahren.
     *
     * @param sender  Der AMI-Sender.
     * @param receiver  Der AMI-Empfaenger.
     */
    public AMI(Sender sender, Receiver receiver) {
        this.sender = sender;
        this.receiver = receiver;
        this.bits = AMI.BitAmount.DEFAULT;
        this.buffer = new BitBuffer(this.bits.getLength());
        this.charset = AMI.Charset.DEFAULT;
    }
    
    /** Liefert den zu codierenden Zeichensatz als regulaeren Ausdruck. 
     *
     * @return Der zu codierende Zeichensatz als regulaerer Ausdruck. 
     */
    public String getCharsetRegExp() {
        return charset.getRegExp();
    }
    
    /** Codiert die zu sendende Eingabe in eine Signalfolge.
     *
     * @param toSend  Die Eingabe.
     * @return  Die Signalfolge.
     */
    public String send(String toSend) {           
        if (toSend == null) {
            return this.sender.flush();
            
        } else {
            // convert to bitform
            boolean[] bitform = bitform(toSend);
            
            return this.sender.send(bitform);
        }
    }
    
    /** Decodiert eine Signalfolge zurueck in Klartext.
     *
     * @param received  Die Signalfolge.
     * @return  Der Klartext.
     * @throws AMIException bei nich behandelbaren Fehlern.
     */
    public String receive(String received) throws AMIException {
        try {            
            if (received == null) {
                boolean[] bitform = this.receiver.flush();
                StringBuilder erg = stringform(bitform);

                if (!buffer.isEmpty()) {                    
                    erg.append(" Rest: " + buffer.read());
                    buffer.clear();
                }

                return erg.toString();

            } else {
                boolean[] bitform = this.receiver.receive(received);

                return stringform(bitform).toString();
            }
        
        } catch (InvalidSignalException ise) {
            buffer.clear();
            throw new AMIException(ise.getMessage());
        }   
    }
    
     /** Liefert den diskretisierten Gleichstromanteil der aktuellen 
     * Uebertragung.
     * 
     * @return Der Gleichstromanteil - diskret als 0, 1 oder -1
     */
    public int getDC() {
        return this.sender.getDC();
    }
    
    /** Liefert das Signal, mit dem der Sender die letzte '1' codierte.
     * 
     * @return  Eins der beiden Signale, mit dem '1' codiert wird.
     */
    public char getLastPulseOfSender() {
        return this.sender.getLastPulse();
    }
    
    /** Liefert das Signal, das der Empfaenger zuletzt als '1' interpretierte.
     * 
     * @return  Eins der beiden Signale, mit dem '1' codiert wird.
     */
    public char getLastPulseOfReceiver() {
        return this.receiver.getLastPulse();
    }
    
    /** Wandelt eine Eingabe in eine bit-Darstellung um.
     *
     * @param convert  Die Eingabe.
     * @return  Eine bit-Darstellung als boolesches Array.
     */
    public boolean[] bitform(String convert) {
        boolean[] bits = new boolean[convert.length() * this.bits.length];
        int pos = 0;
        
        for (int i = 0; i < convert.length(); i++) {
            int bytes = convert.charAt(i);            
            
            for (int x = 0; x < this.bits.getLength(); x++) {
                if (bytes % 2 == 1) {
                    bits[pos] = true;
                    
                } else {
                    bits[pos] = false;
                }
                
                bytes = bytes / 2;
                pos++;
            }
        }
        
        return bits;
    }
    
    /** Wandelt eine bit-Folge in Klartext um.
     *
     * @param convert  Die Eingabe.
     * @return  Der Klartext.
     */
    public String charform(boolean[] convert) {        
        StringBuilder res = new StringBuilder();
        BitBuffer tmp = buffer.copy();
        buffer.clear();
        
        res = stringform(convert);
        
        if (!buffer.isEmpty()) {
            res.append(" Rest: " + buffer.read());
        }
        
        buffer = tmp;

        return res.toString();
    }
    
    
    /* privates */
    
    /** Wandelt eine bit-Folge in Klartext um.
     *
     * @param bits  Die Eingabe.
     * @return  Der Klartext.
     */
    private StringBuilder stringform(boolean[] bits) {
        StringBuilder str = new StringBuilder();
        
        for (int i = 0; i < bits.length; i++) {
            buffer.buffer(bits[i]);
            
            if (buffer.isFull()) {
                str.append(bufferToDecimal());
                buffer.clear();
            }
        }
        
        if (buffer.isFull()) {
            str.append(bufferToDecimal());
            buffer.clear();
        }
        
        return str;
    }
    
    /** Wandelt den Inhalt des Puffers in einen byte-Wert und diesen 
     * in ein Zeichen um.
     *
     * @return  Das ermittelte Zeichen.
     */
    private char bufferToDecimal() {
        int bytes = 0;
        int toAdd = 1;
        
        for (int i = 0; i < bits.length; i++) {
            if (buffer.get(i)) {
                for (int x = 0; x < i; x++) {
                    toAdd *= 2;
                }
                
                bytes += toAdd;
                toAdd = 1;
            }
        }
        
        return (char) bytes;
    }
    
    /** Ein Puffer fuer unverarbeitete bits.
     */ 
    private class BitBuffer {
        private boolean[] buffer;
        private int pointer; // zeigt auf aktuelles element
        
        /** Erzeugt einen neuen Puffer. 
         *
         * @param size  Die Groesse des Puffers.
         */
        BitBuffer(int size) {
            buffer = new boolean[size];
            pointer = -1;
        }
        
        /** Erstellt eine Kopie des Puffers.
         *
         * @return  Die Kopie.
         */
        BitBuffer copy() {
            BitBuffer b = new BitBuffer(buffer.length);
            b.pointer = pointer;
            b.buffer = (boolean[]) buffer.clone();
            
            return b;
        }
        
        /** Puffert das erhaltene bit.
         *
         * @param b  Das zu puffernde bit.
         */
        void buffer (boolean b) {
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
        
        /** Testet, ob der Puffer voll ist.
         *
         * @return  true, falls voll.
         */
        boolean isFull() {
            return pointer == buffer.length - 1;
        }
                
        /** Testet, ob der Puffer leer ist.
         *
         * @return  true, falls leer.
         */
        boolean isEmpty() {
            return pointer == -1;
        }
        
        /** Erzeugt eine String-Darstellung des aktuellen Pufferinhalts.
         *
         * @return  Eine String-Darstellung des aktuellen Pufferinhalts.
         */
        String read() {
            StringBuilder str = new StringBuilder();
            
            for (int i = 0; i <= pointer; i++) {
                if (buffer[i]) {
                    str.append(1);
                    
                } else {
                    str.append(0);
                }
                
            }
            
            return str.toString();
        }
    }
}
