import { Component, OnInit } from '@angular/core';
import { DemoImagesPaths } from '../models/demo-images-paths';
import { DemoService } from '../services/demo.service';

@Component({
    selector: 'app-demo',
    templateUrl: './demo.component.html',
    styleUrls: ['./demo.component.css']
})
export class DemoComponent implements OnInit {
    demoImages: DemoImagesPaths;
    constructor(private demoService: DemoService) { }

    ngOnInit(): void {
        this.demoImages = this.demoService.getDemoImagesPaths();
    }
}
