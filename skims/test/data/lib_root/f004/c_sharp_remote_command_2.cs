using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;

namespace Testcase
{
    public class Testclass : Controller
    {
        public UnsafeProcess Run(HttpRequest query)
        {
            Process p = new Process();
            data = query.ReadLine();
            p.Start(data);
        }
    }
}
