using System;
using EmployeeApp.Models;
using EmployeeApp.Utils;
using EmployeeApp.Database;

namespace EmployeeApp
{
    class Program
    {
        static void Main()
        {
            var repo = new EmployeeRepository();

            while (true)
            {
                Console.WriteLine("\nМеню управления сотрудниками");
                Console.WriteLine("1. Добавить нового сотрудника");
                Console.WriteLine("2. Посмотреть всех сотрудников");
                Console.WriteLine("3. Обновить информацию о сотруднике");
                Console.WriteLine("4. Удалить сотрудника");
                Console.WriteLine("5. Кол-во сотрудников с зарплатой выше средней");
                Console.WriteLine("6. Выйти");
                Console.Write("Выберите пункт:");

                var choice = Console.ReadLine();

                try
                {
                    switch (choice)
                    {
                        case "1": AddEmployee(repo); break;
                        case "2": ViewEmployees(repo); break;
                        case "3": UpdateEmployee(repo); break;
                        case "4": DeleteEmployee(repo); break;
                        case "5": CountAboveAverageSalary(repo); break;
                        case "6": return;
                        default: Console.WriteLine("Неверный выбор."); break;
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Ошибка: {ex.Message}");
                }
            }
        }

        static void AddEmployee(EmployeeRepository repo)
        {
            var emp = new Employee
            {
                FirstName = ConsoleInput.ReadString("Имя: "),
                LastName = ConsoleInput.ReadString("Фамилия: "),
                Email = ConsoleInput.ReadString("Email: "),
                DateOfBirth = ConsoleInput.ReadDate("Дата рождения"),
                Salary = ConsoleInput.ReadDecimal("Зарплата: ")
            };
            repo.AddEmployee(emp);
            Console.WriteLine("Сотрудник добавлен.");
        }

        static void ViewEmployees(EmployeeRepository repo)
        {
            var employees = repo.GetAllEmployees();
            if (employees.Count == 0)
            {
                Console.WriteLine("Сотрудников нет.");
                return;
            }
            foreach (var e in employees)
                Console.WriteLine($"{e.EmployeeID}: {e.FirstName} {e.LastName}, {e.Email}, {e.DateOfBirth:dd.MM.yyyy}, Зарплата: {e.Salary}");
        }

        static void UpdateEmployee(EmployeeRepository repo)
        {
            int id = ConsoleInput.ReadInt("Введите ID сотрудника: ");
            var emp = repo.GetEmployeeById(id);
            if (emp == null)
            {
                Console.WriteLine("Сотрудник не найден.");
                return;
            }

            Console.WriteLine("\nВыберите поле для обновления:");
            Console.WriteLine("1. FirstName (Имя)");
            Console.WriteLine("2. LastName (Фамилия)");
            Console.WriteLine("3. Email");
            Console.WriteLine("4. DateOfBirth (Дата рождения)");
            Console.WriteLine("5. Salary (Зарплата)");
            Console.Write("Введите номер или название поля: ");
            string input = Console.ReadLine()?.Trim() ?? "";

            string field = input switch
            {
                "1" => "FirstName",
                "2" => "LastName",
                "3" => "Email",
                "4" => "DateOfBirth",
                "5" => "Salary",
                "FirstName" => "FirstName",
                "LastName" => "LastName",
                "Email" => "Email",
                "DateOfBirth" => "DateOfBirth",
                "Salary" => "Salary",
                _ => throw new Exception("Неверный выбор поля.")
            };

            object val = field switch
            {
                "FirstName" => ConsoleInput.ReadString("Новое имя: "),
                "LastName" => ConsoleInput.ReadString("Новая фамилия: "),
                "Email" => ConsoleInput.ReadString("Новый Email: "),
                "DateOfBirth" => ConsoleInput.ReadDate("Новая дата рождения"),
                "Salary" => ConsoleInput.ReadDecimal("Новая зарплата: "),
                _ => throw new Exception("Неверное поле.")
            };

            repo.UpdateEmployeeField(id, field, val);
            Console.WriteLine("Обновление выполнено.");
        }


        static void DeleteEmployee(EmployeeRepository repo)
        {
            int id = ConsoleInput.ReadInt("Введите ID сотрудника: ");
            repo.DeleteEmployee(id);
            Console.WriteLine("Сотрудник удалён.");
        }

        static void CountAboveAverageSalary(EmployeeRepository repo)
        {
            int count = repo.CountAboveAverageSalary();
            Console.WriteLine($"Количество сотрудников с зарплатой выше средней: {count}");
        }
    }
}
