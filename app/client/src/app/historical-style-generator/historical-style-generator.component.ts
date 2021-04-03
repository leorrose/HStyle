import { RestApiService } from './../services/rest-api.service';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { StyleTransferRequest } from '../models/style-transfer-request';
import { FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
    selector: 'app-historical-style-generator',
    templateUrl: './historical-style-generator.component.html',
    styleUrls: ['./historical-style-generator.component.css']
})
export class HistoricalStyleGeneratorComponent implements OnInit {
    contentImage: File = null;
    styleImage: File = null;
    addDilation = true;
    generateImageMessage = '';
    enableImageUploader = true;

    // form validators
    inputs = new FormGroup({
        email: new FormControl('', [
            Validators.required,
            Validators.pattern('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$')
        ]),
        styleLoss: new FormControl(0.01, [
            Validators.required,
            Validators.max(0.01),
            Validators.min(0.01)
        ]),
        contentLoss: new FormControl(150, [
            Validators.required,
            Validators.max(100000),
            Validators.min(10)
        ]),
        totalVariationLoss: new FormControl(30, [
            Validators.required,
            Validators.max(30),
            Validators.min(30)
        ]),
    });

    constructor(private restApiService: RestApiService, private changeDetector: ChangeDetectorRef) {


    }

    ngOnInit(): void {
    }

    /**
     * method to set the content image
     * @param contentImage the content image
     */
    setContentImage(contentImage: File): void {
        this.contentImage = contentImage;
    }

    /**
     * method to set the style image
     * @param styleImage the style image
     */
    setStyleImage(styleImage: File): void {
        this.styleImage = styleImage;
    }

    /**
     * method to call api with arguments to generate an image
     * @returns nothing
     */
    async generateImage(): Promise<void> {
        // test if inputs are valid
        if (!this.inputs.valid){
            this.inputs.markAllAsTouched();
            return;
        }


        // create request data object
        const reqData: StyleTransferRequest = {
            email: this.inputs.get('email').value,
            styleLoss: this.inputs.get('styleLoss').value,
            contentLoss: this.inputs.get('contentLoss').value,
            totalVariationLoss: this.inputs.get('totalVariationLoss').value,
            contentImage: this.contentImage,
            styleImage: this.styleImage,
            applyDilation: this.addDilation
        };

        // send request via service
        const response = await this.restApiService.generateImage(reqData);

        // display appropriate message to user
        if (response){
            this.generateImageMessage = `The process will take a few minutes. We will send the result
            to the given email address, please check your inbox`;
            this.inputs.reset({email: '', styleLoss: 0.01, contentLoss: 150, totalVariationLoss: 30});
            this.enableImageUploader = false;
            this.changeDetector.detectChanges();
            this.enableImageUploader = true;
        }
        else{
            this.generateImageMessage = 'A problem occurred will trying to generate image please check the given inputs and try again.';
            this.inputs.reset({email: '', styleLoss: 0.01, contentLoss: 150, totalVariationLoss: 30});
            this.enableImageUploader = false;
            this.changeDetector.detectChanges();
            this.enableImageUploader = true;
        }
    }

    /**
     * method to toggle the dilatation option
     */
    toggleDilation(): void {
        this.addDilation = !this.addDilation;
    }
}
