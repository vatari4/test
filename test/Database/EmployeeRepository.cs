using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.Data.SqlClient;
using EmployeeApp.Models;

namespace EmployeeApp.Database
{
    public class EmployeeRepository
    {
        private const string ConnectionString = @"Server=localhost;Database=EmployeeDB;Trusted_Connection=True;TrustServerCertificate=True;";

        public EmployeeRepository()
        {
            EnsureDatabase();
        }

        private void EnsureDatabase()
        {
            using var conn = new SqlConnection(ConnectionString);
            conn.Open();

            string createTable = @"
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Employees' AND xtype='U')
            CREATE TABLE Employees (
                EmployeeID INT IDENTITY(1,1) PRIMARY KEY,
                FirstName NVARCHAR(50),
                LastName NVARCHAR(50),
                Email NVARCHAR(100),
                DateOfBirth DATE,
                Salary DECIMAL(18,2)
            )";

            using var cmd = new SqlCommand(createTable, conn);
            cmd.ExecuteNonQuery();
        }

        public void AddEmployee(Employee emp)
        {
            using var conn = new SqlConnection(ConnectionString);
            conn.Open();

            string sql = @"INSERT INTO Employees (FirstName, LastName, Email, DateOfBirth, Salary)
                           VALUES (@FirstName, @LastName, @Email, @DateOfBirth, @Salary)";

            using var cmd = new SqlCommand(sql, conn);
            cmd.Parameters.AddWithValue("@FirstName", emp.FirstName);
            cmd.Parameters.AddWithValue("@LastName", emp.LastName);
            cmd.Parameters.AddWithValue("@Email", emp.Email);
            cmd.Parameters.AddWithValue("@DateOfBirth", emp.DateOfBirth);
            cmd.Parameters.AddWithValue("@Salary", emp.Salary);
            cmd.ExecuteNonQuery();
        }

        public List<Employee> GetAllEmployees()
        {
            var list = new List<Employee>();
            using var conn = new SqlConnection(ConnectionString);
            conn.Open();

            string sql = "SELECT EmployeeID, FirstName, LastName, Email, DateOfBirth, Salary FROM Employees";
            using var cmd = new SqlCommand(sql, conn);
            using var reader = cmd.ExecuteReader();

            while (reader.Read())
            {
                list.Add(new Employee
                {
                    EmployeeID = (int)reader["EmployeeID"],
                    FirstName = (string)reader["FirstName"],
                    LastName = (string)reader["LastName"],
                    Email = (string)reader["Email"],
                    DateOfBirth = (DateTime)reader["DateOfBirth"],
                    Salary = (decimal)reader["Salary"]
                });
            }
            return list;
        }

        public Employee? GetEmployeeById(int id)
        {
            using var conn = new SqlConnection(ConnectionString);
            conn.Open();

            string sql = "SELECT * FROM Employees WHERE EmployeeID=@ID";
            using var cmd = new SqlCommand(sql, conn);
            cmd.Parameters.AddWithValue("@ID", id);

            using var reader = cmd.ExecuteReader();
            if (reader.Read())
            {
                return new Employee
                {
                    EmployeeID = (int)reader["EmployeeID"],
                    FirstName = (string)reader["FirstName"],
                    LastName = (string)reader["LastName"],
                    Email = (string)reader["Email"],
                    DateOfBirth = (DateTime)reader["DateOfBirth"],
                    Salary = (decimal)reader["Salary"]
                };
            }
            return null;
        }

        public void UpdateEmployeeField(int id, string field, object value)
        {
            string sql = field switch
            {
                "FirstName" => "UPDATE Employees SET FirstName=@Value WHERE EmployeeID=@ID",
                "LastName" => "UPDATE Employees SET LastName=@Value WHERE EmployeeID=@ID",
                "Email" => "UPDATE Employees SET Email=@Value WHERE EmployeeID=@ID",
                "DateOfBirth" => "UPDATE Employees SET DateOfBirth=@Value WHERE EmployeeID=@ID",
                "Salary" => "UPDATE Employees SET Salary=@Value WHERE EmployeeID=@ID",
                _ => throw new Exception("Неверное поле для обновления.")
            };

            using var conn = new SqlConnection(ConnectionString);
            conn.Open();
            using var cmd = new SqlCommand(sql, conn);
            cmd.Parameters.AddWithValue("@Value", value);
            cmd.Parameters.AddWithValue("@ID", id);

            int affected = cmd.ExecuteNonQuery();
            if (affected == 0) throw new Exception("Сотрудник не найден.");
        }

        public void DeleteEmployee(int id)
        {
            using var conn = new SqlConnection(ConnectionString);
            conn.Open();
            using var cmd = new SqlCommand("DELETE FROM Employees WHERE EmployeeID=@ID", conn);
            cmd.Parameters.AddWithValue("@ID", id);

            int affected = cmd.ExecuteNonQuery();
            if (affected == 0) throw new Exception("Сотрудник не найден.");
        }

        public int CountAboveAverageSalary()
        {
            using var conn = new SqlConnection(ConnectionString);
            conn.Open();

            string sql = @"SELECT COUNT(*) FROM Employees 
                           WHERE Salary > (SELECT AVG(Salary) FROM Employees)";
            using var cmd = new SqlCommand(sql, conn);
            return (int)cmd.ExecuteScalar();
        }
    }
}
