![Angular linting badge](https://github.com/leorrose/HStyle/workflows/Server_side_linting/badge.svg)
![Angular coverage badge](https://github.com/leorrose/HStyle/workflows/Server_side_coverage/badge.svg)
![Python linting badge](https://github.com/leorrose/HStyle/workflows/Client_side_linting/badge.svg)
![Python coverage badge](https://github.com/leorrose/HStyle/workflows/Client_side_coverage/badge.svg)

# Hstyle

Historical documents can reveal a great deal of information about our past, such as, form of writing, 
wording, content that did not exist and more. In order to perform computational learning (Machine Learning) 
a huge amount of classified data (Classified Data) is needed. The process of creating classified data 
(Annotations) is expensive and tedious work, and therefore in the field of historical documents, 
the databases that exist for training models are small. These datasets do not allow training deep 
models to get high results.

In order to create a large database of data, in an easy way that requires less resources, it is necessary 
to create synthetic data. In the this project, we researched a method for creating synthetic 
historical data and developed a system (website) that allows each user to synthesize documents himself.

Our method is a deep learning method based on neural style transfer. In order to improve 
the results of the method, we used several techniques of computer vision, such as Binarization, 
Dilation and Image Processing.

This Project was created with **Python, FastAPI, TensorFlow, Keras, OpenCV, Angular, Bootstrap and more liberais**. 

## Project Research

In order to understand the steps and what we did you are welcome to look at 
the [**Project Book**](https://github.com/leorrose/HStyle/blob/master/research/Project_Book.pdf).

## Project Setup and Run
In order to run this project with docker your environment  needs to support  TensorFlow Docker. you can follow this [**link**](https://www.tensorflow.org/install/docker) to get everything set settled.

### Run on local environment:
1. Clone this repository.
2. Open cmd/shell/terminal and go to application folder: `cd Hstyle/app`
3. Run the docker-compose file: `docker-compose -f docker-compose-local.yml up`
4. Open this [link](http://localhost:3000/)
5. Enjoy the application.

### Run on production environment:
1. Clone this repository.
2. Open the following file: `Hstyle/app/client/src/environments/environment.prod.ts` 
3. In the opened file from step 2 change the API_URL to 'http://PRODUCTION_IP_ADDRESS:5000' where PRODUCTION_IP_ADDRESS is your deployment server IP address.
4. Open cmd/shell/terminal and go to application folder: `cd Hstyle/app`
5. Run the docker-compose file: `docker-compose -f docker-compose-prod.yml up``
6. Open this link http://PRODUCTION_IP_ADDRESS:3000/ where PRODUCTION_IP_ADDRESS is your deployment server IP address.
7. Enjoy the application.

## Demo
[![HStyle Demo](http://img.youtube.com/vi/7kMRTxFQWQo/0.jpg)](http://www.youtube.com/watch?v=7kMRTxFQWQo "HStyle Demo")


## Examples
| Content Image                   | Style Image                     | Changes Applied To Content Image| Result             |
|:-------------------------------:|:-------------------------------:|:----------:|:-------------------------------:|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/1/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/1/style.jpg)||![result](https://github.com/leorrose/HStyle/blob/master/examples/1/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/2/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/2/style.jpg)||![result](https://github.com/leorrose/HStyle/blob/master/examples/2/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/3/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/3/style.jpg)|Apply dilation|![result](https://github.com/leorrose/HStyle/blob/master/examples/3/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/4/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/4/style.jpg)|Apply dilation|![result](https://github.com/leorrose/HStyle/blob/master/examples/4/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/5/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/5/style.jpg)|Apply binarization|![result](https://github.com/leorrose/HStyle/blob/master/examples/5/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/6/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/6/style.jpg)|Apply binarization|![result](https://github.com/leorrose/HStyle/blob/master/examples/6/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/7/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/7/style.jpg)|Apply dilation and binarization|![result](https://github.com/leorrose/HStyle/blob/master/examples/7/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/8/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/8/style.jpg)|Apply dilation and binarization|![result](https://github.com/leorrose/HStyle/blob/master/examples/8/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/9/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/9/style.jpg)|Replace white background with style average pixel value|![result](https://github.com/leorrose/HStyle/blob/master/examples/1/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/10/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/10/style.jpg)|Replace white background with style average pixel value|![result](https://github.com/leorrose/HStyle/blob/master/examples/10/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/11/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/9/style.jpg)|Replace white background with style average pixel value + Apply dilation|![result](https://github.com/leorrose/HStyle/blob/master/examples/1/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/12/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/10/style.jpg)|Replace white background with style average pixel value + Apply dilation|![result](https://github.com/leorrose/HStyle/blob/master/examples/10/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/13/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/9/style.jpg)|Replace white background with style average pixel value + Apply binarization|![result](https://github.com/leorrose/HStyle/blob/master/examples/1/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/14/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/10/style.jpg)|Replace white background with style average pixel value + Apply binarization|![result](https://github.com/leorrose/HStyle/blob/master/examples/10/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/15/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/9/style.jpg)|Replace white background with style average pixel value + Apply binarization + Apply dilation|![result](https://github.com/leorrose/HStyle/blob/master/examples/1/result.png)|
| ![content](https://github.com/leorrose/HStyle/blob/master/examples/16/content.png)|![style](https://github.com/leorrose/HStyle/blob/master//examples/10/style.jpg)|Replace white background with style average pixel value + Apply binarization + Apply dilation|![result](https://github.com/leorrose/HStyle/blob/master/examples/10/result.png)|

## Evaluation
In order to evaluate and determine which technique is best from 3 techniques we thought have the best results (Original content image, Dilate content image, Binary content image), we performed a survey of 50 participants and asked them to rate image readability and image historical look, 1-being the lowest (poor), 5-being the highest (great).

**Result for image historical look**
![Historical Image Readability](https://github.com/leorrose/HStyle/blob/master/documentation/Historical%20Image%20Readability.png)
As we can see, ‘dilate content image’ and ‘binary content image’ get the highest amount of votes for rate three and above, meaning, these results have the highest readability.

**Result for image historical look**
![Image Historical Look](https://github.com/leorrose/HStyle/blob/master/documentation/Image%20Historical%20Look.png)
As we can see, ‘dilate content image’ gets the highest amount of votes for rate three and above, meaning, these results have the most historical look.

