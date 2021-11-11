# Stego-Project

If running in Linux terminal run the following commands:
Requesite: git clone https://github.com/ArmandoJM/Stego-Project.git
1. sudo apt install python3-pip
2. pip install imageio
3. pip install bitarray
4. sudo chmod u+x ./main.py
5. /.main.py -h img/Img_02_24.bmp ./file.txt output.bmp


If running in Windows do 
1. Download pycharm  at https://www.jetbrains.com/community/education/#students
2. In terminal do git clone https://github.com/ArmandoJM/Stego-Project.git
3. In terminal run curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
4. Continue using the terminal to run python get-pip.py
5. pip install imageio
6. pip install bitarray
7. pycharm change run/debug configuration to the following:
 Script Path : <dir-name>/Stego-Project
 Parameters:  "-h" 
               "img/Img_02_24.bmp"
               "./file.txt"
               "output.bmp"
