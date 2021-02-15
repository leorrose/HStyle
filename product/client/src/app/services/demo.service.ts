import { Injectable } from '@angular/core';
import { DemoImagesPaths } from '../models/demo-images-paths';

@Injectable({
  providedIn: 'root'
})
export class DemoService {

  constructor() { }

  getDemoImagesPaths(): DemoImagesPaths{
    const DemoImagesPaths = {
      contentImage: 'assets/hstyle_demo/content.webp',
      styleImage: 'assets/hstyle_demo/style.webp',
      resultImage: 'assets/hstyle_demo/result.webp'

    }
    return DemoImagesPaths
  }
}
