'''
Created on Feb 7, 2016

@author: Devandra
'''
import sys
from BasicClient import BasicClient
    

class BasicClientApp:
    def run(self):
        name = None
        while name==None:
            print("Enter your name in order to join: ");
            name = sys.stdin.readline()
            if name!=None:
                break
            
        bc =BasicClient('127.0.0.1',5000)
        bc.startSession()
        bc.setName(name)
        bc.join(name)

        print("\nWelcome " + name + "\n")
        print("Commands\n");
        print("-----------------------------------------------\n");
        print("help - show this menu \n");
        print("post - send a message to the group (default)\n");
        print("whoami - list my settings\n");
        print("exit - end session\n");
        print("\n");

        forever = True;
        while (forever):
                choice = sys.stdin.readline()

                print("")
                print(choice.lower())
                if (choice == None):
                    continue;
                elif ('whoami' in choice.lower()):
                    print("You are " + bc.getName());
                elif ('exit' in choice.lower()):
                    print("EXIT CMD!");
                    bc.stopSession();
                    forever = False;
                elif ('post' in choice.lower()):
                    print("Enter message: ");
                    msg = sys.stdin.readline()
                    bc.sendMessage(msg);
                elif ('help' in choice.lower()):
                    print("");
                    print("Commands");
                    print("-------------------------------");
                    print("help - show this menu");
                    print("post - send a message");
                    print("list - list connections");
                    print("exit - end session");
                    print("");
                else:
                    bc.sendMessage(choice);
        print("\nGoodbye\n");
        
        
if __name__ == '__main__':
    ca = BasicClientApp();
    ca.run();