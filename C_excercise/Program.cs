using System;
using System.Data;
using System.Numerics;
using C_excercise;
namespace Hello
{
    public class Program {
        public static void Main(String[] args) {
            List<int> list = new List<int>();
            list.Add(1);
            list.Add(3);
            list.Add(2);
            list.RemoveAt(0);
            Console.WriteLine(list);
            for (int i  = 0;i<list.Count;i++) {
                Console.WriteLine(list[i]);
            }
        }
    }
}