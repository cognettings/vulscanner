import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;

public class Test {

  public static void main(String[ ] args) {
    private String car = "Car", plane = "plane", boat = "boat";
    boolean isCar = true;
    String vehicle = "Car";
    try {
      int[] myNumbers = {1, 2, 3};
      System.out.println(myNumbers[10]);
    } catch (IndexException e) {
      if (e.toString() == "Error"){
        System.out.println("Error");
      }
      e.printStackTrace();
    }
    ArrayList<Integer> numbers = new ArrayList<Integer>();
    numbers.add(5);
    numbers.add(9);
    numbers.add(8);
    numbers.add(1);
    numbers.forEach( (n) -> {
			  System.out.println(n);
			  System.out.println(n);
			  System.out.println(n);
		  }
		);

    if(isCar)
    {
      System.out.println("I am a Car");
      for(int i=1; i<=5; i++){
    	  System.out.println("Car number :" + i);
      }
    }

    if(isCar)
    {
    	System.out.println("I am a Car");
    }
    else
    {
      System.out.println("I am a Truck");
      int counter = 0;
      while(counter < 5) {
          System.out.println("Truck number: " + counter);
          counter++;
          for(int i=1; i<=5; i++){
            System.out.println("Truck Number: " + i + ", " + counter);
            if (counter % 2 == 0){
              break;
            }else{
              continue;
            }
            System.out.println("Truck Number: " + i + ", " + counter);
        }
        if (counter > 4){
          break;
        }
        System.out.println("Finish");
      }
    }

    if(vehicle="Car")
    {
    	System.out.println("I am a Car");
    }
    else if(vehicle="Truck")
    {
    	System.out.println("I am a Truck");
    }
    else
    {
    	System.out.println("I am a Bike");
    }

    int age = 3;
    String yourAge;
    switch (age) {
        case 1:  System.out.println("You are one yr old");
                 break;
        case 2:  {
                 System.out.println("You are two yr old");
                 for(int i=1; i<=5; i++){
                  System.out.println("number :" + i);
                  if (i > 3){
                    break;
                    }
                 }
                 System.out.println("Finish");
              break;
            }
        case 3:  System.out.println("You are three yr old");
                 break;
        default: System.out.println("You are more than three yr old");
                 break;
    }

    int age = 2;
    String yourAge;
    switch (age) {
        case 1:  System.out.println("You are one yr old");
        case 2:  System.out.println("You are two yr old");
        case 3:  System.out.println("You are three yr old");
        default: System.out.println("You are more than three yr old");
			break;
    }

	int age = 2;
	String yourAge;
	switch (age) {
		case 1:
		case 2:
		case 3: System.out.println("You are three or less than three yr old");
			break;
		case 4:
		case 5:
		case 6: System.out.println("You are six or less than six yr old");
			break;
		default: System.out.println("You are more than six yr old");
			break;
	}

    int counter = 0;
    while(counter < 5) {
        System.out.println("Inside the while loop, counting: " + counter);
        counter++;
    }

    int counter = 0;
    do {
        System.out.println("Inside the while loop, counting: " + counter);
        counter++;
        for(int i=1; i<=5; i++){
          System.out.println("number :" + i);
            for(int j=1; j<=5; j++){
              int counter = 0;
              while(counter < 5) {
                if(counter==3)
                {
                  System.out.println("Breaking the for loop.");
                  break;
                }
                  System.out.println("Inside the while loop, counting: " + counter);
                  counter++;
                if (counter == 4){
                  continue;
                }
              }
              System.out.println("number :" + j);
            }
        }
    } while(counter < 5);

    for(int i=1; i<=5; i++){
    	  System.out.println("Printing using for loop. Count is: " + i);
    }

    String[] people = {"Vivek","Kavya","Aryan"};
    for (String person : people) {
      System.out.println("Hi, I am " + person);
      int age = 2;
      String yourAge;
      switch (age) {
        case 3: System.out.println("You are three or less than three yr old");
          break;
        case 5:
        case 6: System.out.println("You are six or less than six yr old");
          break;
        default: System.out.println("You are more than six yr old");
          break;
      }
    }

    for(int i=1; i<=5; i++){
    	if(i==3)
    	{
    		System.out.println("Breaking the for loop.");
    		break;
    	}
    	System.out.println("Printing using for loop. Count is: " + i);
    }

    int counter = 0;
    while(counter < 5) {
    	if(counter==3)
    	{
    		System.out.println("Breaking the for loop.");
    		break;
    	}
        System.out.println("Inside the while loop, counting: " + counter);
        counter++;
    }

    int[] nums = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    for (int i = 0; i < nums.length; i++) {
    	if (nums[i] % 2 != 0) {
    		continue;
    	}
    	System.out.println(nums[i] + " is even");
    }

	int[][] nums = { {1, 3, 7, 5},
					 {5, 8, 4, 6},
					 {7, 4, 2, 9} };
	int search = 8;

	for (int i = 0; i < nums.length; i++) {
		for (int j = 0; j < nums[i].length; j++) {
			if (nums[i][j] == search) {
				System.out.println(
					"Found " + search + " at position " + i + "," + j);
				break;
			}
		}
	}

  int counterTesti = 3;
  while(counterTesti < 5) counterTesti + 1;

  try {int j = 0;} catch (E e) {log(e);} catch (E2 e2) {log2(e);};
  try {int j = 0;} catch (E e) {log(e);};
  try {int j = 0;} finally {log(e);};
  try (T r = 0) {int j = 0;};
  }

  private class InnerTest {
  }

  interface Algebra1 {
   int operate(int a, int b);
  }
  public class LambdaCastingTest {
    public static void main(String[] args) {
        printResult((Algebra1)(a, b) -> a + b);
    }
  }
}
