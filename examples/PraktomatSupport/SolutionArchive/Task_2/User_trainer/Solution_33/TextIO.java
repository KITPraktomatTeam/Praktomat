
/*
    The file defines a class TextIO, which provides a simple interface
    to Java's standard console input and output.  This class defines
    several static methhods for reading and writing
    values of various type.
    
    This class will only work with standard, interactive applications.
    When it is used in such an application, System.out and System.in
    should not be used directly, since the TextIO class thinks it has
    exclusive control of System.out and System.in.  (Actually, using
    System.out will probably not cause any problems, but don't use
    System.in.)

    To use this class in your program, simply include the compiled class
    file TextIO.class in the same directory with the class file for your
    main program.  (If you are using a development environment such as
    CodeWarrior or Visual J++, you can include the source file,
    TextIO.java in your project.)  You can then use all the public static methods
    from the TextIO class in your program.  (In your programs, the names
    of the methods must be prefaced with "TextIO."  For example, you should
    use the name TextIO.getln() rather than simply getln().)

    (This class is for use with my on-line introductory java textbook,
    which is available at http://math.hws.edu/eck/cs124/notes/index.html.)

    Written by:  David Eck
                 Department of Mathematics and Computer Science
                 Hobart and William Smith Colleges
                 Geneva, NY 14456
                 Email:  eck@hws.edu
                 WWW:  http://math.hws.edu/eck/

    July 16, 1998
    
    Modified February, 2000; getChar() now skips blanks and CR's, and getAnyChar() 
    can be used to read the next char even if it's a blank or CR.

*/

import java.io.*;
   
public class TextIO {

   // *************************** I/O Methods *********************************
   
         // Methods for writing the primitive types, plus type String,
         // to the console, with no extra spaces.
         //
         // Note that the real-number data types, float
         // and double, a rounded version is output that will
         // use at most 10 or 11 characters.  If you want to
         // output a real number with full accuracy, use
         // "TextIO.put(String.valueOf(x))", for example.
         
   public static void put(int x)     { put(x,0); }   // Note: also handles byte and short!
   public static void put(long x)    { put(x,0); }
   public static void put(double x)  { put(x,0); }   // Also handles float.
   public static void put(char x)    { put(x,0); }
   public static void put(boolean x) { put(x,0); }
   public static void put(String x)  { put(x,0); }


         // Methods for writing the primitive types, plus type String,
         // to the console,followed by a carriage return, with
         // no extra spaces.

   public static void putln(int x)      { put(x,0); newLine(); }  // Note: also handles byte and short!
   public static void putln(long x)     { put(x,0); newLine(); }
   public static void putln(double x)   { put(x,0); newLine(); }  // Also handles float.
   public static void putln(char x)     { put(x,0); newLine(); }
   public static void putln(boolean x)  { put(x,0); newLine(); }
   public static void putln(String x)   { put(x,0); newLine(); }
  

         // Methods for writing the primitive types, plus type String,
         // to the console, with a minimum field width of w,
         // and followed by a carriage  return.
         // If output value is less than w characters, it is padded
         // with extra spaces in front of the value.

   public static void putln(int x, int w)     { put(x,w); newLine(); }   // Note: also handles byte and short!
   public static void putln(long x, int w)    { put(x,w); newLine(); }
   public static void putln(double x, int w)  { put(x,w); newLine(); }   // Also handles float.
   public static void putln(char x, int w)    { put(x,w); newLine(); }
   public static void putln(boolean x, int w) { put(x,w); newLine(); }
   public static void putln(String x, int w)  { put(x,w); newLine(); }


          // Method for outputting a carriage return

   public static void putln() { newLine(); }
   

         // Methods for writing the primitive types, plus type String,
         // to the console, with minimum field width w.
   
   public static void put(int x, int w)     { dumpString(String.valueOf(x), w); }   // Note: also handles byte and short!
   public static void put(long x, int w)    { dumpString(String.valueOf(x), w); }
   public static void put(double x, int w)  { dumpString(realToString(x), w); }     // Also handles float.
   public static void put(char x, int w)    { dumpString(String.valueOf(x), w); }
   public static void put(boolean x, int w) { dumpString(String.valueOf(x), w); }
   public static void put(String x, int w)  { dumpString(x, w); }
   
   
         // Methods for reading in the primitive types, plus "words" and "lines".
         // The "getln..." methods discard any extra input, up to and including
         //    the next carriage return.
         // A "word" read by getlnWord() is any sequence of non-blank characters.
         // A "line" read by getlnString() or getln() is everything up to next CR;
         //    the carriage return is not part of the returned value, but it is
         //    read and discarded.
         // Note that all input methods except getAnyChar(), peek(), the ones for lines
         //    skip past any blanks and carriage returns to find a non-blank value.
         // getln() can return an empty string; getChar() and getlnChar() can 
         //    return a space or a linefeed ('\n') character.
         // peek() allows you to look at the next character in input, without
         //    removing it from the input stream.  (Note that using this
         //    routine might force the user to enter a line, in order to
         //    check what the next character is.)
         // Acceptable boolean values are the "words": true, false, t, f, yes,
         //    no, y, n, 0, or 1;  uppercase letters are OK.
         // None of these can produce an error; if an error is found in input,
         //    the user is forced to re-enter.
         // Available input routines are:
         //
         //            getByte()      getlnByte()    getShort()     getlnShort()
         //            getInt()       getlnInt()     getLong()      getlnLong()
         //            getFloat()     getlnFloat()   getDouble()    getlnDouble()
         //            getChar()      getlnChar()    peek()         getAnyChar()
         //            getWord()      getlnWord()    getln()        getString()    getlnString()
         //
         // (getlnString is the same as getln and is onlyprovided for consistency.)
   
   public static byte getlnByte()       { byte x=getByte();       emptyBuffer();  return x; }
   public static short getlnShort()     { short x=getShort();     emptyBuffer();  return x; }
   public static int getlnInt()         { int x=getInt();         emptyBuffer();  return x; }
   public static long getlnLong()       { long x=getLong();       emptyBuffer();  return x; }
   public static float getlnFloat()     { float x=getFloat();     emptyBuffer();  return x; }
   public static double getlnDouble()   { double x=getDouble();   emptyBuffer();  return x; }
   public static char getlnChar()       { char x=getChar();       emptyBuffer();  return x; }
   public static boolean getlnBoolean() { boolean x=getBoolean(); emptyBuffer();  return x; }
   public static String getlnWord()     { String x=getWord();     emptyBuffer();  return x; }
   public static String getlnString()   { return getln(); }  // same as getln()
   public static String getln() {
      StringBuffer s = new StringBuffer(100);
      char ch = readChar();
      while (ch != '\n') {
         s.append(ch);
         ch = readChar();
      }
      return s.toString();
   }
   
   
   public static byte getByte()   { return (byte)readInteger(-128L,127L); }
   public static short getShort() { return (short)readInteger(-32768L,32767L); }   
   public static int getInt()     { return (int)readInteger((long)Integer.MIN_VALUE, (long)Integer.MAX_VALUE); }
   public static long getLong()   { return readInteger(Long.MIN_VALUE, Long.MAX_VALUE); }
   
   public static char getAnyChar(){ return readChar(); }
   public static char peek()      { return lookChar(); }
   
   public static char getChar() {  // skip spaces & cr's, then return next char
      char ch = lookChar();
      while (ch == ' ' || ch == '\n') {
         readChar();
         if (ch == '\n')
            dumpString("? ",0);
         ch = lookChar();
      }
      return readChar();
   }

   public static float getFloat() {
      float x = 0.0F;
      while (true) {
         String str = readRealString();
         if (str.equals("")) {
             errorMessage("Illegal floating point input.",
                          "Real number in the range " + Float.MIN_VALUE + " to " + Float.MAX_VALUE);
         }
         else {
            Float f = null;
            try { f = Float.valueOf(str); }
            catch (NumberFormatException e) {
               errorMessage("Illegal floating point input.",
                            "Real number in the range " + Float.MIN_VALUE + " to " + Float.MAX_VALUE);
               continue;
            }
            if (f.isInfinite()) {
               errorMessage("Floating point input outside of legal range.",
                            "Real number in the range " + Float.MIN_VALUE + " to " + Float.MAX_VALUE);
               continue;
            }
            x = f.floatValue();
            break;
         }
      }
      return x;
   }
   
   public static double getDouble() {
      double x = 0.0;
      while (true) {
         String str = readRealString();
         if (str.equals("")) {
             errorMessage("Illegal floating point input",
                          "Real number in the range " + Double.MIN_VALUE + " to " + Double.MAX_VALUE);
         }
         else {
            Double f = null;
            try { f = Double.valueOf(str); }
            catch (NumberFormatException e) {
               errorMessage("Illegal floating point input",
                            "Real number in the range " + Double.MIN_VALUE + " to " + Double.MAX_VALUE);
               continue;
            }
            if (f.isInfinite()) {
               errorMessage("Floating point input outside of legal range.",
                            "Real number in the range " + Double.MIN_VALUE + " to " + Double.MAX_VALUE);
               continue;
            }
            x = f.doubleValue();
            break;
         }
      }
      return x;
   }
   
   public static String getWord() {
      char ch = lookChar();
      while (ch == ' ' || ch == '\n') {
         readChar();
         if (ch == '\n')
            dumpString("? ",0);
         ch = lookChar();
      }
      StringBuffer str = new StringBuffer(50);
      while (ch != ' ' && ch != '\n') {
         str.append(readChar());
         ch = lookChar();
      }
      return str.toString();
   }
   
   public static boolean getBoolean() {
      boolean ans = false;
      while (true) {
         String s = getWord();
         if ( s.equalsIgnoreCase("true") || s.equalsIgnoreCase("t") ||
                 s.equalsIgnoreCase("yes")  || s.equalsIgnoreCase("y") ||
                 s.equals("1") ) {
              ans = true;
              break;
          }
          else if ( s.equalsIgnoreCase("false") || s.equalsIgnoreCase("f") ||
                 s.equalsIgnoreCase("no")  || s.equalsIgnoreCase("n") ||
                 s.equals("0") ) {
              ans = false;
              break;
          }
          else
             errorMessage("Illegal boolean input value.",
                          "one of:  true, false, t, f, yes, no, y, n, 0, or 1");
      }
      return ans;
   }
   
   // ***************** Everything beyond this point is private *******************
   
   // ********************** Utility routines for input/output ********************

   private static InputStream in = System.in;    // rename standard input stream
   private static PrintStream out = System.out;  // rename standard output stream

   private static String buffer = null;  // one line read from input
   private static int pos = 0;           // position of next char in input line that has
                                         //      not yet been processed


   private static String readRealString() {   // read chars from input following syntax of real numbers
      StringBuffer s=new StringBuffer(50);
      char ch=lookChar();
      while (ch == ' ' || ch == '\n') {
          readChar();
          if (ch == '\n')
             dumpString("? ",0);
          ch = lookChar();
      }
      if (ch == '-' || ch == '+') {
          s.append(readChar());
          ch = lookChar();
          while (ch == ' ') {
             readChar();
             ch = lookChar();
          }
      }
      while (ch >= '0' && ch <= '9') {
          s.append(readChar());
          ch = lookChar();
      }
      if (ch == '.') {
         s.append(readChar());
         ch = lookChar();
         while (ch >= '0' && ch <= '9') {
             s.append(readChar());
             ch = lookChar();
         }
      }
      if (ch == 'E' || ch == 'e') {
         s.append(readChar());
         ch = lookChar();
         if (ch == '-' || ch == '+') {
             s.append(readChar());
             ch = lookChar();
         }
         while (ch >= '0' && ch <= '9') {
             s.append(readChar());
             ch = lookChar();
         }
      }
      return s.toString();
   }

   private static long readInteger(long min, long max) {  // read long integer, limited to specified range
      long x=0;
      while (true) {
         StringBuffer s=new StringBuffer(34);
         char ch=lookChar();
         while (ch == ' ' || ch == '\n') {
             readChar();
             if (ch == '\n');
                dumpString("? ",0);
             ch = lookChar();
         }
         if (ch == '-' || ch == '+') {
             s.append(readChar());
             ch = lookChar();
             while (ch == ' ') {
                readChar();
                ch = lookChar();
             }
         }
         while (ch >= '0' && ch <= '9') {
             s.append(readChar());
             ch = lookChar();
         }
         if (s.equals("")){
             errorMessage("Illegal integer input.",
                          "Integer in the range " + min + " to " + max);
         }
         else {
             String str = s.toString();
             try { 
                x = Long.parseLong(str);
             }
             catch (NumberFormatException e) {
                errorMessage("Illegal integer input.",
                             "Integer in the range " + min + " to " + max);
                continue;
             }
             if (x < min || x > max) {
                errorMessage("Integer input outside of legal range.",
                             "Integer in the range " + min + " to " + max);
                continue;
             }
             break;
         }
      }
      return x;
   }
   
   private static String realToString(double x) {
         // Goal is to get a reasonable representation of x in at most
         // 10 characters, or 11 characters if x is negative.
      if (Double.isNaN(x))
         return "undefined";
      if (Double.isInfinite(x))
         if (x < 0)
            return "-INF";
         else
            return "INF";
      if (Math.abs(x) <= 5000000000.0 && Math.rint(x) == x)
         return String.valueOf( (long)x );
      String s = String.valueOf(x);
      if (s.length() <= 10)
         return s;
      boolean neg = false;
      if (x < 0) {
         neg = true;
         x = -x;
         s = String.valueOf(x);
      }
      if (x >= 0.00005 && x <= 50000000 && (s.indexOf('E') == -1 && s.indexOf('e') == -1)) {  // trim x to 10 chars max
         s = round(s,10);
         s = trimZeros(s);
      }
      else if (x > 1) { // construct exponential form with positive exponent
          long power = (long)Math.floor(Math.log(x)/Math.log(10));
          String exp = "E" + power;
          int numlength = 10 - exp.length();
          x = x / Math.pow(10,power);
          s = String.valueOf(x);
          s = round(s,numlength);
          s = trimZeros(s);
          s += exp;
      }
      else { // constuct exponential form
          long power = (long)Math.ceil(-Math.log(x)/Math.log(10));
          String exp = "E-" + power;
          int numlength = 10 - exp.length();
          x = x * Math.pow(10,power);
          s = String.valueOf(x);
          s = round(s,numlength);
          s = trimZeros(s);
          s += exp;
      }
      if (neg)
         return "-" + s;
      else
         return s;
   }
   
   private static String trimZeros(String num) {  // used by realToString
     if (num.indexOf('.') >= 0 && num.charAt(num.length() - 1) == '0') {
        int i = num.length() - 1;
        while (num.charAt(i) == '0')
           i--;
        if (num.charAt(i) == '.')
           num = num.substring(0,i);
        else
           num = num.substring(0,i+1);
     }
     return num;
   }
   
   private static String round(String num, int length) {  // used by realToString
      if (num.indexOf('.') < 0)
         return num;
      if (num.length() <= length)
         return num;
      if (num.charAt(length) >= '5' && num.charAt(length) != '.') {
         char[] temp = new char[length+1];
         int ct = length;
         boolean rounding = true;
         for (int i = length-1; i >= 0; i--) {
            temp[ct] = num.charAt(i); 
            if (rounding && temp[ct] != '.') {
               if (temp[ct] < '9') {
                  temp[ct]++;
                  rounding = false;
               }
               else
                  temp[ct] = '0';
            }
            ct--;
         }
         if (rounding) {
            temp[ct] = '1';
            ct--;
         }
         // ct is -1 or 0
         return new String(temp,ct+1,length-ct);
      }
      else 
         return num.substring(0,length);
      
   }
   private static void dumpString(String str, int w) {   // output string to console
      for (int i=str.length(); i<w; i++)
         out.print(' ');
      for (int i=0; i<str.length(); i++)
         if ((int)str.charAt(i) >= 0x20 && (int)str.charAt(i) != 0x7F)  // no control chars or delete
            out.print(str.charAt(i));
         else if (str.charAt(i) == '\n' || str.charAt(i) == '\r')
            newLine();
   }
   
   private static void errorMessage(String message, String expecting) {
                  // inform user of error and force user to re-enter.
       newLine();
       dumpString("  *** Error in input: " + message + "\n", 0);
       dumpString("  *** Expecting: " + expecting + "\n", 0);
       dumpString("  *** Discarding Input: ", 0);
       if (lookChar() == '\n')
          dumpString("(end-of-line)\n\n",0);
       else {
          while (lookChar() != '\n')
             out.print(readChar());
          dumpString("\n\n",0);
       }
       dumpString("Please re-enter: ", 0);
       readChar();  // discard the end-of-line character
   }

   private static char lookChar() {  // return next character from input
      if (buffer == null || pos > buffer.length())
         fillBuffer();
      if (pos == buffer.length())
         return '\n';
      return buffer.charAt(pos);
   }

   private static char readChar() {  // return and discard next character from input
      char ch = lookChar();
      pos++;
      return ch;
   }

   private static void newLine() {   // output a CR to console
      out.println();
      out.flush();
   }

   private static boolean possibleLinefeedPending = false;

   private static void fillBuffer() {    // Wait for user to type a line and press return,
                                         // and put the typed line into the buffer.
      StringBuffer b = new StringBuffer();
      out.flush();
      try {
         int ch = in.read();
         if (ch == '\n' && possibleLinefeedPending)
            ch = in.read();
         possibleLinefeedPending = false;
         while (ch != -1 && ch != '\n' && ch != '\r') {
             b.append((char)ch);
             ch = in.read();
         }
         possibleLinefeedPending = (ch == '\r');
         if (ch == -1) {
            System.out.println("\n*** Found an end-of-file while trying to read from standard input!");
            System.out.println("*** Maybe your Java system doesn't implement standard input?");
            System.out.println("*** Program will be terminated.\n");
            throw new RuntimeException("End-of-file on standard input.");
         }
      }
      catch (IOException e) {
         System.out.println("Unexpected system error on input.");
         System.out.println("Terminating program.");
         System.exit(1);
      }
      buffer = b.toString();
      pos = 0;
   }

   private static void emptyBuffer() {   // discard the rest of the current line of input
      buffer = null;
   }
   
   
} // end of class Console
