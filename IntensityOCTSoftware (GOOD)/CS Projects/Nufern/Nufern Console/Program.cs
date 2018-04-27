using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Nufern_Console
{
    class Program
    {
        public bool Stop { get; set; }

        public bool ResponseRecieved
        {
            get; set;
        }

        public void ResponseHandler(String msg)
        {
            Console.WriteLine("Nufern Respone: " + msg + "  \r\n");
            ResponseRecieved = true;
        }

        public static void consoleHelp()
        {
            string h = "Commands: \r\n" + 
                        "-c X: Set the com port to X, i.e. -c COM1. This is \r\n"  + 
                        "       case sensitive!\r\n" +
                        "Press any key to quit... \r\n";
            Console.Write(h);
            Console.ReadKey();
        }

        public static void programHelp()
        {
            string h = "See Nufern manual for list of commands. \r\n" +
                        "on: turns the laser on, same as NUQON \r\n" +
                        "off: turns the laser off, same as NUQOFF \r\n" +
                        "prr, PRR: Gets the pulse repitition rate \r\n" +
                        "prr X, PRR X: Sets the pulse repitition rate, X is in kHz, i.e. PRR 30 is \r\n" +
                        "       set to 30kHz \r\n" +
                        "p, pow, POW: Gets the power of the laser \r\n" +
                        "p X, pow X, POW X: Sets the power of the laser, i.e. POW 10 is 10% power \r\n" +
                        "ERR: gets the last error command \r\n" +
                        "reset: Resets errors, same as RESERR \r\n" +
                        "g, gsta, GSTA: Gets the status of the system \r\n" +
                        "q or quit: stops the program \r\n\r\n";
            Console.Write(h);
        }

        static void Main(string[] args)
        {
            Program p = new Program();

            if(args.Length % 2 != 0)
            {
                consoleHelp();
                return;
            }

            string comport = null;

            for(int i = 0; i < args.Length; i+=2)
            {
                switch (args[i])
                {
                    case "-c":
                        comport = args[i + 1];
                        break;

                }
            }

            if(comport == null)
            {
                comport = "COM1";
            }

            Nufern.Nufern n = new Nufern.Nufern(comport);
            n.ResponseEvent += p.ResponseHandler;
            n.connect();

            while (!p.Stop)
            {

                for(int i = 0; i < 10; i++)
                {
                    Thread.Sleep(100);
                    if (p.ResponseRecieved)
                    {
                        break;
                    }
                }
                p.ResponseRecieved = false;

                Console.Write("Enter command or help or h for a list of commands: ");
                string input = Console.ReadLine();

                input = input.ToLower().Trim();
                string[] split = input.Split(' ');

                switch (split[0])
                {
                    case "q":
                    case "quit":
                        n.quit();
                        p.Stop = true;
                        break;

                    case "h":
                    case "help":
                        programHelp();
                        break;

                    case "prr":
                        if(split.Length == 1)
                        {
                            n.sendCommand("PRR");
                        }
                        else
                        {
                            n.sendCommand("PRR " + split[1]);
                        }
                        break;

                    case "on":
                        n.sendCommand("NUQON");
                        break;

                    case "off":
                        n.sendCommand("NUQOFF");
                        break;

                    case "p":
                    case "pow":
                        if(split.Length == 1)
                        {
                            n.sendCommand("POW");
                        }
                        else
                        {
                            n.sendCommand("POW " + split[1]);
                        }
                        break;

                    case "err":
                        n.sendCommand("ERR");
                        break;

                    case "reset":
                        n.sendCommand("RESERR");
                        break;

                    case "GSTA":
                    case "gsta":
                    case "g":
                        n.sendCommand("GSTA");
                        break;

                    default:
                        if (split.Length == 1)
                        {
                            n.sendCommand(split[0]);
                        }
                        else
                        {
                            n.sendCommand(split[0] + " " + split[1]);
                        }
                        break;
                }
            }
        }
    }
}
