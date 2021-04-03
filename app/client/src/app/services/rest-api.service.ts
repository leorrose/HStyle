import { StyleTransferRequest } from './../models/style-transfer-request';
import { environment } from './../../environments/environment';
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class RestApiService {

    constructor(private http: HttpClient) { }

    /**
     * method to call api to generate image
     * @param data for api call
     * @returns true if request was successful else false
     */
    generateImage(data: StyleTransferRequest): Promise<boolean> {
        const formData = new FormData();
        formData.append('email', data.email);
        formData.append('content_loss', data.contentLoss.toString());
        formData.append('style_loss', data.styleLoss.toString());
        formData.append('total_variation_loss', data.totalVariationLoss.toString());
        formData.append('apply_dilation', data.applyDilation.toString());
        if (data.contentImage){
            formData.append('content_image', data.contentImage);
        }
        if (data.styleImage){
            formData.append('style_image', data.styleImage);
        }
        const url = environment.API_URL + '/api/styleTransfer/renderImage/';


        return this.http.post(url, formData).toPromise().then(
            (res: Response) => {
                return true;
            },
            (err: HttpErrorResponse) => {
                return false;
            }
        );
    }
}
