# safedun-server
**A responsive web application for server-side image scrambling.**

<img align='center' src='https://github.com/adildsw/safedun-server/blob/master/assets/logo.png' />

<b>safedun-server</b> is a responsive web application for server-side image scrambling. Built with a very specific purpose of maintaining image privacy over web sharing, safedun-server can be hosted on the local network server, facilitating image scrambling directly to other devices on the network. safedun-server is made using a responsive, mobile-first web framework, making it platform-independent and usable over most mobile devices and computers alike.

## Getting Started
The following instructions will help you get safedun-server up and running in your preferred server/port. Before proceeding to the installation, make sure that your system contains all the prerequisites.

## Prerequisites
safedun-server is built on Python and uses external libraries like numpy, opencv and flask. Follow the instructions below to setup your system.

#### 1. Install Python 3.6+ ([Anaconda](https://www.anaconda.com/download/) distribution recommended)
#### 2. Install dependencies
Run the following command on the terminal/command prompt to install all the dependencies:
```
pip install numpy opencv-python flask
```

## Installing
Clone safedun-server repository into your system using the following command:
```
git clone https://github.com/adildsw/safedun-server.git
```

## Running safedun-server
### Starting the server
#### Navigate to the cloned repository directory.
```
cd safedun-server
```
#### Start the server
```
python server.py
```
Upon successful server hosting, the terminal/command prompt should return the following message:
```
* Serving Flask app "server" (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://x.x.x.x:port/ (Press CTRL+C to quit)
```
```http://x.x.x.x:port/``` is the address of the hosted server.

### Opening safedun-server
Once the server is up and running, open the address ```http://x.x.x.x:port/``` (refer to terminal/command prompt running the server) in your browser to open safedun-server.

<img src='https://github.com/adildsw/safedun-server/blob/master/assets/screen.png' />

### Closing the server
Open the terminal/command prompt running the server and press ```CTRL+C``` to terminate the server.

## How to use
safedun-server offers the functionality of encoding and decoding images. 

## Configuration
safedun-server allows users to change the default host IP, port number and activate debug mode.

### Starting the server in localhost
```
python server.py --local True
```

### Starting the server in a custom host IP/port
```
python server.py --host x.x.x.x --port xxxx
```

### Starting the server in debugging mode
```
python server.py --debug True
```

#### NOTE: By default, safedun-server attempts to host the server in the system's local network with the default port ```5000```.


## Results

  Cycle                    |  Key                      |  Original Image           |  Scrambled Image
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
1  |  @mAz!ng  |  ![](https://github.com/adildsw/safedun-server/blob/master/assets/1_@mAz!ng_input.png)  |  ![](https://github.com/adildsw/safedun-server/blob/master/assets/1_@mAz!ng_output.png)
5  |  van!llaTEA  |  ![](https://github.com/adildsw/safedun-server/blob/master/assets/5_van!llaTEA_input.png)  |  ![](https://github.com/adildsw/safedun-server/blob/master/assets/5_van!llaTEA_output.png)
10  |  thisIStotallyCrAzY  |  ![](https://github.com/adildsw/safedun-server/blob/master/assets/10_thisIStotallyCrAzY_input.png)  |  ![](https://github.com/adildsw/safedun-server/blob/master/assets/10_thisIStotallyCrAzY_output.png)
20  |  Sp@gheTT!  |  ![](https://github.com/adildsw/safedun-server/blob/master/assets/20_Sp@gheTT!_input.png)  |  ![](https://github.com/adildsw/safedun-server/blob/master/assets/20_Sp@gheTT!_output.png)

## Built With
* [Flask](https://palletsprojects.com/p/flask/) - Web Framework
* [Bulma](https://bulma.io) - CSS Framework

## License
MIT License

Copyright (c) 2019 Adil Rahman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

**Made with GitHub**
