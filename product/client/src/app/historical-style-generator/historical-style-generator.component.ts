import { RestApiService } from './../services/rest-api.service';
import { Component, OnInit } from '@angular/core';
import { StyleTransferRequest } from '../models/style-transfer-request';

@Component({
  selector: 'app-historical-style-generator',
  templateUrl: './historical-style-generator.component.html',
  styleUrls: ['./historical-style-generator.component.css']
})
export class HistoricalStyleGeneratorComponent implements OnInit {
  contentImage: File = null;
  styleImage: File = null;
  isDefaultContentImage = true;
  isDefaultStyleImage = true;
  styleLoss:number = 0.01;
  totalVariationLoss:number = 30;
  contentLossInput: number = 150;
  contentLossInputWarning = '';
  contentLossInputMin = 10;
  contentLossInputMax = 100000;
  addDilation = true;


  constructor(private restApiService:RestApiService) { }

  ngOnInit(): void {
  }

  setContentImage(contentImage: File): void {
    this.contentImage = contentImage;
    if (this.contentImage == null){
      this.isDefaultContentImage = true;
    }
    else{
      this.isDefaultContentImage = false;
    }
  }

  setStyleImage(styleImage: File): void {
    this.styleImage = styleImage;
    if (this.styleImage == null){
      this.isDefaultStyleImage = true;
    }
    else{
      this.isDefaultStyleImage = false;
    }
  }

  async generateImage(): Promise<void>{
    if(this.contentLossInput < this.contentLossInputMin || this.contentLossInput > this.contentLossInputMax){
      this.contentLossInputWarning = "Content Loss needs to be between 10 to 100000"
    }

    let reqData: StyleTransferRequest = {
      styleLoss: this.styleLoss,
      contentLoss: this.contentLossInput,
      totalVariationLoss: this.totalVariationLoss,
      contentImage: this.contentImage,
      styleImage: this.styleImage,
      applyDilation: this.addDilation
    }
    console.log(await this.restApiService.test(reqData));
  }

  toggleDilation(): void{
    this.addDilation = !this.addDilation;
  }
}
