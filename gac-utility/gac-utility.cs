using System;
using System.Text;
using System.EnterpriseServices.Internal;

namespace gac_utility
{
    class Entry
    {
        
        static int Main(string[] args)
        {
            int nRet = 0;
            if (args.Length == 0)
            {
                //show usage
                string usage = " no parameters defined\n usage: gac-utility <-i><-u> assembly path";
                Console.WriteLine(usage);
                nRet= - 1;
            }
            else if(args[0]== "-i")
            {
                if (System.Reflection.Assembly.LoadFile(args[1]).GetName().GetPublicKey().Length > 0)
                {
                    Publish objPublish = new Publish();
                    Console.WriteLine("Adding {0} to GAC", args[1]);
                    try
                    {
                        objPublish.GacInstall(args[1]);
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("Error {0} Cannot add assembly to GAC!", e);
                        nRet = -1;
                    }
                }
                else
                {
                    Console.WriteLine("Error {0} not signed cannot add to GAC!", args[1]);
                    nRet = -1; 
                }            
            }
            else if(args[0]== "-u")
            {
                Publish objPublish = new Publish();
                Console.WriteLine("Removing {0} from GAC", args[1]);
                try
                {
                    objPublish.GacRemove(args[1]);
                    nRet = 0;
                }
                catch (Exception e)
                {
                    Console.WriteLine("Error {0} Cannot remove assembly from GAC?", e);
                    nRet = -1;
                }
            }
            return nRet;
        }
    }
}
