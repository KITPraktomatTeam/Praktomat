public class HelloWorld {
  public static void main (String[] args) {

    System.out.println("Hello World!");
  }
}


interface Bicycle {
	void speedUp(int increment);
}

class Tandem implements Bicycle {
	public void speedUp(int increment){
		// woooschhhhh
	}
}