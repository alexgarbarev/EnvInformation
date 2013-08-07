EnvInformation.py
=================

Script helpful when you want to print latest git commit hash, compiler version, Xcode version in your iOS application console. 
It helpful to identify .ipa (or .xcarchive, or .app) archive with git commit to debug. Or show commit number as version in your application.

![Add script](/images/Enviroment.png "Optional title")

How to use
=================

1. Copy EnvInformation.py to your project folder, (for example to scripts subdirectory)  
2. Open your Xcode project, go to project settings and navigate to Build Phases tab
3. Press "Add Build Phase" button -> "Add Run Script"
![Add script](/images/AddPhase.png "Optional title")
4. Drag and drop added script before "Copy Bundle Resources" phase
5. Write "scripts/EnvInformation.py -w -o Resources" where "scripts" is folder where script located, "Resources" - output folder 
6. Do steps 3 again, but now script phase should be after "Copy Bundle Resources" phase
7. Write "scripts/EnvInformation.py -r -o Resources". 

Now you should get something like:
![Add script](/images/Result.png "Optional title")

Thats all. 

"EnvInformation.py -w" will write environment information, "EnvInformation.py -r" will revert back to empty plist, it needed to not commit Enviroment.plist each time it changed.
You can add empty Enviroment.plist to Xcode project and use in application to display git or compiler information