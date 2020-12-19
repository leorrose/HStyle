import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-historical-style-generator',
  templateUrl: './historical-style-generator.component.html',
  styleUrls: ['./historical-style-generator.component.css']
})
export class HistoricalStyleGeneratorComponent implements OnInit {
  isUploadContent = true;
  isUploadStyle = false;
  isModelParams = false;
  contentImage: string | ArrayBuffer = '';
  styleImage: string | ArrayBuffer = '';
  contentImageError = '';
  styleImageError = '';

  images = ['assets/content_images/content copy 2.webp', 'assets/content_images/content copy 3.webp', 'assets/content_images/content copy 4.webp', 'assets/content_images/content copy.webp'];


  constructor() { }

  ngOnInit(): void {
  }

  goToContentImageUpload(): void{
    this.isUploadContent = true;
    this.isUploadStyle = false;
    this.isModelParams = false;
  }

  goToStyleImageUpload(): void{
    if (this.contentImage){
      this.isUploadContent = false;
      this.isUploadStyle = true;
      this.isModelParams = false;
    }
    else{
      this.contentImageError = 'Please upload a content image or select one from below!';
    }
  }

  goToSelectModelParameters(): void{
    if (this.styleImage){
      this.isUploadContent = false;
      this.isUploadStyle = false;
      this.isModelParams = true;
    }
    else{
      this.styleImageError = 'Please upload a style image or select one from below!';
    }
  }

  generateImage(): void{
    this.isUploadContent = false;
    this.isUploadStyle = false;
    this.isModelParams = false;
  }

  setContentImage(contentImage: string | ArrayBuffer): void {
    this.contentImage = contentImage;
  }

  setStyleImage(styleImage: string | ArrayBuffer): void {
    this.styleImage = styleImage;
  }
}
