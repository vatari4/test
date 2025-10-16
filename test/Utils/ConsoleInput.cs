using System;
using System.Globalization;

namespace EmployeeApp.Utils
{
    public static class ConsoleInput
    {
        public static string ReadString(string prompt)
        {
            Console.Write(prompt);
            return Console.ReadLine() ?? "";
        }

        public static int ReadInt(string prompt)
        {
            while (true)
            {
                Console.Write(prompt);
                if (int.TryParse(Console.ReadLine(), out int value))
                    return value;
                Console.WriteLine("Неверный ввод. Попробуйте снова.");
            }
        }

        public static decimal ReadDecimal(string prompt)
        {
            while (true)
            {
                Console.Write(prompt);
                if (decimal.TryParse(Console.ReadLine(), out decimal value))
                    return value;
                Console.WriteLine("Неверный ввод. Попробуйте снова.");
            }
        }

        public static DateTime ReadDate(string prompt)
        {
            var culture = new CultureInfo("ru-RU");
            while (true)
            {
                Console.Write($"{prompt} (дд.мм.гггг): ");
                string input = Console.ReadLine() ?? "";
                if (DateTime.TryParseExact(input, "dd.MM.yyyy", culture, DateTimeStyles.None, out DateTime value))
                    return value;
                Console.WriteLine("Неверный формат. Введите дату в формате дд.мм.гггг, например 15.10.2025");
            }
        }
    }
}
