using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO.Ports;
using System.Threading;

namespace Nufern
{
    public class Nufern
    {
        SerialPort sp;

        public delegate void ResponseHandler(String msg);

        public event ResponseHandler ResponseEvent;

        bool _connected = false;

        String response = "";

        public Nufern(String comport)
        {
            sp = new SerialPort(comport);
            sp.BaudRate = 9600;
            sp.Parity = Parity.None;
            sp.StopBits = StopBits.One;
            sp.DataBits = 8;
            sp.Handshake = Handshake.None;
            sp.DataReceived += Sp_DataReceived;

            sp.Open();
        }

        private void Sp_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            response += sp.ReadExisting();

            if (response.Contains("\r\n"))
            {
                string[] split = response.Split(new string[] { "\r\n"}, StringSplitOptions.None);
                ResponseEvent(split[0]);
                _connected = true;
                response = "";
            }
        }

        public void quit()
        {
            sp.Close();
        }

        public void connect()
        {
            while (!_connected)
            {
                sp.Write("GSTA\r\n");
                Thread.Sleep(100);
            }
            sp.Write("S_232\r\n");
        }

        public void sendCommand(string cmd)
        {
            sp.Write(cmd + "\r\n");
        }
    }
}
