import { Injectable } from '@angular/core';
import { DemoImagesPaths } from '../models/demo-images-paths';

@Injectable({
    providedIn: 'root'
})
export class DemoService {

    constructor() { }

    /**
     * method to get application demo images paths
     * @returns the paths to demo images
     */
    getDemoImagesPaths(): DemoImagesPaths {
        const Paths: DemoImagesPaths = {
            contentImage: 'assets/HStyle_demo/content.webp',
            styleImage: 'assets/HStyle_demo/style.webp',
            resultImage: 'assets/HStyle_demo/result.webp'

        };
        return Paths;
    }
}
