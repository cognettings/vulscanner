using System;
using Project = PC.MyCompany.Project;

namespace MVCWebProdem.Controllers
{
    interface ISampleInterface
    {
        void SampleMethod();
    }
}

class cipher{

  public void Encrypt(byte[] key, byte[] data, MemoryStream target)
	{
    byte[] initializationVector = new byte[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 };
		using var aes = new AesCryptoServiceProvider();
		var encryptor = aes.CreateEncryptor(key, initializationVector);

  }

  public override void Bad(HttpRequest req, HttpResponse resp)
  {
    string data;
    string[] names = data.Split('-');
    int successCount = 0;
    if (data != null)
    {
      try
      {
        using (SqlConnection dbConnection = IO.GetDBConnection())
        {
          badSqlCommand.Connection = dbConnection;

          if (existingStudent != null)
          {
              existingStudent.FirstName = student.FirstName;
              existingStudent.LastName = student.LastName;

              ctx.SaveChanges();
          }
          else
          {
              return NotFound();
          }

          for (int i = 0; i < names.Length; i++)
          {
              /* POTENTIAL FLAW: data concatenated into SQL statement used in CommandText, which could result in SQL Injection */
              badSqlCommand.CommandText += "update users set hitcount=hitcount+1 where name='" + names[i] + "';";
          }
          successCount += affectedRows;
          IO.WriteLine("Succeeded in " + successCount + " out of " + names.Length + " queries.");
        }
      }
      catch (SqlException exceptSql)
      {
        IO.Logger.Log(NLog.LogLevel.Warn, "Error getting database connection", exceptSql);
      }
      finally
      {
        IO.Logger.Log(NLog.LogLevel.Warn, "Error disposing SqlCommand", exceptSql);
      }
    }
  }
}

public class Test {

  public static void main(String[ ] args) {

    int i = 0;
    while (i < 5) Console.WriteLine(i);

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

    try
    {
      ShowErrorMessage(result.Message);
    }
    catch (Exception)
    {
      throw;
    }
	}

  public partial class Customer{
    public string Number{
      set{
        this._Number = value;
      }
    }

    public string Name
    {
      get => _name;
      set => _name = value;
    }

    public string Email
    { get; set; }
  }

  public class CastExpr{
    IEnumerable<int> numbers = new int[] { 10, 20, 30 };
    IList<int> list = (IList<int>)numbers;
    var myValue = paidDate?.Day;
    string interpolated_var = $"{author} is an author of {book}" +
      $"The book price is ${price} and was published in year {year}";
    var student = new { Id = 1, FirstName = "James", LastName = "Bond" };
  }
}
